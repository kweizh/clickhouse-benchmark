import clickhouse_connect

def main():
    # Connect to ClickHouse
    client = clickhouse_connect.get_client(host='localhost', port=8123, username='REDACTED', password='')

    # Create table
    client.command('CREATE TABLE IF NOT EXISTS async_table (id UInt64, data String) ENGINE = MergeTree ORDER BY id')

    # Data to insert
    data = [
        (1, 'row 1'),
        (2, 'row 2'),
        (3, 'row 3'),
        (4, 'row 4'),
        (5, 'row 5')
    ]

    # Insert data with Async Inserts enabled
    client.insert(
        'async_table',
        data,
        column_names=['id', 'data'],
        settings={'async_insert': 1, 'wait_for_async_insert': 1}
    )

    print("Successfully inserted 5 rows into async_table with async_insert=1")

    # Verify insertion
    result = client.query('SELECT count() FROM async_table')
    print(f"Total rows in async_table: {result.result_rows[0][0]}")

if __name__ == '__main__':
    main()
