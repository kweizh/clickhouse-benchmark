import os
import logging
import clickhouse_connect

# Configure logging
log_file = '/home/user/ch-migration/migration.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def migrate():
    # 1. Read connection details from environment variables
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 'REDACTED'))
    username = os.getenv('CLICKHOUSE_USER', 'REDACTED')
    password = os.getenv('CLICKHOUSE_PASSWORD')

    if not host or not password:
        logging.error("CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD must be set")
        return

    try:
        # 2. Connect to ClickHouse Cloud
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=username,
            password=password,
            secure=True
        )
        logging.info("Connected to ClickHouse Cloud")

        # 3. Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UInt64,
            username String
        ) ENGINE = MergeTree
        ORDER BY id
        """
        client.command(create_table_query)
        logging.info("Table 'users' checked/created")

        # 4. Add column if not exists
        alter_table_query = "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime"
        client.command(alter_table_query)
        logging.info("Column 'last_login' checked/added to 'users' table")

        # 5. Success message
        success_msg = "Migration completed successfully"
        logging.info(success_msg)
        print(success_msg)

    except Exception as e:
        error_msg = f"Migration failed: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

if __name__ == "__main__":
    migrate()
