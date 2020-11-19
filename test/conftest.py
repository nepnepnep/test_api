import pytest
from api.auth.auth import Auth



@pytest.fixture()
def auth_header():
    auth_header = Auth().get_auth_header('testlogin123','testlogin123')
    yield auth_header