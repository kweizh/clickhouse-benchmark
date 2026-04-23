import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "async_insert.py")

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup_environment():
    # Start clickhouse-server
    server_process = subprocess.Popen(
        ["clickhouse-server"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(8123):
        import signal
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        pytest.fail("clickhouse-server failed to start on port 8123.")
        
    # Run the user's script
    result = subprocess.run(
        ["python3", SCRIPT_PATH],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    
    if result.returncode != 0:
        import signal
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        pytest.fail(f"User script failed to execute: {result.stderr}")
        
    yield
    
    # Teardown
    import signal
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    server_process.wait(timeout=10)

def test_table_contains_data():
    """Priority 1: Use clickhouse-client to verify the table and data."""
    result = subprocess.run(
        ["clickhouse-client", "--query", "SELECT count() FROM async_table"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to query async_table: {result.stderr}"
    
    count = int(result.stdout.strip())
    assert count >= 5, f"Expected at least 5 rows in async_table, got {count}."

def test_script_uses_async_insert():
    """Priority 3: Verify the script contains the async_insert setting."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
        
    assert "async_insert" in content, "The script does not seem to enable async_insert."
