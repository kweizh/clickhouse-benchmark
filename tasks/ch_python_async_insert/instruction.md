# ClickHouse Async Insert via Python

## Background
When ingesting data into ClickHouse, performance can degrade if many small inserts are performed. Using the Async Inserts feature allows ClickHouse to batch these small inserts server-side. You will write a Python script using the official `clickhouse-connect` SDK to demonstrate this.

## Requirements
- Create a Python script at `/home/user/project/async_insert.py`.
- The script must connect to a local ClickHouse instance at `localhost:8123` (username `default`, no password).
- Create a table named `async_table` with columns `id UInt64` and `data String`, using `MergeTree` engine ordered by `id`.
- Insert at least 5 rows of data into `async_table` using the `insert` method.
- You MUST enable Async Inserts for the ingestion by passing the appropriate settings (`async_insert=1` and `wait_for_async_insert=1`) in the insert call or connection.

## Implementation Guide
1. Ensure `clickhouse-connect` is installed.
2. Write the script to connect to the database.
3. Execute `CREATE TABLE IF NOT EXISTS async_table (id UInt64, data String) ENGINE = MergeTree ORDER BY id`.
4. Call `client.insert` with the data and the settings `{'async_insert': 1, 'wait_for_async_insert': 1}`.

## Constraints
- Project path: `/home/user/project`
- Script path: `/home/user/project/async_insert.py`