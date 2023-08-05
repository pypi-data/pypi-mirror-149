from datetime import datetime, timedelta

from dateutil import parser


def utc_now():
    """Don't keep timezone"""
    return datetime.utcnow()


def utc_delta(
    *,
    days: int | None = None,
    hours: int | None = None,
    minutes: int | None = None,
    seconds: int | None = None,
):
    params = {}
    if days:
        params["days"] = days
    if hours:
        params["hours"] = hours
    if minutes:
        params["minutes"] = minutes
    if seconds:
        params["seconds"] = seconds
    return datetime.utcnow() + timedelta(**params)


def parse_date(value: str, ignoretz=False) -> datetime:
    return parser.parse(value, ignoretz=ignoretz)
