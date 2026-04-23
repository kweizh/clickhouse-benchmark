# ClickHouse Service Status Checker

## Background
You need to automate the monitoring of a ClickHouse service using the official `clickhouse-client` CLI.

## Requirements
Write a bash script `check_status.sh` that retrieves the version of a ClickHouse service to verify it is running.
- The script must use `clickhouse-client` to execute the query `SELECT version()`.
- The output of the command must be saved to `status.log`.
- The script must be executable.

## Implementation Guide
1. Create a script named `check_status.sh` in `/home/user/project`.
2. Add the shebang `#!/bin/bash`.
3. Run `clickhouse-client --query "SELECT version()" > /home/user/project/status.log`.
4. Make the script executable with `chmod +x /home/user/project/check_status.sh`.

## Constraints
- Project path: `/home/user/project`
- Log file: `/home/user/project/status.log`
- You must use `clickhouse-client --query`.

## Integrations
- None