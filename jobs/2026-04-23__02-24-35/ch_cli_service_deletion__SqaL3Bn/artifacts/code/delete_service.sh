#!/bin/bash

# Check if service name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_NAME="$1"

# Find the service ID associated with the provided service name
# We use --json for reliable parsing
SERVICES_JSON=$(clickhousectl cloud service list --json)

if [ $? -ne 0 ]; then
    echo "Error: Failed to list services. Please check your credentials and connectivity."
    exit 1
fi

SERVICE_ID=$(echo "$SERVICES_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    # The JSON output might be a list or an object containing a list (e.g., in a 'result' or 'services' field)
    if isinstance(data, list):
        services = data
    elif isinstance(data, dict):
        services = data.get('result', data.get('services', []))
    else:
        services = []
    
    for service in services:
        if service.get('name') == sys.argv[1]:
            print(service.get('id'))
            sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
" "$SERVICE_NAME")

if [ $? -ne 0 ] || [ -z "$SERVICE_ID" ]; then
    echo "Error: Service '$SERVICE_NAME' not found."
    exit 1
fi

# Delete the service using the found service ID
clickhousectl cloud service delete "$SERVICE_ID"
