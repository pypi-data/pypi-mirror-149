import typing
from typing import Union, List, Any, Optional, Iterable


def check(obj: Union[object, dict], check_as_dict: bool, **kwargs) -> bool:
    """
    checks a specific object for attributes
    :param obj: the object to check
    :param check_as_dict: whether the values should be accessed as values of a dict or attributes of an object
    :param kwargs: the attributes to check
    :return: whether the query matches this object
    """
    for k, v in kwargs.items():
        if check_as_dict:
            if obj[k] != v:
                return False
        else:
            if getattr(obj, k) != v:
                return False
    return True


T = typing.TypeVar("T")


def filter(seq: Iterable[T], check_as_dict: bool = False, only_one: bool = False, **kwargs) -> Optional[Union[List[T], T]]:
    """
    Filters an iterable for items with specified attributes.

    :param seq: The sequence to filter
    :param check_as_dict: whether the attributes of the objects should be accessed as values of a dict or attributes of an object
    :param only_one: whether only one object or a list of all matching objects should be returned.
    :param kwargs: the attributes to check
    :return: Depending on only_one
    """
    out = []
    for item in seq:
        if check(item, check_as_dict, **kwargs):
            if only_one:
                return item
            else:
                out.append(item)
    return None if only_one else out


def find(seq: Iterable[T], check_as_dict: bool = False, **kwargs) -> Optional[T]:
    """
    Searches an iterable for an item with the specified attributes.
    Like filter() except it only searches one item.

    :param seq: The sequence to search
    :param check_as_dict: whether the attributes of the objects should be accessed as values of a dict or attributes of an object
    :param kwargs: the attributes to check
    :return: The found item or None if none found
    """
    return filter(seq, check_as_dict=check_as_dict, only_one=True, **kwargs)
