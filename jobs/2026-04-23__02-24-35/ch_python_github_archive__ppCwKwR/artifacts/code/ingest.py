import os
import clickhouse_connect

def main():
    # Read connection details from environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port = os.getenv('CLICKHOUSE_PORT')
    username = os.getenv('CLICKHOUSE_USERNAME')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if host is None or port is None or username is None:
        print("Error: Missing ClickHouse connection details in environment variables.")
        print(f"HOST: {host}, PORT: {port}, USERNAME: {username}")
        return

    try:
        # Connect to ClickHouse
        # If port is 8123, it's likely HTTP. If REDACTED, it's likely HTTPS.
        is_secure = port == 'REDACTED' or port == '443'
        client = clickhouse_connect.get_client(
            host=host,
            port=int(port),
            username=username,
            password=password if password else '',
            secure=is_secure
        )

        # Enable experimental JSON type if needed
        client.command("SET allow_experimental_object_type = 1")

        # Create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS github_events (
            id String,
            type String,
            actor JSON,
            repo JSON,
            payload JSON,
            public UInt8,
            created_at DateTime
        ) ENGINE = MergeTree()
        ORDER BY id
        """
        client.command(create_table_query)

        # Ingest data using url() function
        url = "https://data.gharchive.org/2015-01-01-15.json.gz"
        
        # We use INSERT INTO ... SELECT * FROM url(...)
        # The schema in the URL function should match the file content.
        # GH Archive JSON has these fields.
        insert_query = f"""
        INSERT INTO github_events
        SELECT id, type, actor, repo, payload, public, created_at
        FROM url('{url}', 'JSONEachRow')
        """
        
        print(f"Ingesting data from {url}...")
        client.command(insert_query)

        # Get total row count
        row_count = client.command("SELECT count() FROM github_events")
        print(f"Total rows in github_events: {row_count}")

        # Write row count to output.log
        with open('/home/user/ch-task/output.log', 'w') as f:
            f.write(str(row_count))
            
        print("Ingestion completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
