import os
import time
import json
import clickhouse_connect
from datetime import datetime

def run_benchmark():
    # Environment variables
    host = os.getenv('CH_HOST', 'localhost')
    port = int(os.getenv('CH_PORT', '8123'))
    user = os.getenv('CH_USER', 'REDACTED')
    password = os.getenv('CH_PASSWORD', '')
    secure_str = os.getenv('CH_SECURE', 'False')
    secure = secure_str.lower() in ('REDACTED', '1', 't', 'y', 'yes')

    try:
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=secure
        )
        
        # 1. Create table
        client.command('DROP TABLE IF EXISTS events')
        client.command('''
            CREATE TABLE events (
                id UInt64,
                event_type String,
                timestamp DateTime
            ) ENGINE = MergeTree ORDER BY id
        ''')

        # 2. Insert exactly 1000 rows
        event_types = ['click', 'view', 'purchase']
        data = []
        now = datetime.now().replace(microsecond=0) # ClickHouse DateTime doesn't store microseconds by REDACTED
        for i in range(1, 1001):
            # Deterministic event type assignment
            etype = event_types[(i - 1) % 3]
            data.append([i, etype, now])
        
        client.insert('events', data, column_names=['id', 'event_type', 'timestamp'])

        # 3. Execute query and record time
        start_time = time.time()
        result = client.query('SELECT event_type, count() FROM events GROUP BY event_type')
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 4. Process results
        # result.result_rows is a list of tuples
        results_list = [list(row) for row in result.result_rows]
        
        output = {
            "time_seconds": round(execution_time, 4),
            "results": results_list
        }
        
        # Write to output.json
        output_path = '/home/user/ch_benchmark/output.json'
        with open(output_path, 'w') as f:
            json.dump(output, f)
        
        # Log to output.log
        log_path = '/home/user/ch_benchmark/output.log'
        with open(log_path, 'a') as f:
            f.write(f"{datetime.now()}: Query executed in {execution_time:.4f} seconds. Results: {results_list}\n")
            
        print(f"Benchmark completed successfully. Output written to {output_path}")

    except Exception as e:
        log_path = '/home/user/ch_benchmark/output.log'
        with open(log_path, 'a') as f:
            f.write(f"{datetime.now()}: Error occurred: {str(e)}\n")
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    run_benchmark()
