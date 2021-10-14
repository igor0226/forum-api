import re
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
