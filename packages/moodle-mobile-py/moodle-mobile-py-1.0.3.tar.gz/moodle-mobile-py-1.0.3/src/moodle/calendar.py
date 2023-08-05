from __future__ import annotations

from .modulebase import MoodleModule
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .moodle import MoodleCrawler


class MoodleCalendar(MoodleModule):
    """
    Class that represents the Moodle Calendar and its Events.
    """
    IGNORE_FIELDS = {"default": ["year", "month"]}

    def __init__(self, moodle: MoodleCrawler, year: int, month: int):
        """
        :param moodle: the main moodle class
        :param year: the year that should be fetched
        :param month: the month that should be fetched
        """
        super(MoodleCalendar, self).__init__(moodle)
        self.year: int = year
        self.month: int = month
        self.data: Optional[dict] = None

    async def fetch(self):
        """
        Fetches the Calendar for the current moodle account.
        After calling this MoodleCalendar#data can be accessed.
        """
        json = await self.moodle.api_request("core_calendar_get_calendar_monthly_view", year=self.year, month=self.month, mini=1)
        self.data = json
        self._set_resolved()
