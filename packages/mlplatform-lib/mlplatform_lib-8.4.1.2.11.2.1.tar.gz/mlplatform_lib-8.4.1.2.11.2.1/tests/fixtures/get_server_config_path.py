import os
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def get_server_config_path(request):
    cur_test_file_path = Path(request.fspath).parent
    return os.path.join(cur_test_file_path, "config", "server_config.yaml")
