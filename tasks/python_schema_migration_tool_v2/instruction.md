# ClickHouse Schema Migration with Python

## Background
You need to build a simple schema migration script using the official Python SDK `clickhouse-connect`. The script will ensure a specific table schema exists in ClickHouse Cloud and apply an `ALTER TABLE` migration if a column is missing.

## Requirements
- Connect to ClickHouse Cloud using credentials from environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT` (default 8443), `CLICKHOUSE_USER` (default 'default'), and `CLICKHOUSE_PASSWORD`.
- Ensure a table named `users` exists with the engine `MergeTree` ordered by `id`. The initial schema should be `id UInt64, name String`.
- Detect if the `email` column (type `String`) exists in the `users` table.
- If the `email` column is missing, apply a migration to add it: `ALTER TABLE users ADD COLUMN email String`.
- Insert a test record with `id=1`, `name='Alice'`, and `email='alice@example.com'` into the `users` table.

## Implementation Guide
1. Create a Python script at `/home/user/migrate.py`.
2. Use `clickhouse_connect.get_client` to establish a secure connection (`secure=True`).
3. Use `client.command()` for DDL operations (CREATE, ALTER).
4. Query `system.columns` to check if the `email` column exists for the `users` table.
5. Use `client.insert()` to add the test record.

## Constraints
- Project path: `/home/user`
- The script must be executable by running `python3 /home/user/migrate.py`.
- Do not hardcode credentials; always read from the environment variables.