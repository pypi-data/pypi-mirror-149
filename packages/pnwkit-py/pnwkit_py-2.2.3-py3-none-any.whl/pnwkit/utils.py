"""
The MIT License (MIT)

Copyright (c) 2021-present Village

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from . import data

__all__ = (
    "get_int_or_none",
    "get_datetime_or_none",
    "convert_data_array",
    "convert_data_dict",
    "find_data_class",
)

if TYPE_CHECKING:
    from typing import Any, Dict, List, Optional, Union


def get_int_or_none(value: Optional[Any]) -> Optional[int]:
    return None if value is None else int(value)


def get_datetime_or_none(value: Optional[Any]) -> Optional[datetime.datetime]:
    return None if value is None else datetime.datetime.fromisoformat(value)


def convert_data_array(data: List[Any]) -> List[Any]:
    if not data:
        return []
    cls = find_data_class(data[0]["__typename"])
    return [cls.from_data(i) for i in data]


def convert_data_dict(data: Dict[Any, Any]) -> Union[Any, List[Any]]:
    if data["__typename"].endswith("Paginator"):
        return convert_data_array(data["data"])
    return find_data_class(data["__typename"]).from_data(data)


def find_data_class(name: str) -> Any:
    return getattr(data, name)
