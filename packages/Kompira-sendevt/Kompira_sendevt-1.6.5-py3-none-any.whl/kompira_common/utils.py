# -*- coding: utf-8 -*-
import pytz
import sys
from contextlib import contextmanager
from datetime import datetime

BASE_DATETIME = datetime(2020, 1, 1)


@contextmanager
def redirect_stdio(stdout, stderr):
    _stdout = sys.stdout
    _stderr = sys.stderr
    sys.stdout = stdout
    sys.stderr = stderr
    try:
        yield
    finally:
        sys.stdout = _stdout
        sys.stderr = _stderr


def system_timezone():
    dt_aware = BASE_DATETIME.astimezone()
    tzname = dt_aware.tzname()
    for tz in pytz.all_timezones:
        if tzname == pytz.timezone(tz).tzname(BASE_DATETIME):
            return tz
    return 'UTC'
