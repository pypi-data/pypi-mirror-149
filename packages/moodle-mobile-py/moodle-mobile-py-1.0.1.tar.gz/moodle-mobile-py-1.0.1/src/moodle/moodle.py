from __future__ import annotations

import functools

import aiohttp

from .calendar import MoodleCalendar
from .course import CourseManager
from .siteinfo import SiteInfo


def requires_login(func):
    """
    Decorator for Methods in MoodleCrawler that require the user to be logged in.
    """
    @functools.wraps(func)
    async def wrapper(crawler: MoodleCrawler, *args, **kwargs):
        if not crawler.logged_in:
            raise ValueError("MoodleCrawler must be logged in to use this function")
        return await func(crawler, *args, **kwargs)
    return wrapper


class MoodleCrawler:
    """
    Base Class of the Moodle Crawler.
    """
    def __init__(self, username, password, site_url):
        self._logged_in: bool = False
        self.username: str = username
        self.password: str = password
        self.site_url: str = site_url
        self.site_info: SiteInfo = SiteInfo(self)
        self.courses: CourseManager = CourseManager(self)
        self.token: str = ""
        self.private_token: str = ""

    async def login(self) -> None:
        """
        Tries to login with the specified credentials
        """
        data = {
            "username": self.username,
            "password": self.password,
            "service": "moodle_mobile_app"
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(self.site_url + "/login/token.php", data=data) as r:
                json = await r.json()
        if "token" not in json.keys():
            raise ValueError("login wasn't successful")
        self._logged_in = True
        self.token, self.private_token = json["token"], json["privatetoken"]
        await self._load_modules()

    @requires_login
    async def _load_modules(self) -> None:
        """
        Loads all Modules
        """
        await self.site_info.fetch()
        await self.courses.fetch()

    @property
    def logged_in(self) -> bool:
        """
        Whether the crawler is logged in or not.
        :return:
        """
        return self._logged_in

    @requires_login
    async def fetch_calendar(self, year: int, month: int) -> MoodleCalendar:
        """
        Fetches a Calendar for the specified month
        :param year: the year of the calendar
        :param month: the month of the calendar (1-12)
        :return: the fetched and resolved MoodleCalendar
        """
        c = MoodleCalendar(self, year, month)
        await c.fetch()
        return c

    @requires_login
    async def api_request(self, function: str, path: str = "/webservice/rest/server.php", **kwargs) -> dict:
        """
        Shorthand for making REST function calls to moodle.
        :param function: the function to execute
        :param path: the path where the webservice is running at
        :param kwargs: attributes to include in the post data
        :return: the json response of the server
        """
        data = {
            "moodlewssettingfilter": True,
            "moodlewssettingfileurl": False,
            "wsfunction": function,
            "wstoken": self.token,
            **kwargs
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(self.site_url + path + f"?moodlewsrestformat=json&wsfunction={function}", data=data) as r:
                return await r.json()
