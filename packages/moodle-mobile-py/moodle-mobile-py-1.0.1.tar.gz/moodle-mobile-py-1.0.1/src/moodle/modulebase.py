from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict, Optional, Any

if TYPE_CHECKING:
    from .moodle import MoodleCrawler
from asyncio import iscoroutinefunction
import functools


def requires_resolved(state="default"):
    """
    When using this as decorator in a method of a MoodleModule, the method can only be used when the given state is resolved.
    :param state: the state that has to be resolved to use this method
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(module: MoodleModule, *args, **kwargs):
            if state not in module._resolve_state:
                raise ValueError(f"{state} is not resolved in {module.__class__.__name__}")
            return await func(module, *args, **kwargs)
        return wrapper
    return decorator


class MoodleModule:
    """
    Base Class for all Moodle Modules.
    Manages resolving states.
    """

    _IGNORE_FIELDS: List[str] = ["__class__", "_resolve_state", "IGNORE_FIELDS", "moodle", "ALL"]
    IGNORE_FIELDS: Dict[str, List[str]] = {}
    ALL: List[str] = []

    @classmethod
    def get_all(cls) -> List[str]:
        """
        used to get all attributes specified in MoodleModule#IGNORE_FIELDS and MoodleModule#_IGNORE_FIELDS.
        When a attribute is not in this list, it is only accessible when the "default" state is resolved.
        :return: a list of all specified attributes
        """
        cls.ALL = cls._IGNORE_FIELDS[:]
        for state in cls.IGNORE_FIELDS.values():
            cls.ALL.extend(state)
        return cls.ALL

    def __init__(self, moodle: MoodleCrawler):
        self._resolve_state = []
        self.moodle = moodle

    def _set_resolved(self, state="default") -> None:
        """
        Resolves a specified state.
        Should only be called inside a Subclass of MoodleModule.
        :param state: the state to set resolved
        """
        if state not in self._resolve_state:
            self._resolve_state.append(state)

    async def fetch(self) -> None:
        """
        Default Fetching Method of this Module
        :return:
        """
        pass

    def __getattribute__(self, item) -> Optional[Any]:
        """
        Makes attributes only accessible when their state is resolved.
        """
        value = object.__getattribute__(self, item)
        if callable(value) or iscoroutinefunction(value):
            return value
        if item not in MoodleModule._IGNORE_FIELDS:
            all_ = self.ALL if len(self.ALL) > 0 else self.get_all()
            if item not in all_:
                return value
            # handle defined attributes
            for k, v in self.IGNORE_FIELDS.items():
                if k not in self._resolve_state and k != "default":
                    raise ValueError(f"\"{item}\" on {self.__class__.__name__} is not resolved")
                if item in v:
                    return value
            if "default" not in self._resolve_state and item not in all_:
                raise ValueError(f"\"{item}\" on {self.__class__.__name__} is not resolved")
        return value
