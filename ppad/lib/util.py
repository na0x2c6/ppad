import datetime
from dateutil import parser
import pytz
import time


def parse_date(date: str) -> datetime:
    dt = parser.isoparse(date)

    if dt.tzinfo is not None:
        return dt

    default_tz = pytz.timezone(time.tzname[time.daylight])
    return default_tz.localize(dt)


def parse_argv(argv: list[str]) -> tuple[datetime, datetime]:
    if len(argv) == 1:
        return None, None

    date_to: datetime = None
    date_from: datetime = None
    from_str: str
    to_str: str

    span = argv[1].split('~')
    if len(span) == 1:
        from_str = to_str = span[0]
    else:
        [from_str, to_str, *_] = span

    if from_str:
        date_from = parse_date(from_str)

    if to_str:
        date_to = parse_date(to_str)

    if date_from is None and date_to is None:
        # probably `argv` would be only character '~'
        return None, None

    if date_from == date_to:
        date_to = date_to + datetime.timedelta(days=1)

    return date_from, date_to
