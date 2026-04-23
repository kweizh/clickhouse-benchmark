import os
import clickhouse_connect
import pytest

def get_client():
    host = os.environ.get("CLICKHOUSE_HOST")
    password = os.environ.get("CLICKHOUSE_PASSWORD")
    port = int(os.environ.get("CLICKHOUSE_PORT", "8443"))
    user = os.environ.get("CLICKHOUSE_USER", "default")
    
    assert host is not None, "CLICKHOUSE_HOST environment variable not set"
    assert password is not None, "CLICKHOUSE_PASSWORD environment variable not set"
    
    return clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        secure=True
    )

def test_users_table_exists():
    client = get_client()
    result = client.query("SHOW TABLES LIKE 'users'")
    assert len(result.result_rows) > 0, "Table 'users' does not exist."

def test_email_column_exists():
    client = get_client()
    result = client.query("SELECT name FROM system.columns WHERE table = 'users' AND name = 'email'")
    assert len(result.result_rows) > 0, "Column 'email' does not exist in 'users' table."

def test_data_inserted():
    client = get_client()
    result = client.query("SELECT id, name, email FROM users WHERE id = 1")
    assert len(result.result_rows) > 0, "Test record not found."
    row = result.result_rows[0]
    assert row[1] == 'Alice', "Name does not match 'Alice'."
    assert row[2] == 'alice@example.com', "Email does not match 'alice@example.com'."
