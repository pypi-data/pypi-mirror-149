from __future__ import annotations

from .modulebase import MoodleModule


class SiteInfo(MoodleModule):
    """
    Includes all important config values for moodle
    """
    def __init__(self, moodle):
        super(SiteInfo, self).__init__(moodle)
        self.site_name: str = ""
        self.first_name: str = ""
        self.last_name: str = ""
        self.language: str = ""
        self.user_id: int = 0
        self.private_access_key: str = ""
        self.is_admin: bool = False
        self.functions: list = []

    async def fetch(self) -> None:
        json = await self.moodle.api_request("core_webservice_get_site_info")
        self.site_name = json["sitename"]
        self.first_name = json["firstname"]
        self.last_name = json["lastname"]
        self.language = json["lang"]
        self.user_id = json["userid"]
        self.private_access_key = json["userprivateaccesskey"]
        self.is_admin = json["userissiteadmin"]
        self.functions = json["functions"]
        self._set_resolved()
