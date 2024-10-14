import pytest
import os


@pytest.fixture
def rootdir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
