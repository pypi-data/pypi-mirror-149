import pytest
import os

@pytest.fixture(scope="session")
def data_path(tmp_path_factory):
    data = tmp_path_factory.mktemp("data")
    os.chdir(data)
    return data
