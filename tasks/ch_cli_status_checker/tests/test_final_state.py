import os
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "check_status.sh")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_is_executable():
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_script_contains_correct_command():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()
    assert "clickhousectl cloud service get" in content, \
        "Script does not contain the expected command 'clickhousectl cloud service get'."

def test_script_redirects_output():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()
    assert "> /home/user/project/status.log" in content or "> status.log" in content or ">> /home/user/project/status.log" in content or ">> status.log" in content, \
        "Script does not redirect output to status.log."
