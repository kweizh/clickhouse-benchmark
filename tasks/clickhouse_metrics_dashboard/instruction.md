# ClickHouse Metrics Dashboard

## Background
Create a simple Next.js web application that connects to ClickHouse Cloud and displays system metrics.

## Requirements
- Build a Next.js app that connects to ClickHouse using `@clickhouse/client`.
- The app must display the total number of tables in the ClickHouse database by querying `SELECT count() as count FROM system.tables`.
- The page must contain the text 'Total Tables:' followed by the count.

## Implementation Guide
1. A Next.js project is already initialized in `/home/user/app`.
2. Install `@clickhouse/client` in `/home/user/app`.
3. Update the main page (`app/page.js` or `pages/index.js`) to fetch the count of system tables from ClickHouse.
4. Use the `CLICKHOUSE_HOST` and `CLICKHOUSE_PASSWORD` environment variables to connect. The host is HTTPS on port 8443 (e.g., `https://your-host:8443`). Username is `default`.

## Constraints
- **Project path**: `/home/user/app`
- **Start command**: `npm run build && npm start`
- **Port**: 3000