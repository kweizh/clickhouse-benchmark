import subprocess
import json
import pytest

def test_schema_migrations_table_exists():
    """Priority 1: Use clickhouse-client to verify the schema_migrations table exists."""
    result = subprocess.run(
        ["clickhouse-client", "--query", "EXISTS schema_migrations"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse-client failed: {result.stderr}"
    assert result.stdout.strip() == "1", "Table schema_migrations does not exist."

def test_schema_migrations_versions():
    """Priority 1: Use clickhouse-client to verify the two migration records exist."""
    result = subprocess.run(
        ["clickhouse-client", "--query", "SELECT version FROM schema_migrations ORDER BY version", "--format", "JSON"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse-client failed: {result.stderr}"
    data = json.loads(result.stdout)
    versions = [row["version"] for row in data["data"]]
    assert "01_create_users.sql" in versions, f"'01_create_users.sql' is missing from schema_migrations. Got: {versions}"
    assert "02_add_email.sql" in versions, f"'02_add_email.sql' is missing from schema_migrations. Got: {versions}"

def test_users_table_exists():
    """Priority 1: Use clickhouse-client to verify the users table exists."""
    result = subprocess.run(
        ["clickhouse-client", "--query", "EXISTS users"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse-client failed: {result.stderr}"
    assert result.stdout.strip() == "1", "Table users does not exist."

def test_users_table_columns():
    """Priority 1: Use clickhouse-client to verify the columns of the users table."""
    result = subprocess.run(
        ["clickhouse-client", "--query", "DESCRIBE TABLE users", "--format", "JSON"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"clickhouse-client failed: {result.stderr}"
    data = json.loads(result.stdout)
    columns = {row["name"]: row["type"] for row in data["data"]}
    
    assert "id" in columns, f"Column 'id' is missing from users table. Columns found: {list(columns.keys())}"
    assert columns["id"] == "UInt64", f"Expected column 'id' to be UInt64, got {columns['id']}"
    
    assert "name" in columns, f"Column 'name' is missing from users table. Columns found: {list(columns.keys())}"
    assert columns["name"] == "String", f"Expected column 'name' to be String, got {columns['name']}"
    
    assert "email" in columns, f"Column 'email' is missing from users table. Columns found: {list(columns.keys())}"
    assert columns["email"] == "String", f"Expected column 'email' to be String, got {columns['email']}"
