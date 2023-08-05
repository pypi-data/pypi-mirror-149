from __future__ import annotations

from datetime import datetime

from .modulebase import MoodleModule, requires_resolved
from .resources import MoodleResource
from .util import filter
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .moodle import MoodleCrawler


class CourseManager(MoodleModule):
    def __init__(self, moodle: MoodleCrawler):
        super(CourseManager, self).__init__(moodle)
        self.courses: Optional[List[MoodleCourse]] = None

    async def fetch(self):
        """
        Fetches the Course Overview of the current Moodle Account.
        After calling this, CourseManager#courses is accessible.
        """
        json = await self.moodle.api_request("core_enrol_get_users_courses", userid=self.moodle.site_info.user_id,
                                             returnusercount=1)
        self.courses = []
        self._set_resolved()
        for course in json:
            self.courses.append(MoodleCourse(self.moodle, course))


class MoodleCourse(MoodleModule):
    IGNORE_FIELDS = {"default": ["id"],
                     "init": ["short_name", "full_name", "display_name", "id_number", "visible",
                              "summary", "summary_format", "format", "show_grades", "language",
                              "category", "progress", "completed", "start_date", "end_date", "marker",
                              "last_access", "overview_files"],
                     "resources": ["resources"]}

    def __init__(self, moodle, data):
        super(MoodleCourse, self).__init__(moodle)
        self.id: int = data["id"]
        try:
            self.short_name: str = data["shortname"]
            self.full_name: str = data["fullname"]
            self.display_name: str = data["displayname"]
            self.id_number = data["idnumber"]
            self.visible: bool = data["visible"]
            self.summary: str = data["summary"]
            self.summary_format: int = data["summaryformat"]
            self.format = data["format"]
            self.show_grades: bool = data["showgrades"]
            self.language: str = data["lang"]
            self.category: int = data["category"]
            self.progress = data["progress"]
            self.completed = data["completed"]
            self.start_date: datetime = datetime.fromtimestamp(data["startdate"])
            self.end_date: datetime = None if data["enddate"] == 0 else datetime.fromtimestamp(data["enddate"])
            self.marker = data["marker"]
            self.last_access: Optional[datetime] = datetime.fromtimestamp(data["lastaccess"]) if data["lastaccess"] else None
            self.overview_files: List[dict] = data["overviewfiles"]
            self._set_resolved("init")
        except KeyError:
            pass

        self.data: Optional[dict] = None
        self.resources: Optional[List[MoodleResource]] = None

    def __repr__(self) -> str:
        return f"MoodleCourse[id={self.id}, display_name=\"{self.display_name}\"]"

    async def fetch(self) -> None:
        data = {
            "options[0][name]": "excludemodules",
            "options[0][value]": 0,
            "options[1][name]": "excludecontents",
            "options[1][value]": 1,
            "options[2][name]": "includestealthmodules",
            "options[2][value]": 0
        }
        json = await self.moodle.api_request("core_course_get_contents", courseid=self.id, **data)
        self.data = json
        self._set_resolved()

    async def fetch_resources(self) -> None:
        json = await self.moodle.api_request("mod_resource_get_resources_by_courses", **{"courseids[0]": 14})
        self.resources = []
        self._set_resolved("resources")
        for res in json["resources"]:
            self.resources.append(MoodleResource(self.moodle, res))

    @requires_resolved("resources")
    async def get_resource(self, id_) -> MoodleResource:
        return filter(self.resources, id=id_)
