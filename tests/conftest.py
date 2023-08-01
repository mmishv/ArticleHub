import os

import pytest

from common.database import get_database


@pytest.fixture
def enable_test_mode():
    os.environ["TEST_MODE"] = "True"
    yield
    os.environ.pop("TEST_MODE")


@pytest.fixture
def db(enable_test_mode):
    return get_database()
