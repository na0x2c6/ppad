import datetime
from dateutil import parser
import pytz
import time


def date_parse(date: str) -> datetime:
    dt = parser.isoparse(date)

    if dt.tzinfo is not None:
        return dt

    default_tz = pytz.timezone(time.tzname[time.daylight])
    return default_tz.localize(dt)
