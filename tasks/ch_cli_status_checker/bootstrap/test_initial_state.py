import os
import shutil
import pytest

PROJECT_DIR = "/home/user/project"

def test_clickhouse_client_binary_available():
    assert shutil.which("clickhouse-client") is not None, "clickhouse-client binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
