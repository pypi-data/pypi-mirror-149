""""""
# Standard library imports
from typing import Optional, Any, Union

# Third party imports
import datetime

# Local imports


def timedelta_nice_format(td_object : Optional[datetime.timedelta]) -> str:
    """Create string with nice formatted time duration"""
    if td_object is None:
        return "None"
    seconds = int(td_object.total_seconds())
    return seconds_nice_format(seconds)


def seconds_nice_format(seconds : Union[int, float]) -> str:
    """Create string with nice formatted time duration in seconds"""
    if seconds == 0:
        return "0 seconds"
    periods = [
        ('year', 60*60*24*365),
        ('month', 60*60*24*30),
        ('day', 60*60*24),
        ('hour', 60*60),
        ('minute', 60),
        ('second', 1)
    ]
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)
