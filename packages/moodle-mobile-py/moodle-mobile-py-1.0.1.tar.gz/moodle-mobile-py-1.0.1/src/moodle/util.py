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


def filter(seq: Iterable, check_as_dict: bool = False, only_one: bool = True, **kwargs) -> Optional[Union[List[Any], Any]]:
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
