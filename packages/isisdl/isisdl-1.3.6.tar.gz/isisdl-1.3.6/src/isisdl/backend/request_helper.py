from __future__ import annotations

import os
import random
import re
import time
from base64 import standard_b64decode
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from email.utils import parsedate_to_datetime
from itertools import repeat, chain
from pathlib import Path
from queue import Queue
from threading import Thread, Lock, current_thread
from typing import Optional, Dict, List, Any, cast, Union, Iterable, DefaultDict, Tuple
from urllib.parse import urlparse

from requests import Session, Response
from requests.adapters import HTTPAdapter
from requests.exceptions import InvalidSchema

from isisdl.backend.crypt import get_credentials
from isisdl.backend.status import StatusOptions, DownloadStatus, RequestHelperStatus
from isisdl.settings import download_timeout, download_timeout_multiplier, download_static_sleep_time, num_tries_download, status_time, perc_diff_for_checksum, error_text, bandwidth_mavg_perc, \
    extern_ignore, log_file_location, datetime_str
from isisdl.settings import enable_multithread, discover_num_threads, is_windows, is_testing, testing_bad_urls, url_finder, isis_ignore
from isisdl.utils import User, path, sanitize_name, args, on_kill, database_helper, config, generate_error_message, logger, parse_google_drive_url, get_url_from_gdrive_confirmation, \
    DownloadThrottler, MediaType, HumanBytes
from isisdl.utils import calculate_local_checksum
from isisdl.version import __version__


