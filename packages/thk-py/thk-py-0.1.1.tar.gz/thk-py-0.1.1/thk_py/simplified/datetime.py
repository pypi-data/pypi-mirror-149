# -*- coding: utf-8 -*-
from typing import Iterator
from copy import deepcopy
from datetime import datetime, date, timedelta


STANDARD_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
STANDARD_DATE_FORMAT = '%Y-%m-%d'


def datetime2str(target_datetime: datetime, str_format: str = STANDARD_DATETIME_FORMAT) -> str:
    return target_datetime.strftime(str_format)


def str2datetime(str_datetime: str, str_format: str = STANDARD_DATETIME_FORMAT) -> datetime:
    return datetime.strptime(str_datetime, str_format)


def date2str(target_date: date, str_format: str = STANDARD_DATE_FORMAT) -> str:
    return target_date.strftime(str_format)


def str2date(str_date: str, str_format: str = STANDARD_DATE_FORMAT) -> date:
    return datetime.strptime(str_date, str_format).date()


def timestamp2datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)


def datetime2timestamp(target_datetime: datetime) -> int:
    return int(target_datetime.timestamp())


def date_range(first_date: date, last_date: date) -> Iterator[date]:
    current_date = deepcopy(first_date)
    while current_date <= last_date:
        yield current_date
        current_date += timedelta(days=1)


def date_range_reversed(last_date: date, first_date: date) -> Iterator[date]:
    current_date = deepcopy(last_date)
    while current_date >= first_date:
        yield current_date
        current_date -= timedelta(days=1)


def build_first_datetime(day: date = None) -> datetime:
    if day is None:
        day = date.today()

    return datetime.combine(day, datetime.min.time())


def build_last_datetime(day: date = None):
    if day is None:
        day = date.today()

    return datetime.combine(day, datetime.max.time())
