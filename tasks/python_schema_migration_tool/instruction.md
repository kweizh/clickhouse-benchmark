# ClickHouse Python Schema Migration Tool

## Background
Create a simple schema migration tool in Python using `clickhouse-connect` that applies SQL migration scripts to a ClickHouse Cloud service.

## Requirements
- Connect to ClickHouse using `clickhouse-connect`.
- Read all `.sql` files from a `migrations` directory.
- Execute each SQL file in alphabetical order.
- Record applied migrations in a `schema_migrations` table (columns: `version` String, `applied_at` DateTime).
- Skip migrations that have already been applied.

## Implementation
1. Initialize a Python project in `/home/user/project`.
2. Install `clickhouse-connect`.
3. Create a `migrate.py` script that implements the logic.
4. Create a `migrations` directory with two files: `01_create_users.sql` (creates a `users` table with `id` UInt64 and `name` String) and `02_add_email.sql` (adds an `email` String column to the `users` table).

## Constraints
- Project path: `/home/user/project`
- The ClickHouse credentials will be provided via environment variables: `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`.
- Log file: `/home/user/project/migration.log`