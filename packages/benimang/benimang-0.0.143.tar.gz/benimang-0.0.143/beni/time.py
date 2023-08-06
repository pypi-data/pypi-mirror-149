import datetime
import time

_DEFAULT_FMT = '%Y-%m-%d %H:%M:%S'


def timestamp_bystr(value: str, fmt: str = _DEFAULT_FMT):
    return time.mktime(time.strptime(value, fmt))


def timestamp_tostr(timestamp: float | None, fmt: str = _DEFAULT_FMT):
    timestamp = timestamp or time.time()
    ary = time.localtime(timestamp)
    return time.strftime(fmt, ary)


def date(date_str: str, fmt: str = '%Y-%m-%d'):
    return datetime.datetime.strptime(date_str, fmt).date()
