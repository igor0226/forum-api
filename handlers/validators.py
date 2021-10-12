def default_validator(val):
    return val is not None


def not_null_str(val):
    return bool(val and len(val))
