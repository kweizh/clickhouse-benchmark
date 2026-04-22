The ClickHouse Cloud Management API (`https://api.clickhouse.cloud/v1`) enables developers to automate cluster lifecycle events, such as scaling resources up or down programmatically.

You need to write a Python script (`scale_cluster.py`) that makes a REST API call to scale the memory allocation of an existing ClickHouse Cloud service. 

**Constraints:**
- You must use the `requests` library and target the official `v1` REST API endpoint.
- Authentication must be handled via Basic Auth using the `CLICKHOUSE_API_KEY_ID` and `CLICKHOUSE_API_KEY_SECRET` environment variables.
- Do NOT use `clickhousectl` or the standard SDKs; this task strictly tests direct REST API interaction.