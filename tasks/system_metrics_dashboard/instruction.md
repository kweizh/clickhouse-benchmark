# ClickHouse System Metrics Dashboard

## Background
Create a simple Node.js Express dashboard that connects to ClickHouse Cloud and displays system metrics.

## Requirements
- Connect to ClickHouse Cloud using the `@clickhouse/client` SDK.
- Create an Express API endpoint `/api/metrics` that runs `SELECT metric, value FROM system.metrics LIMIT 10` and returns the results as JSON.
- Serve a static `index.html` at the root `/` that fetches data from `/api/metrics` and displays it in a list.
- The ClickHouse connection must use the environment variables `CLICKHOUSE_HOST` and `CLICKHOUSE_PASSWORD`. The connection should be secure (HTTPS).

## Implementation
1. Initialize a Node.js project in `/home/user/dashboard`.
2. Install `express` and `@clickhouse/client`.
3. Create an `index.js` that sets up the Express server on port 3000 and serves static files from `public`.
4. Create `public/index.html` with a script to fetch and display the metrics.

## Constraints
- Project path: `/home/user/dashboard`
- Start command: `node index.js`
- Port: 3000