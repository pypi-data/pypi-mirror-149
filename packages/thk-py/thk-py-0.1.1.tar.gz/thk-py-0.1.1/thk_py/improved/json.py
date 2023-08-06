# -*- coding: utf-8 -*-
import ujson
from typing import Union

_VALID_JSON_TYPE = Union[None, str, int, float, bool, dict, list]


def fast_loads(str_json: str):
    return ujson.loads(str_json)


def fast_dumps(obj: _VALID_JSON_TYPE, ensure_ascii: bool = False) -> str:
    return ujson.dumps(obj, ensure_ascii=ensure_ascii)
