from __future__ import print_function

import logging
from datetime import datetime, timedelta


def to_isostring(dt):
    """
    Converts the given datetime to an ISO String.
    This assumes the datetime is UTC.
    """
    if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) > timedelta(0):
        logging.warn("Warning: aware datetimes are interpreted as if they were naive")

    # -3 to change microseconds to milliseconds
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def parse_isostring(isostring):
    """
    Parse the ISO String to a native ``datetime``.
    """
    if not isostring:
        return None
    return datetime.strptime(isostring.replace("Z", "GMT"), "%Y-%m-%dT%H:%M:%S.%f%Z")
