import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/dashboard"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_endpoint(start_app):
    """Test that the API endpoint returns data."""
    import urllib.request
    import json
    
    try:
        req = urllib.request.Request("http://localhost:3000/api/metrics")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            assert isinstance(data, list), "Expected a JSON array of metrics"
            assert len(data) > 0, "Expected at least one metric"
    except Exception as e:
        pytest.fail(f"Failed to fetch from API endpoint: {e}")

def test_web_ui(start_app):
    reason = "The application should display a web page with system metrics fetched from the ClickHouse database."
    truth = "Navigate to http://localhost:3000. Verify that the page loads successfully. Verify that the page displays a list or table of system metrics (e.g., metric names and their values)."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_web_ui"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