class SessionWithKey(Session):
    key: str
    token: str

    __slots__ = tuple(__annotations__)  # type: ignore

    _lock = Lock()

    def __init__(self, key: str, token: str):
        super().__init__()
        self.key = key
        self.token = token

        # Increase the number of recycled connections (Copied from https://stackoverflow.com/a/18845952/18680554)
        self.mount("https://", HTTPAdapter(pool_maxsize=discover_num_threads // 2, pool_block=False))

    @classmethod
    def from_scratch(cls, user: User) -> Optional[SessionWithKey]:
        try:
            s = cls("", "")
            s.headers.update({"User-Agent": "isisdl (Python Requests)"})

            s.get_("https://isis.tu-berlin.de/auth/shibboleth/index.php?")
            s.post_("https://shibboleth.tubit.tu-berlin.de/idp/profile/SAML2/Redirect/SSO?execution=e1s1",
                    data={
                        "shib_idp_ls_exception.shib_idp_session_ss": "",
                        "shib_idp_ls_success.shib_idp_session_ss": "false",
                        "shib_idp_ls_value.shib_idp_session_ss": "",
                        "shib_idp_ls_exception.shib_idp_persistent_ss": "",
                        "shib_idp_ls_success.shib_idp_persistent_ss": "false",
                        "shib_idp_ls_value.shib_idp_persistent_ss": "",
                        "shib_idp_ls_supported": "", "_eventId_proceed": "",
                    })

            response = s.post_("https://shibboleth.tubit.tu-berlin.de/idp/profile/SAML2/Redirect/SSO?execution=e1s2",
                               params={"j_username": user.username, "j_password": user.password, "_eventId_proceed": ""})

            if response is None or response.url == "https://shibboleth.tubit.tu-berlin.de/idp/profile/SAML2/Redirect/SSO?execution=e1s3":
                # The redirection did not work → credentials are wrong
                return None

            # Extract the session key
            _key = re.findall(r"\"sesskey\":\"(.*?)\"", response.text)
            if not _key:
                return None

            key = _key[0]

            try:
                # This is a somewhat dirty hack.
                # The Moodle API always wants to have a token. This is obtained through the `/login/token.php` site.
                # Since ISIS handles authentication via SSO, the entered password is invalid every time.

                # In [1] this way of obtaining the token is described.
                # I would love to get a better way working, but unfortunately it seems as if it is not supported.
                #
                # [1]: https://github.com/C0D3D3V/Moodle-Downloader-2/wiki/Obtain-a-Token#get-a-token-with-sso-login

                # Note: Don't replace .get by .get_ - Since the .get_ will catch all exceptions.

                s.get("https://isis.tu-berlin.de/admin/tool/mobile/launch.php?service=moodle_mobile_app&passport=12345&urlscheme=moodledownloader")
                raise InvalidSchema
            except InvalidSchema as ex:
                token = standard_b64decode(str(ex).split("token=")[-1]).decode().split(":::")[1]

            s.key = key
            s.token = token

            return s

        except Exception as ex:
            generate_error_message(ex)

    @staticmethod
    def _timeouter(func: Any, url: str, *args: Iterable[Any], **kwargs: Dict[Any, Any]) -> Any:
        if "tubcloud.tu-berlin.de" in url:
            # The tubcloud is *really* slow
            _download_timeout = 20
        else:
            _download_timeout = download_timeout

        i = 0
        while i < num_tries_download:
            try:
                return func(url, *args, timeout=_download_timeout + download_timeout_multiplier ** (0.5 * i), **kwargs)

            except Exception:
                time.sleep(download_static_sleep_time)
                i += 1

    def get_(self, url: str, *args: Any, **kwargs: Any) -> Optional[Response]:
        return cast(Optional[Response], self._timeouter(super().get, url, *args, **kwargs))

    def post_(self, url: str, *args: Any, **kwargs: Any) -> Optional[Response]:
        return cast(Optional[Response], self._timeouter(super().post, url, *args, **kwargs))

    def head_(self, url: str, *args: Any, **kwargs: Any) -> Optional[Response]:
        return cast(Optional[Response], self._timeouter(super().head, url, *args, **kwargs))

    def __str__(self) -> str:
        return "~Session~"

    def __repr__(self) -> str:
        return "~Session~"


class PreMediaContainer:
    url: str
    _name: Optional[str]
    time: Optional[int]
    size: Optional[int]
    course: Course
    media_type: MediaType
    is_cached: bool
    parent_path: Path

    __slots__ = tuple(__annotations__)  # type: ignore

    def __init__(self, url: str, course: Course, media_type: MediaType, name: Optional[str] = None, relative_location: Optional[str] = None, size: Optional[int] = None, time: Optional[int] = None):
        relative_location = (relative_location or media_type.dir_name).strip("/")
        if config.make_subdirs is False:
            relative_location = ""

        if url.endswith("?forcedownload=1"):
            url = url[:-len("?forcedownload=1")]

        self.url = url
        self._name = name
        self.time = time
        self.size = size
        self.course = course
        self.media_type = media_type
        self.is_cached = not (database_helper.know_url(url, course.course_id) is True)
        self.parent_path = course.path(sanitize_name(relative_location, True))
        self.parent_path.mkdir(exist_ok=True)

    def __str__(self) -> str:
        return f"{self._name}: {self.course}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def is_ready(self) -> bool:
        return self._name is not None and self.time is not None and self.size is not None


class MediaContainer:
    _name: str
    url: str
    download_url: str
    path: Path
    time: int
    course: Course
    media_type: MediaType
    size: int
    _links: List[MediaContainer]
    checksum: Optional[str]
    current_size: Optional[int]
    _stop: bool
    _done: bool
    _newly_downloaded: bool
    _newly_discovered: bool

    __slots__ = tuple(__annotations__)  # type: ignore

    def __init__(self, _name: str, url: str, download_url: str, path: Path, time: int, course: Course, media_type: MediaType, size: int,
                 checksum: Optional[str] = None, _links: Optional[List[MediaContainer]] = None,
                 _newly_downloaded: bool = False, _newly_discovered: bool = False) -> None:
        self._name = _name
        self.url = url
        self.download_url = download_url
        self.path = path
        self.time = time
        self.course = course
        self.media_type = media_type
        self.size = size
        self.checksum = checksum
        self.current_size = None
        self._stop = False
        self._links = _links or []
        self._done = False
        self._newly_downloaded = _newly_downloaded
        self._newly_discovered = _newly_discovered

    @classmethod
    def from_dump(cls, url: str, course: Course) -> Union[bool, MediaContainer]:
        """
        The `bool` return value indicates if the container should be downloaded.
        """
        info = database_helper.know_url(url, course.course_id)
        if isinstance(info, bool):
            return info

        container = cls(*info)
        container.media_type = MediaType(container.media_type)
        container.path = Path(container.path)

        course_id: int = container.course  # type: ignore
        if course_id not in RequestHelper.course_id_mapping:
            return True

        container.course = RequestHelper.course_id_mapping[course_id]

        if is_testing:
            if container.media_type == MediaType.corrupted:
                assert container.size == 0
            else:
                assert container.size != 0 and container.size != -1

        return container

    @classmethod
    def from_pre_container(cls, container: PreMediaContainer, session: SessionWithKey, status: Optional[RequestHelperStatus] = None) -> Optional[MediaContainer]:
        con: Optional[Response] = None
        try:
            if is_testing and container.url in testing_bad_urls:
                return None

            maybe_container = MediaContainer.from_dump(container.url, container.course)
            if isinstance(maybe_container, MediaContainer):
                return maybe_container

            elif maybe_container is False:
                return None

            # If there was not enough information to determine name, size and time for the container, get it.
            download_url = None
            if "tu-berlin.hosted.exlibrisgroup.com" in container.url:
                pass

            elif "https://drive.google.com/" in container.url:
                drive_id = parse_google_drive_url(container.url)
                if drive_id is None:
                    database_helper.add_bad_url(container.url)
                    return None

                temp_url = "https://drive.google.com/uc?id={id}".format(id=drive_id)

                try:
                    con = session.get_(temp_url, stream=True)
                    if con is None:
                        raise ValueError
                except Exception:
                    database_helper.add_bad_url(container.url)
                    return None

                if "Content-Disposition" in con.headers:
                    # This is the file
                    download_url = temp_url
                else:
                    _url = get_url_from_gdrive_confirmation(con.text)
                    if _url is None:
                        database_helper.add_bad_url(container.url)
                        return None
                    download_url = _url

                con.close()

            elif "tubcloud.tu-berlin.de" in container.url:
                if container.url.endswith("/download"):
                    download_url = container.url
                else:
                    download_url = container.url + "/download"

            # TODO: More content
            elif "youtube.com" in container.url or "youtu.be" in container.url:
                pass

            elif "link.springer.com" in container.url:
                pass

            elif 'prezi.com' in container.url:
                pass

            elif "docs.google.com/document" in container.url:
                pass

            elif 'doi.org' in container.url:
                pass

            elif 'video.isis.tu-berlin.de' in container.url:
                pass

            elif 'www.sciencedirect.com' in container.url:
                pass

            elif 'onlinelibrary.wiley.com' in container.url:
                pass

            if container.is_ready:
                assert container._name is not None and container.time is not None and container.size is not None
                return cls(container._name, container.url, container.url, container.parent_path.joinpath(sanitize_name(container._name, False)),
                           container.time, container.course, container.media_type, container.size, _newly_discovered=True).dump()

            con = session.get_(download_url or container.url, params={"token": session.token}, stream=True)
            if con is None:
                database_helper.add_bad_url(container.url)
                return None

            media_type = container.media_type
            if not (con.ok and "Content-Type" in con.headers and (con.headers["Content-Type"].startswith("application/") or con.headers["Content-Type"].startswith("video/"))):
                media_type = MediaType.corrupted

            if container._name is not None:
                name = container._name
            else:
                if maybe_names := re.findall("filename=\"(.*?)\"", str(con.headers)):
                    name = maybe_names[0]
                else:
                    name = os.path.basename(container.url)

            if media_type == MediaType.corrupted:
                size = 0
            elif container.size is not None:
                size = container.size
            else:
                if "Content-Length" not in con.headers:
                    size = -1
                    media_type = MediaType.corrupted
                else:
                    size = int(con.headers["Content-Length"])

            if container.time is not None:
                time = container.time
            elif "Last-Modified" in con.headers:
                try:
                    time = int(parsedate_to_datetime(con.headers["Last-Modified"]).timestamp())
                except Exception:
                    time = int(datetime.now().timestamp())
            else:
                time = int(datetime.now().timestamp())

            if not (con.ok and "Content-Type" in con.headers and (con.headers["Content-Type"].startswith("application/") or con.headers["Content-Type"].startswith("video/"))):
                media_type = MediaType.corrupted

            if is_testing:
                if media_type == MediaType.corrupted:
                    assert size == 0
                else:
                    assert size != 0 and size != -1

            return cls(name, container.url, download_url or container.url, container.parent_path.joinpath(sanitize_name(name, False)), time, container.course, media_type, size,
                       _newly_discovered=True).dump()

        finally:
            container.is_cached = True
            if con is not None:
                con.close()

            if not container.is_ready and status is not None and status.status == StatusOptions.building_cache:
                status.done()

    @property
    def should_download(self) -> bool:
        if self._done or self.media_type == MediaType.corrupted:
            return False

        if not self.path.exists():
            actual_size = 0
        else:
            actual_size = self.path.stat().st_size

        maybe_container = MediaContainer.from_dump(self.url, self.course)
        if isinstance(maybe_container, bool):
            return maybe_container

        if maybe_container.checksum is not None:
            return False

        if actual_size == 0 or not (self.size * (1 - perc_diff_for_checksum) <= actual_size <= self.size * (1 + perc_diff_for_checksum)):
            return True

        if self.size == actual_size:
            return False

        return calculate_local_checksum(self.path) == maybe_container.checksum

    def dump(self) -> MediaContainer:
        database_helper.add_pre_container(self)
        return self

    def string_dump(self) -> str:
        return f"Name: {sanitize_name(self._name, False)!r}\nCourse: {self.course!r}\nSize: {HumanBytes.format_str(self.size)}\n" \
               f"Time: {datetime.fromtimestamp(self.time).strftime(datetime_str)}\nIs downloaded: {self.checksum is not None}\n"

    def __str__(self) -> str:
        if config.absolute_path_filename:
            return str(self.path)

        return sanitize_name(self._name, False)

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return self.url.__hash__()

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False

        acc = True
        for attr in self.__slots__:
            if attr in {"current_size", "_links", "_done", "_newly_downloaded", "_newly_discovered"}:
                continue

            self_val = getattr(self, attr)
            other_val = getattr(other, attr)

            acc &= self_val == other_val and type(self_val) == type(other_val)

        return acc

    def __gt__(self, other: MediaContainer) -> bool:
        return int.__gt__(self.size, other.size)

    def stop(self) -> None:
        self._stop = True

    def download(self, throttler: DownloadThrottler, session: SessionWithKey, is_stream: bool = False) -> None:
        if self._stop or self.media_type == MediaType.corrupted:
            self._done = True
            return

        if self.current_size is not None:
            return

        self.current_size = 0

        if not self.should_download:
            self.current_size = self.size
            self._done = True
            return

        if is_stream:
            throttler.start_stream(self.path)

        download = session.get_(self.download_url, params={"token": session.token}, stream=True)

        if download is None or not download.ok:
            self.size = 0
            self.current_size = None
            self.media_type = MediaType.corrupted
            self._done = True
            database_helper.add_bad_url(self.url)
            self.dump()
            return

        # We copy in chunks so the download rate can be limited. This could also be done with `shutil.copyfileobj(…)`
        with self.path.open("wb") as f:
            while True:
                token = throttler.get(self.path)

                i = 0
                while i < num_tries_download:
                    try:
                        new = download.raw.read(token.num_bytes, decode_content=True)
                        break

                    except Exception:
                        i += 1
                else:
                    break

                if not new:
                    # No file left
                    break

                f.write(new)
                self.current_size += len(new)

        if self.media_type == MediaType.corrupted:
            with self.path.open("wb"):
                # Reopen the file such that previous content is ignored.
                pass

        if is_stream:
            throttler.end_stream()

        download.close()

        # Only register the file after successfully downloading it.
        if self.media_type != MediaType.corrupted:
            if is_testing:
                assert self.size * (1 - perc_diff_for_checksum) <= self.path.stat().st_size <= self.size * (1 + perc_diff_for_checksum), self.path

        self.size = self.path.stat().st_size
        self.checksum = calculate_local_checksum(self.path)
        self.dump()

        # Resolve hard links
        for link in self._links:
            if is_testing:
                assert link.size == self.size
                assert link._links == []

            link.current_size = self.current_size
            link.media_type = self.media_type
            link.checksum = self.checksum

            link.path.unlink(missing_ok=True)
            os.link(self.path, link.path)
            link.dump()
            link._done = True

        self._newly_downloaded = True
        self._done = True


class Course:
    displayname: str
    _name: str
    name: str
    course_id: int

    __slots__ = tuple(__annotations__)  # type: ignore

    def __init__(self, displayname: str, _name: str, name: str, course_id: int) -> None:
        self.displayname = displayname
        self._name = _name
        self.name = name
        self.course_id = course_id

    @classmethod
    def from_dict(cls, info: Dict[str, Any]) -> Course:
        displayname = cast(str, info["displayname"])
        _name = cast(str, info["shortname"] or info["displayname"])
        id = cast(int, info["id"])

        if config.renamed_courses is None:
            name = _name
        else:
            name = config.renamed_courses.get(id, "") or _name

        obj = cls(sanitize_name(displayname, True), _name, sanitize_name(name, True), id)
        obj.make_directories()

        return obj

    def make_directories(self) -> None:
        from isisdl.backend.config import was_in_configuration

        if was_in_configuration is False and self.ok:
            os.makedirs(self.path(), exist_ok=True)

            if config.make_subdirs:
                for item in MediaType.list_dirs():
                    os.makedirs(self.path(item), exist_ok=True)

    def download_videos(self, s: SessionWithKey) -> List[PreMediaContainer]:
        if config.download_videos is False:
            return []

        url = "https://isis.tu-berlin.de/lib/ajax/service.php"
        # Thank you isia-tub for this data <3
        video_data = [{
            "methodname": "mod_videoservice_get_videos",
            "args": {"courseid": self.course_id}
        }]

        videos_res = s.get_(url, params={"sesskey": s.key}, json=video_data)

        if videos_res is None or not videos_res.ok:
            return []

        videos_json = videos_res.json()[0]

        if videos_json["error"]:
            return []

        videos_json = videos_json["data"]["videos"]
        video_urls = [item["url"] for item in videos_json]
        video_names = [item["title"].strip() + item["fileext"] for item in videos_json]

        return [PreMediaContainer(url, self, MediaType.video, name) for url, name in zip(video_urls, video_names)]

    def download_documents(self, helper: RequestHelper) -> List[PreMediaContainer]:
        content = helper.post_REST("core_course_get_contents", {"courseid": self.course_id})
        if content is None or isinstance(content, dict) and "exception" in content:
            return []

        content = cast(List[Dict[str, Any]], content)
        all_content: List[PreMediaContainer] = []

        for week in content:
            if "modules" not in week:
                continue

            module: Dict[str, Any]
            for module in week["modules"]:
                # Check if the description contains url's to be followed
                if "description" in module:
                    links = url_finder.findall(module["description"])
                    for link in links:
                        parse = urlparse(link)
                        if parse.scheme and parse.netloc and config.follow_links and extern_ignore.match(link) is None and isis_ignore.match(link) is None:
                            all_content.append(PreMediaContainer(link, self, MediaType.extern, None))

                if "url" not in module:
                    continue

                url: str = module["url"]
                ignore = isis_ignore.match(url)

                if ignore is not None:
                    # Blacklist hit
                    continue

                is_no_download = re.match(".*mod/(?:folder|resource|url)/.*", url) is None
                if is_no_download:
                    # No blacklist match
                    logger.assert_fail(f"""re.match(".*mod/(?:folder|resource|url)/.*", url) is None\n\nCurrent url: {url}""")

                if "contents" not in module and is_no_download:
                    # Probably the black/white- list didn't match.
                    logger.assert_fail(f'"contents not in file\n\nCurrent url: {url}')
                    continue

                if "contents" in module:
                    for file in module["contents"]:
                        if config.follow_links and "type" in file and file["type"] == "url" and "fileurl" in file and extern_ignore.match(file["fileurl"]) is None and isis_ignore.match(
                                file["fileurl"]) is None:
                            all_content.append(PreMediaContainer(file["fileurl"], self, MediaType.extern))
                        else:
                            all_content.append(PreMediaContainer(file["fileurl"], self, MediaType.document, file["filename"], file["filepath"], file["filesize"], file["timemodified"]))

        return all_content

    def path(self, *args: str) -> Path:
        # Custom path function that prepends the args with the course name.
        return path(sanitize_name(self.name, True), *args)

    @property
    def ok(self) -> bool:
        if config.whitelist is None and config.blacklist is None:
            return True

        if config.whitelist is None and config.blacklist is not None:
            return self.course_id not in config.blacklist

        if config.whitelist is not None and config.blacklist is None:
            return self.course_id in config.whitelist

        if config.whitelist is not None and config.blacklist is not None:
            return self.course_id in config.whitelist and self.course_id not in config.blacklist

        assert False

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.displayname

    def __eq__(self, other: Any) -> bool:
        if other is True:
            return True

        if other.__class__ == self.__class__:
            return bool(self.course_id == other.course_id)

        if isinstance(other, (str, int)):
            return str(self.course_id) == str(other)

        return False

    def __hash__(self) -> int:
        return self.course_id

    def __lt__(self, other: Course) -> bool:
        return self.course_id < other.course_id


class RequestHelper:
    user: User
    session: SessionWithKey
    courses: List[Course]
    _courses: List[Course]
    _meta_info: Dict[str, str]
    course_id_mapping: Dict[int, Course] = {}
    _instance: Optional[RequestHelper] = None
    _instance_init: bool = False

    def __init__(self, user: User, status: Optional[RequestHelperStatus] = None):
        if self._instance_init:
            return

        if status is not None:
            status.set_status(StatusOptions.authenticating)

        self.user = user
        session = SessionWithKey.from_scratch(self.user)

        if session is None:
            print(f"I had a problem getting the user {self.user}. You have probably entered the wrong credentials.\nBailing out…")
            os._exit(1)

        if status is not None:
            status.set_status(StatusOptions.getting_content)

        self.session = session
        self._meta_info = cast(Dict[str, str], self.post_REST("core_webservice_get_site_info"))
        self.get_courses()

        RequestHelper._instance_init = True

    def __new__(cls, user: User, status: Optional[RequestHelperStatus] = None) -> RequestHelper:
        if RequestHelper._instance is None:
            RequestHelper._instance = super().__new__(cls)

        return RequestHelper._instance

    def get_courses(self) -> None:
        _courses = self.post_REST("core_enrol_get_users_courses", {"userid": self._meta_info["userid"]}, use_timeout=False)
        if _courses is None:
            print(f"{error_text} Retrieving the courses failed. Bailing out!")
            os._exit(0)

        courses = cast(List[Dict[str, str]], _courses)
        self.courses = []
        self._courses = []

        for _course in courses:
            course = Course.from_dict(_course)
            RequestHelper.course_id_mapping[course.course_id] = course

            self._courses.append(course)
            if course.ok:
                self.courses.append(course)

        random.shuffle(self.courses)
        random.shuffle(self._courses)

    def make_course_paths(self) -> None:
        for course in self.courses:
            course.make_directories()

    def post_REST(self, function: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None, use_timeout: bool = True) -> Optional[Any]:
        data = data or {}

        data.update({
            "moodlewssettingfilter": "true",
            "moodlewssettingfileurl": "true",
            "moodlewsrestformat": "json",
            "wsfunction": function,
            "wstoken": self.session.token,
        })

        url = "https://isis.tu-berlin.de/webservice/rest/server.php"

        if use_timeout:
            response = self.session.post_(url, data=data, params=params)
        else:
            try:
                response = self.session.post(url, data=data, params=params)
            except Exception:
                response = None

        if response is None or not response.ok:
            return None

        return response.json()

    def download_content(self, status: Optional[RequestHelperStatus] = None) -> Dict[MediaType, List[MediaContainer]]:
        exception_lock = Lock()

        if status is not None:
            status.set_total(len(self.courses))

        if enable_multithread:
            with ThreadPoolExecutor(discover_num_threads) as ex:
                _mod_assign = ex.map(self._download_mod_assign, [0])
                _document_containers = ex.map(self._download_documents, self.courses, repeat(exception_lock))
                _video_containers = ex.map(self._download_videos, self.courses, repeat(exception_lock), repeat(status))

        else:
            _mod_assign = iter([self._download_mod_assign()])
            _document_containers = iter([self._download_documents(course, exception_lock) for course in self.courses])
            _video_containers = iter([self._download_videos(course, exception_lock, status) for course in self.courses])

        pre_containers = [item for row in chain(_document_containers, _video_containers, _mod_assign) for item in row]
        pre_containers = list({f"{item.course} {item.url}": item for item in pre_containers}.values())
        random.shuffle(pre_containers)

        if (num_cached := sum(pre_container.is_cached for pre_container in pre_containers)) != len(pre_containers):
            if status is not None:
                status.set_total(len([item for item in pre_containers if not item.is_ready]))
                status.count = num_cached
                status.set_build_cache_files(pre_containers)
                status.set_status(StatusOptions.building_cache)
                status._eta_start_time = datetime.now()

            # Only multithread if there are actual requests going to be made.
            if enable_multithread:
                with ThreadPoolExecutor(discover_num_threads) as ex:
                    _containers = list(ex.map(MediaContainer.from_pre_container, pre_containers, repeat(self.session), repeat(status)))
            else:
                _containers = [MediaContainer.from_pre_container(pre_container, self.session, status) for pre_container in pre_containers]

        else:
            _containers = [MediaContainer.from_pre_container(pre_container, self.session, None) for pre_container in pre_containers]

        containers = check_for_conflicts_in_files([item for item in _containers if item is not None])
        mapping: Dict[MediaType, List[MediaContainer]] = {typ: [] for typ in MediaType}

        for container in containers:
            mapping[container.media_type].append(container)

        return {typ: sorted(item, key=lambda x: x.time, reverse=True) for typ, item in mapping.items()}

    def _download_mod_assign(self, _: Any = None) -> List[PreMediaContainer]:
        all_content = []
        _assignments = self.post_REST("mod_assign_get_assignments", use_timeout=False)
        if _assignments is None:
            return []

        assignments = cast(Dict[str, Any], _assignments)

        allowed_ids = {item.course_id for item in self.courses}
        for _course in assignments["courses"]:
            if _course["id"] in allowed_ids:
                for assignment in _course["assignments"]:
                    if "introattachments" not in assignment:
                        continue

                    for file in assignment["introattachments"]:
                        file["filepath"] = assignment["name"]
                        all_content.append(PreMediaContainer(file["fileurl"], RequestHelper.course_id_mapping[_course["id"]], MediaType.document,
                                                             file["filename"], file["filepath"], file["filesize"], file["timemodified"]))

        return all_content

    def _download_documents(self, course: Course, exception_lock: Lock) -> List[PreMediaContainer]:
        try:
            return course.download_documents(self)

        except Exception as ex:
            with exception_lock:
                generate_error_message(ex)

    def _download_videos(self, course: Course, exception_lock: Lock, status: Optional[RequestHelperStatus] = None) -> List[PreMediaContainer]:
        try:
            return course.download_videos(self.session)

        except Exception as ex:
            with exception_lock:
                generate_error_message(ex)

        finally:
            if status is not None:
                status.done()


def check_for_conflicts_in_files(files: List[MediaContainer]) -> List[MediaContainer]:
    final_list: List[MediaContainer] = []
    new_files: List[MediaContainer] = []

    file: MediaContainer
    for file in files:
        if file.media_type == MediaType.corrupted:
            final_list.append(file)
        else:
            new_files.append(file)

    files = new_files

    # First check for the same urls across the entire list
    hard_link_conflicts: DefaultDict[str, List[MediaContainer]] = defaultdict(list)

    for file in {file.path: file for file in files}.values():
        hard_link_conflicts[file.download_url].append(file)

    for conflict in hard_link_conflicts.values():
        if len(conflict) != 1:
            conflict.sort(key=lambda x: x.time)
            conflict[0]._links.extend(conflict[1:])
            final_list.append(conflict[0])
            for item in conflict[0]._links:
                files.remove(item)

    # Now check for files with the same size in each course
    hard_link_conflicts = defaultdict(list)

    for file in {file.path: file for file in files}.values():
        hard_link_conflicts[f"{file.course.course_id} {file._name} {file.size}"].append(file)

    for conflict in hard_link_conflicts.values():
        if len(conflict) != 1:
            conflict.sort(key=lambda x: x.time)
            conflict[0]._links.extend(conflict[1:])
            final_list.append(conflict[0])
            for item in conflict[0]._links:
                files.remove(item)

    conflicts: DefaultDict[Path, List[MediaContainer]] = defaultdict(list)
    for file in set(files):
        conflicts[file.path].append(file)

    for typ, conflict in conflicts.items():
        conflict.sort(key=lambda x: x.time)

        if len(conflict) == 1:
            # Only same sizes
            final_list.append(conflict[0])

        elif all(item.size == conflict[0].size for item in conflict):
            final_list.append(conflict[0])

        elif len(set(item.size for item in conflict)) == len(conflict):
            # Only unique sizes
            for i, file in enumerate(conflict):
                basename, ext = os.path.splitext(file._name)
                file._name = basename + f".{i}" + ext
                file.path = file.path.parent.joinpath(sanitize_name(file._name, False))
                file.dump()
                final_list.append(file)

        else:
            logger.assert_fail(f"conflict: {[{x: getattr(item, x) for x in item.__slots__} for item in conflict]}")
            continue

    return final_list


class Downloader(Thread):
    q: Queue[MediaContainer]
    ret_q: Queue[int]
    thread_id: int
    status: DownloadStatus
    throttler: DownloadThrottler
    session: SessionWithKey

    is_downloading: bool = False
    _lock = Lock()

    def __init__(self, q: Queue[MediaContainer], ret_q: Queue[int], thread_id: int, status: DownloadStatus, throttler: DownloadThrottler, session: SessionWithKey):
        self.q = q
        self.ret_q = ret_q
        self.thread_id = thread_id
        self.status = status
        self.throttler = throttler
        self.session = session

        super().__init__(daemon=True)
        self.start()

    def run(self) -> None:
        try:
            while True:
                file = self.q.get()
                self.is_downloading = True
                self.status.add_container(self.thread_id, file)

                file.download(self.throttler, self.session)
                self.status.done(self.thread_id, file)
                self.is_downloading = False
                self.ret_q.put(self.thread_id)

        except Exception as ex:
            with self._lock:
                generate_error_message(ex)


class BandwidthWatcher(Thread):
    throttler: DownloadThrottler
    num_threads: int
    bandwidths: Dict[int, Tuple[int, float]]

    def __init__(self, throttler: DownloadThrottler, num_threads: int, bandwidths: Dict[int, Tuple[int, float]]) -> None:
        self.throttler = throttler
        self.num_threads = num_threads
        self.bandwidths = bandwidths

        super().__init__(daemon=True)
        self.start()

    def run(self) -> None:
        while True:
            num_samples, old_bw = self.bandwidths[self.num_threads]
            if num_samples:
                new_bw = old_bw * (1 - bandwidth_mavg_perc) + self.throttler.bandwidth_used * bandwidth_mavg_perc
                self.bandwidths[self.num_threads] = (num_samples + 1, new_bw)
            else:
                self.bandwidths[self.num_threads] = (1, self.throttler.bandwidth_used)

            pass


class CourseDownloader:
    containers: Dict[MediaType, List[MediaContainer]] = {}
    _did_message: bool = False

    def start(self) -> None:
        user = get_credentials()
        with RequestHelperStatus() as status:
            helper = RequestHelper(user, status)
            containers = helper.download_content(status)
            collapsed_containers = [item for row in containers.values() for item in row]
            collapsed_containers.sort(reverse=True, key=lambda x: x.time)

            for container in collapsed_containers:
                if container.should_download:
                    container.path.open("w").close()

        CourseDownloader.containers = containers

        # Log the metadata
        conf = config.to_dict()
        del conf["password"]

        logger.post({
            "num_g_files": len(collapsed_containers),
            "num_c_files": len(collapsed_containers),

            "total_g_bytes": sum((item.size for item in collapsed_containers)),
            "total_c_bytes": sum((item.size for item in collapsed_containers)),

            "course_ids": sorted([course.course_id for course in helper._courses]),

            "config": conf,
        })

        if not any(item.should_download for row in containers.values() for item in row):
            for row in containers.values():
                for item in row:
                    item._done = True

            logger.done.get()
            self.message_what_did_i_do(collapsed_containers)
            return

        # Make the runner a thread in case of a user needing to exit the program → downloading is done in the main thread
        throttler = DownloadThrottler()
        with DownloadStatus(containers, args.max_num_threads, throttler) as status:
            Thread(target=self.stream_files, args=(containers, throttler, status, helper.session), daemon=True).start()
            if not args.stream:
                downloader = Thread(target=self.download_files, args=(containers, throttler, helper.session, status))
                downloader.start()

            if args.stream:
                while True:
                    time.sleep(65536)

            downloader.join()

        self.message_what_did_i_do(collapsed_containers)

    @staticmethod
    def message_what_did_i_do(collapsed_containers: List[MediaContainer]) -> None:
        if CourseDownloader._did_message:
            return

        CourseDownloader._did_message = True

        if not any(item._newly_downloaded or item._newly_discovered for item in collapsed_containers):
            print("No new files to download ... (cricket sounds)")
            return

        try:
            with path(log_file_location).open() as f:
                prev_msg = f.read()

            now_msg = f"""
===== {datetime.now().strftime(datetime_str)} =====

Running isisdl version {__version__}

Newly downloaded files:

{chr(10).join(item.string_dump() for item in collapsed_containers if item._newly_downloaded) or "None"}


Newly discovered files:

{chr(10).join(item.string_dump() for item in collapsed_containers if item._newly_discovered) or "None"}



"""

            with path(log_file_location).open("w") as f:
                f.write(now_msg)
                f.write(prev_msg)

            if len([item for item in collapsed_containers if item._newly_downloaded or item._newly_discovered]) < 50:
                print("".join(now_msg.splitlines(keepends=True)[4:]))
            else:
                print(f"Downloaded / Discovered too many files to list here. If you are interested please look at\n`{path(log_file_location)}`")

        except OSError:
            pass

    def stream_files(self, files: Dict[MediaType, List[MediaContainer]], throttler: DownloadThrottler, status: DownloadStatus, session: SessionWithKey) -> None:
        if is_windows:
            return

        import pyinotify

        class EventHandler(pyinotify.ProcessEvent):  # type: ignore[misc]
            def __init__(self, files: List[MediaContainer], throttler: DownloadThrottler, session: SessionWithKey, **kwargs: Any):
                self.session = session
                self.throttler = throttler
                self.files: Dict[Path, MediaContainer] = {file.path: file for file in files}

                super().__init__(**kwargs)

            def process_IN_OPEN(self, event: pyinotify.Event) -> None:
                if event.dir:
                    return

                file = self.files.get(Path(event.pathname), None)
                if file is not None and file.current_size is not None:
                    return

                if file is None:
                    return

                if file.current_size is not None:
                    return

                status.add_streaming(file)
                file.download(self.throttler, self.session, True)
                status.done_streaming()

        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, EventHandler([item for row in files.values() for item in row], throttler, session))
        wm.add_watch(str(path()), pyinotify.ALL_EVENTS, rec=True, auto_add=True)

        notifier.loop()

    def download_files(self, files: Dict[MediaType, List[MediaContainer]], throttler: DownloadThrottler, session: SessionWithKey, status: DownloadStatus) -> None:
        # TODO: Dynamic calculation of num threads such that optimal Internet Usage is achieved
        exception_lock = Lock()

        def download(file: MediaContainer) -> None:
            if enable_multithread:
                thread_id = int(current_thread().name.split("T_")[-1])
            else:
                thread_id = 0

            status.add_container(thread_id, file)
            try:
                file.download(throttler, session)
                status.done(thread_id, file)

            except Exception as ex:
                with exception_lock:
                    generate_error_message(ex)

        first_files: List[MediaContainer] = []
        second_files: List[MediaContainer] = []

        for _files in files.values():
            for file in _files:
                if not file.should_download:
                    first_files.append(file)
                else:
                    second_files.append(file)

        if enable_multithread:
            with ThreadPoolExecutor(args.max_num_threads, thread_name_prefix="T") as ex:
                list(ex.map(download, first_files + second_files))
        else:
            for file in first_files + second_files:
                download(file)

        # files_to_download = files[MediaType.document] + files[MediaType.extern] + files[MediaType.video]
        # files_to_download = [file for file in files_to_download if file.should_download]
        #
        # bandwidths: Dict[int, Tuple[int, float]] = {i: (0, 0.0) for i in range(args.max_num_threads)}
        # ret_q: Queue[int] = Queue()
        #
        # if enable_multithread:
        #     threads = [Downloader(Queue(), ret_q, i, status, throttler, session) for i in range(args.max_num_threads)]
        #
        # else:
        #     threads = [Downloader(Queue(), ret_q, 0, status, throttler, session)]
        #
        # max_downloading = args.max_num_threads // 2
        # i = -1
        # num_iter = 2 / status_time
        #
        # while files_to_download:
        #     i += 1
        #
        #     num_dl_threads = sum(thread.is_downloading for thread in threads)
        #
        #
        #     if i == num_iter:
        #         i = 0
        #
        #     if num_dl_threads >= max_downloading:
        #         time.sleep(status_time)
        #         continue
        #
        #     for thread in threads:
        #         if num_dl_threads >= max_downloading:
        #             break
        #
        #         if not thread.is_downloading:
        #             thread.q.put(files_to_download.pop(0))
        #             time.sleep(status_time)
        #             num_dl_threads += 1

    @staticmethod
    @on_kill(2)
    def shutdown_running_downloads(*_: Any) -> None:
        if not CourseDownloader.containers:
            return

        if args.stream:
            return

        for row in CourseDownloader.containers.values():
            for item in row:
                item.stop()

        # Now wait for the downloads to finish
        collapsed_containers = [item for row in CourseDownloader.containers.values() for item in row]

        while not all(item._done for item in collapsed_containers):
            time.sleep(status_time)

        CourseDownloader.message_what_did_i_do(collapsed_containers)


def maybe_create_log_file() -> None:
    if not path(log_file_location).exists():
        with path(log_file_location).open("w") as f:
            containers = [MediaContainer(*item) for item in database_helper._url_container_mapping.values()]
            # When getting the container mapping the media_type will be an integer corresponding to the media type.
            containers = [item for item in containers if item.media_type != MediaType.corrupted.value]  # type: ignore

            f.write(f"===== {datetime.now().strftime(datetime_str)} =====\n\n")
            f.write("Detected that the log file does not exist.\nHere is what I currently have in the database:\n\n")
            f.write("\n".join(item.string_dump() for item in containers))
            f.write("\n\n")


maybe_create_log_file()
