from __future__ import annotations
import os.path
from asyncio.coroutines import iscoroutine
from datetime import datetime
from datetime import timedelta
from operator import attrgetter
from typing import Dict, Any, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .moodle import MoodleCrawler

import aiofiles
import aiohttp


class MoodleResource:
    """
    Represents a Moodle Resource that can have multiple files.
    """

    def __init__(self, moodle: MoodleCrawler, data: Dict[str, Any]):
        self.moodle: MoodleCrawler = moodle

        self.id: int = data["id"]
        self.course_id: int = data["course"]
        self.name: str = data["name"]
        self.content_files: List[ContentFile] = [ContentFile(self.moodle, x) for x in data["contentfiles"]]
        self.revision: int = data["revision"]
        self.modified: datetime = datetime.fromtimestamp(data["timemodified"])

    async def get_latest_file(self) -> ContentFile:
        """
        :return: the last file edited
        """
        return min(self.content_files, key=attrgetter("modified"))


class ContentFile:
    """
    Represents a single file of a Resource
    """

    def __init__(self, moodle: MoodleCrawler, data: Dict[str, Any]):
        self.moodle: MoodleCrawler = moodle

        self.file_name: str = data["filename"]
        self.file_path: str = data["filepath"]
        self.file_url: str = data["fileurl"]
        self.modified: datetime = datetime.fromtimestamp(data["timemodified"])
        self.mimetype: str = data["mimetype"]
        self.is_external: bool = data["isexternalfile"]

    async def download(self, out_steam, binary: bool = True) -> None:
        """
        Downloads this resource and writes it to the specified stream.
        :param out_steam: the stream to write to output to
        :param binary: whether the data should not be decoded
        """
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{self.file_url}?token={self.moodle.token}") as r:
                data = await r.read()
                if not binary:
                    data = data.decode()
                res = out_steam.write(data)
                if iscoroutine(res):
                    await res

    async def save(self, path: str) -> str:
        """
        Downloads and saves this file to the specified directory
        :param path: the directory to save the file at
        :return: the file output file path
        """
        out_path = os.path.join(path, self.file_name)
        async with aiofiles.open(out_path, mode="wb") as f:
            await self.download(f)
        return out_path

    async def get_modification_delta(self) -> timedelta:
        """
        Calculates before what time this file was last modified.
        """
        return datetime.now() - self.modified
