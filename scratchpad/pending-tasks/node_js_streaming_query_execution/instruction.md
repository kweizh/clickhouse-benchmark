The Node.js `@clickhouse/client` SDK is commonly used to build backend APIs that stream analytical data efficiently using formats like `JSONEachRow`.

You need to create a Node.js script (`query.js`) that connects to ClickHouse Cloud, queries the `system.tables` table, and streams the results to standard output in JSON format. 

**Constraints:**
- You must establish the connection over HTTPS using port `8443` (do not use the legacy 8123 port).
- The query execution method must specify `format: 'JSONEachRow'`.
- You must handle the streaming response properly and log the fully parsed JSON array to the console.