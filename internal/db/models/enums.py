from enum import Enum


class TimeInterval(Enum):
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"


class TimeIntervalPatterns(Enum):
    FULL = "%Y-%m-%dT%H:%M:%S"
    HOUR = "%Y-%m-%dT%H"
    DAY = "%Y-%m-%d"
    MONTH = "%Y-%m"
