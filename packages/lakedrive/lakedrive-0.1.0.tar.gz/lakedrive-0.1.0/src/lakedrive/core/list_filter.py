from functools import partial
import re
import operator
from datetime import datetime, timedelta
from typing import Callable, List, Tuple

from .objects import FileObject


def split_by_comma(line: str) -> List[str]:
    """Split a string by comma into a list,
    - exclude comma between double-quotes
    - remove any leading and trailing spaces"""
    return [kv.strip(" ") for kv in re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)]


def split_key_value(kv_string: str) -> Tuple[str, str]:
    """Split a string like key=value into (key, value) tuple
    - ensure key is always lowercased
    - value can contain the "=" char, i.e. only split on first occurrence of "="
    """
    key, value = kv_string.split("=", 1)
    return (key.lower(), value)


BYTE_UNITS = {
    "b": 1,
    "k": 1024,
    "M": 1024 ** 2,
    "G": 1024 ** 3,
    "T": 1024 ** 4,
    "P": 1024 ** 5,
}

COMPARE_OPERATORS = {
    "+": operator.gt,
    "-": operator.le,
}

# follow pattern used by GNU date
TIME_UNITS = {
    "S": "seconds",
    "M": "minutes",
    "H": "hours",
    "d": "days",
    "w": "weeks",
}


def filter_by_name(value_str: str, file_objects: List[FileObject]) -> List[FileObject]:
    if value_str[0] == "*":
        value_str = "." + value_str
    pattern = re.compile(value_str)
    return [obj for obj in file_objects if pattern.match(obj.name)]


def filter_by_size(value_str: str, file_objects: List[FileObject]) -> List[FileObject]:
    unit_key = value_str[-1]
    operator_key = value_str[0]

    if operator_key in COMPARE_OPERATORS:
        value_str = value_str[1:]
        operator_func = COMPARE_OPERATORS[operator_key]
    else:
        operator_func = operator.eq

    if unit_key in BYTE_UNITS:
        compare_value = int(value_str[0:-1]) * BYTE_UNITS[unit_key]
    else:
        compare_value = int(value_str)

    return [
        obj for obj in file_objects if operator_func(obj.bytes, compare_value) is True
    ]


def filter_by_mtime(value_str: str, file_objects: List[FileObject]) -> List[FileObject]:

    unit_key = value_str[-1]
    operator_key = value_str[0]

    if operator_key in COMPARE_OPERATORS:
        value_str = value_str[1:]
        operator_func = COMPARE_OPERATORS[operator_key]
    else:
        operator_func = operator.le

    if unit_key in TIME_UNITS:
        diff_value = int(value_str[0:-1])
        time_unit = TIME_UNITS[unit_key]
    else:
        diff_value = int(value_str)
        time_unit = "seconds"

    point_in_time = int(
        (datetime.now() - timedelta(**{time_unit: diff_value})).timestamp()
    )
    return [
        obj for obj in file_objects if operator_func(point_in_time, obj.mtime) is True
    ]


FILTER_FUNCTIONS = {
    "name": filter_by_name,
    "size": filter_by_size,
    "mtime": filter_by_mtime,
}


def parse_filter_string(filter_str: str) -> List[Callable]:

    filters = []
    for kv_string in split_by_comma(filter_str):
        key, value = split_key_value(kv_string)
        filter_function = FILTER_FUNCTIONS.get(key, None)
        if filter_function is None:
            continue
        filters.append(partial(filter_function, value))
    return filters


def apply_search_filters(
    filters: List[Callable], file_objects: List[FileObject]
) -> List[FileObject]:

    filtered = file_objects
    for filter_function in filters:
        filtered = filter_function(filtered)
    return filtered


def apply_search_filter_str(
    filter_str: str, file_objects: List[FileObject]
) -> List[FileObject]:
    return apply_search_filters(parse_filter_string(filter_str), file_objects)
