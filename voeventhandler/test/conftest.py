import pytest
import textwrap
from pathlib import Path

@pytest.fixture
def notice_str(request):
    notice_path = Path(__file__).parent / "notices" / request.param
    with open(notice_path, "r") as f:
        notice = f.read()
    return textwrap.dedent(notice).strip().encode('UTF-8')

@pytest.fixture
def config():
    return Path(__file__).parent / "conf" / "config.json"

@pytest.fixture
def clean_database():
    pass