from datetime import UTC, datetime


def get_utc_now():
    return datetime.now(UTC)
