import re


def default_validator(val):
    return val is not None


def not_null_str(val):
    return bool(val and len(val))


def is_email(val):
    return bool(re.match('[^@]+@[^@]+\.[^@]+', val))


def is_nickname(val):
    return bool(re.match('^[a-zA-Z0-9_.]+$', val))
