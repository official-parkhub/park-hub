import pytest


class _RC:
    def __init__(self, db):
        self.db = db


@pytest.fixture
async def rc(db):
    return _RC(db)
