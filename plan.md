# ClickHouse Cloud Evaluation Benchmark Research
This research provides the technical foundation for building evaluation datasets and benchmark tasks for AI coding agents operating ClickHouse Cloud via its SDKs, CLI, and Management API.
---
### 1. Library Overview
*   **Description**: ClickHouse Cloud is a fully managed, serverless, or dedicated version of the ClickHouse OLAP database. It is optimized for real-time analytical queries on massive datasets.
*   **Ecosystem Role**: Acts as the high-performance analytical layer in modern data stacks (often used alongside S3, Kafka, and BI tools like Grafana/Superset).
*   **Project Setup**:
    1.  **Cloud Console**: Create an account and a service (cluster) at [clickhouse.cloud](https://clickhouse.cloud).
    2.  **CLI Initialization**: Install `clickhousectl` (the modern CLI) and authenticate:
        ```bash
        curl -s https://clickhouse.com/clp | sh
        ./clickhousectl cloud auth
        ```
    3.  **Connection Details**: Locate the Hostname, Port (8443 for HTTPS, 9440 for Native), Username (`default`), and Password in the "Connect" modal of the Cloud Console.
---
### 2. Core Primitives & APIs
#### A. Unified CLI: `clickhousectl`
The modern tool for managing both local development and cloud services.
*   **Cloud Management**:
    ```bash
    # Create a new service
    clickhousectl cloud service create --name analytics-db --provider aws --region us-east-1
    # List services and get details
    clickhousectl cloud service list
    clickhousectl cloud service get <service-id>
    ```
*   **SQL Execution**:
    ```bash
    clickhousectl query "SELECT count() FROM system.parts"
    ```
#### B. Python SDK: `clickhouse-connect` (Official HTTP Client)
*   **Usage**:
    ```python
    import clickhouse_connect
    client = clickhouse_connect.get_client(
        host='your-host.clickhouse.cloud',
        port=8443,
        username='default',
        password='your-password',
        secure=True
    )
    # DDL
    client.command('CREATE TABLE test (id UInt64) ENGINE = MergeTree ORDER BY id')
    # Ingestion
    client.insert('test', [[1], [2], [3]], column_names=['id'])
    # Query
    result = client.query('SELECT sum(id) FROM test')
    print(result.result_rows)
    ```
*   **Docs**: [Python Integration](https://clickhouse.com/docs/en/integrations/python)
#### C. Node.js SDK: `@clickhouse/client`
*   **Usage**:
    ```javascript
    import { createClient } from '@clickhouse/client'
    const client = createClient({
      host: 'https://your-host.clickhouse.cloud:8443',
      password: 'your-password',
    })
    // Query with streaming support
    const resultSet = await client.query({
      query: 'SELECT * FROM system.tables LIMIT 5',
      format: 'JSONEachRow',
    })
    const dataset = await resultSet.json()
    ```
*   **Docs**: [Node.js Integration](https://clickhouse.com/docs/en/integrations/nodejs)
#### D. Cloud Management API (REST)
*   **Base URL**: `https://api.clickhouse.cloud/v1`
*   **Auth**: Uses `API Key ID` and `API Key Secret` passed via Basic Auth.
*   **Capabilities**: Programmatic scaling, backup management, and service lifecycle.
---
### 3. Real-World Use Cases & Templates
*   **Real-time Analytics API**: Building a REST API (using Express or FastAPI) that queries ClickHouse to provide dashboard metrics.
*   **S3 Data Ingestion**: Using the `s3()` table function to pull parquet/CSV data from AWS S3 into ClickHouse Cloud.
*   **GitHub Activity Tracker**: A common demo project involving ingesting the GitHub Archive dataset for trend analysis.
*   **Official Examples**: [ClickHouse JS Examples](https://github.com/ClickHouse/clickhouse-js/tree/main/examples) and [Python Examples](https://github.com/ClickHouse/clickhouse-connect/tree/main/examples).
---
### 4. Developer Friction Points
1.  **Protocol/Port Confusion**: Developers often try to use port 8123 (standard HTTP) instead of 8443 (Cloud HTTPS) or 9000 instead of 9440 (Native TLS). Cloud **strictly requires TLS**.
2.  **Serverless Idling**: ClickHouse Cloud services may "pause" when idle. The first request after a pause may experience higher latency (cold start), which SDKs need to handle via increased timeouts.
3.  **API Key Scoping**: Creating API keys with sufficient permissions (Admin vs Developer) for `clickhousectl` or the Management API.
4.  **Insert Batching**: Performance degrades significantly if users perform many small inserts. Agents must be taught to use bulk inserts or the `Async Inserts` feature.
---
### 5. Evaluation Ideas
*   **Provision & Load**: Use `clickhousectl` to create a service, then use the Python SDK to create a table and load a local CSV file.
*   **Scaling Automation**: Write a script using the Cloud REST API to scale up a cluster's memory based on current usage metrics.
*   **Secure Connection Setup**: Configure a Node.js client to connect using a custom CA certificate for enterprise environments.
*   **Schema Migration**: Implement a simple migration tool that uses the SDK to detect schema changes and apply `ALTER TABLE` commands.
*   **Query Endpoint Generator**: Use the Cloud API to programmatically create and configure "Query Endpoints" (REST wrappers for SQL).
*   **Backup Management**: Create a script to list all backups for a specific service and trigger a restore to a new "dev" service.
---
### 6. Sources
1.  [ClickHouse Docs - llms.txt](https://clickhouse.com/docs/llms.txt): Comprehensive structured documentation for LLMs.
2.  [ClickHouse Cloud CLI Reference](https://clickhouse.com/docs/cloud/features/cli): Documentation for the new `clickhousectl`.
3.  [ClickHouse Python SDK Guide](https://clickhouse.com/docs/en/integrations/python): Official guide for `clickhouse-connect`.
4.  [ClickHouse Node.js SDK Guide](https://clickhouse.com/docs/en/integrations/nodejs): Official guide for `@clickhouse/client`.
5.  [ClickHouse Cloud Management API](https://clickhouse.com/docs/cloud/manage/api/api-overview): OpenAPI specification and REST API details.
6.  [ClickHouse Cloud Connection Details](https://clickhouse.com/docs/cloud/guides/sql-console/gather-connection-details): Guide for finding host/port/auth info.
