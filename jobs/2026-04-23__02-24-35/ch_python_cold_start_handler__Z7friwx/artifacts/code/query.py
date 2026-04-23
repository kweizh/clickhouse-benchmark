import os
import clickhouse_connect

def main():
    # Read connection details from environment variables
    host = os.getenv('CH_HOST')
    port = os.getenv('CH_PORT')
    user = os.getenv('CH_USER')
    password = os.getenv('CH_PASSWORD')

    # Initialize ClickHouse client with specified timeouts for cold start handling
    client = clickhouse_connect.get_client(
        host=host,
        port=port,
        username=user,
        password=password,
        connect_timeout=30,
        send_receive_timeout=120
    )

    # Execute a simple query
    result = client.query('SELECT 1')

    # Print the result to standard output
    print(result.result_set[0][0])

if __name__ == '__main__':
    main()
