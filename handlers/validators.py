import re
from urllib.parse import urlparse


# "2020-10-31T20:12:41.233Z"
date_re = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'
# "2021-03-01T03:22:19.081+03:00"
date_with_tz_re = '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}$'


def default_validator(val):
    return val is not None


def not_null_str(val):
    return bool(val and len(val))


def is_email(val):
    return bool(re.match('[^@]+@[^@]+\.[^@]+', val))


def is_nickname(val):
    return bool(re.match('^[a-zA-Z0-9_.]+$', val))


def is_non_negative(val):
    return int(val) > 0


def is_url(val):
    parse_result = urlparse(val)
    return parse_result.scheme == 'https' and parse_result.path and parse_result.netloc


def is_non_digit(val):
    return not re.match('^\d+$', val)


def is_timestamp(val: str):
    return bool(re.match(date_with_tz_re, val) or re.match(date_re, val))


def is_bool_str(val):
    return val == 'true' or val == 'false'
