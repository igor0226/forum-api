from pytz import timezone
from datetime import datetime


def get_pg_timestamp():
    timestamp_with_tz = datetime.now(timezone("Europe/Moscow")).strftime(
        '%Y-%m-%dT%H:%M:%S.%f%z'
    )
    timestamp_with_tz = timestamp_with_tz[:-2:] + ':' + timestamp_with_tz[-2::]
    timestamp_with_tz = timestamp_with_tz[:23:] + timestamp_with_tz[26::]
    return timestamp_with_tz


def serialize_pg_timestamp(timestamp):
    if not timestamp:
        return ''

    created = str(timestamp)
    separator = created[19]

    if separator == '+':
        created = created[:19:] + '.000000' + created[19::]
    
    created = created[:10:] + 'T' + created[11::]
    created = created[:-9:] + 'Z'

    return created


def make_kv_list(**kwargs):
    conditions = []

    for key, value in kwargs.items():
        if not value:
            continue

        conditions.append({
            'key': key,
            'value': value,
        })

    return conditions


def get_first_defined(val1, val2):
    return val1 if val1 is not None else val2


def is_str(val):
    return isinstance(val, str)
