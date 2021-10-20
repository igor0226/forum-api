import re
from datetime import datetime
from urllib.parse import urlparse


def default_validator(val):
    return val is not None


def not_null_str(val):
    return bool(val and len(val))


def is_email(val):
    return bool(re.match('[^@]+@[^@]+\.[^@]+', val))


def is_nickname(val):
    return bool(re.match('^[a-zA-Z0-9_.]+$', val))


def is_non_negative(val):
    return val > 0


def is_url(val):
    parse_result = urlparse(val)
    return parse_result.scheme == 'https' and parse_result.path and parse_result.netloc


def is_non_digit(val):
    return not re.match('^\d+$', val)


# "2021-03-01T03:22:19.081+03:00"
def is_timestamp(val: str):
    try:
        timestamp = ''.join(val.rsplit(':', 1))
        return bool(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z'))
    except ValueError:
        return False
