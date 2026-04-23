import os
import shutil
import pytest

PROJECT_DIR = "/home/user/app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found in {PROJECT_DIR}."

def test_next_config_exists():
    next_config_path = os.path.join(PROJECT_DIR, "next.config.mjs")
    fallback_path = os.path.join(PROJECT_DIR, "next.config.js")
    assert os.path.isfile(next_config_path) or os.path.isfile(fallback_path), f"Next.js config not found in {PROJECT_DIR}."
