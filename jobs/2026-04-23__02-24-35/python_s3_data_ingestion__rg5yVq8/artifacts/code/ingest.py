import os
import clickhouse_connect

def main():
    # Get credentials from environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port = os.getenv('CLICKHOUSE_PORT')
    user = os.getenv('CLICKHOUSE_USER')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not all([host, port, user, password]):
        print("Error: CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, and CLICKHOUSE_PASSWORD environment variables must be set.")
        return

    try:
        # Establish connection
        client = clickhouse_connect.get_client(
            host=host,
            port=int(port),
            username=user,
            password=password,
            secure=True
        )
        print(f"Connected to ClickHouse at {host}")

        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS aapl_stock (
            Date Date,
            Open Float64,
            High Float64,
            Low Float64,
            Close Float64,
            Volume UInt64,
            OpenInt UInt64
        ) ENGINE = MergeTree
        ORDER BY Date
        """
        client.command(create_table_query)
        print("Table 'aapl_stock' checked/created.")

        # Ingest data from S3
        s3_url = 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/aapl_stock.csv'
        insert_query = f"""
        INSERT INTO aapl_stock
        SELECT * FROM s3('{s3_url}', 'CSVWithNames')
        """
        
        # Before insertion count
        pre_count = client.query("SELECT count() FROM aapl_stock").result_rows[0][0]
        
        client.command(insert_query)
        
        # After insertion count
        post_count = client.query("SELECT count() FROM aapl_stock").result_rows[0][0]
        inserted = post_count - pre_count
        
        print(f"Data ingestion complete. Successfully inserted {inserted} rows.")
        print(f"Total rows in 'aapl_stock': {post_count}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
