Performance degrades significantly in ClickHouse if users perform many small, row-by-row inserts. Using `clickhouse-connect` in Python requires batching inserts to maximize throughput.

You need to write a Python script (`ingest.py`) that reads a local file `dataset.csv` and inserts its 50,000 rows into a ClickHouse Cloud `MergeTree` table named `events`. 

**Constraints:**
- You must use the `clickhouse-connect` official Python SDK.
- You must configure the client to connect using port `8443` and `secure=True`.
- The data MUST be inserted in batches of at least 5,000 rows, or use the Async Inserts feature. Do NOT insert row-by-row.