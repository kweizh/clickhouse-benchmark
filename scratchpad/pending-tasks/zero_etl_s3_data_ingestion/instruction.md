ClickHouse natively supports reading from external object storage like AWS S3, allowing developers to pull data such as Parquet or CSV files directly into a table without external ETL tools.

You need to write a standalone SQL script (`ingest_s3.sql`) that creates a new table `user_activity` and populates it by querying an external S3 bucket using the `s3()` table function. 

**Constraints:**
- The script must contain valid ClickHouse SQL syntax containing a `CREATE TABLE` statement followed by an `INSERT INTO ... SELECT` statement.
- Do NOT rely on external scripting languages (Python/Node.js) to perform the data movement.
- Assume the S3 bucket is public and contains Parquet files; format the `s3()` function call accordingly.