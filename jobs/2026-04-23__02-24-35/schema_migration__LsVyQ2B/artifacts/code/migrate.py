import os
import clickhouse_connect

def migrate():
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 'REDACTED'))
    username = os.getenv('CLICKHOUSE_USERNAME', 'REDACTED')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not host or not password:
        print("Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables must be set.")
        return

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            secure=True
        )
        print(f"Connected to ClickHouse at {host}:{port}")

        # Open migrations.sql in the same directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        migrations_file = os.path.join(script_dir, 'migrations.sql')

        with open(migrations_file, 'r') as f:
            sql_content = f.read()

        # Split by semicolon and filter out empty statements
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]

        for statement in statements:
            print(f"Executing: {statement}")
            client.command(statement)
            print("Successfully executed.")

        print("Migration completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    migrate()
