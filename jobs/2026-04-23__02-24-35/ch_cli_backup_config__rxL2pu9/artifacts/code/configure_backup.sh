#!/bin/bash

# Check if required environment variables are set
if [ -z "$CH_API_KEY_ID" ] || [ -z "$CH_API_KEY_SECRET" ] || [ -z "$CH_ORG_ID" ] || [ -z "$CH_SERVICE_ID" ]; then
    echo "Error: CH_API_KEY_ID, CH_API_KEY_SECRET, CH_ORG_ID, and CH_SERVICE_ID environment variables must be set."
    exit 1
fi

LOG_FILE="/home/user/ch-backup/output.log"

# JSON payload
PAYLOAD='{"startTime": "00:00", "retention": 7}'

# Send PATCH request to ClickHouse Cloud Management API
curl -s -X PATCH "https://api.clickhouse.cloud/v1/organizations/${CH_ORG_ID}/services/${CH_SERVICE_ID}/backupConfiguration" \
     -u "${CH_API_KEY_ID}:${CH_API_KEY_SECRET}" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD" > "$LOG_FILE" 2>&1

echo "Backup configuration update request sent. Check $LOG_FILE for details."
