import os
import logging
import clickhouse_connect
from datetime import datetime

# Setup logging
LOG_FILE = '/home/user/project/migration.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def migrate():
    host = os.getenv('CLICKHOUSE_HOST')
    port = int(os.getenv('CLICKHOUSE_PORT', 8123))
    user = os.getenv('CLICKHOUSE_USER', 'REDACTED')
    password = os.getenv('CLICKHOUSE_PASSWORD', '')
    secure = os.getenv('CLICKHOUSE_SECURE', 'REDACTED').lower() == 'REDACTED'

    if not host:
        logger.error("CLICKHOUSE_HOST environment variable is not set")
        return

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=secure
        )
        logger.info(f"Connected to ClickHouse at {host}")

        # Create schema_migrations table if not exists
        client.command("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version String,
                applied_at DateTime DEFAULT now()
            ) ENGINE = MergeTree()
            ORDER BY version
        """)

        # Get applied migrations
        applied_migrations = client.query("SELECT version FROM schema_migrations").result_set
        applied_versions = {row[0] for row in applied_migrations}

        # Read migration files
        migrations_dir = '/home/user/project/migrations'
        migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])

        for filename in migration_files:
            if filename in applied_versions:
                logger.info(f"Skipping already applied migration: {filename}")
                continue

            logger.info(f"Applying migration: {filename}")
            filepath = os.path.join(migrations_dir, filename)
            
            with open(filepath, 'r') as f:
                sql = f.read().strip()
                
            if sql:
                # Multiple statements in one file might be tricky with client.command
                # but for simple migrations we assume one block or ClickHouse handles it
                # Split by semicolon if needed, but ClickHouse client.command usually handles one logical block.
                # For safety, let's split by ';' if it's multiple statements, 
                # but clickhouse-connect's command() can take a single string with multiple statements sometimes
                # actually it's better to execute them one by one if we want robust error handling.
                statements = [s.strip() for s in sql.split(';') if s.strip()]
                for statement in statements:
                    client.command(statement)
                
                # Record migration
                client.command(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    parameters=[filename]
                )
                logger.info(f"Successfully applied migration: {filename}")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == '__main__':
    migrate()
