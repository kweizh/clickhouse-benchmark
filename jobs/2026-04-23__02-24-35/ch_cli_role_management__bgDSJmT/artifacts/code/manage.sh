#!/bin/bash

# Arguments
EMAIL=$1
ROLE_ID=$2
KEY_NAME=$3

# Check if all arguments are provided
if [ -z "$EMAIL" ] || [ -z "$ROLE_ID" ] || [ -z "$KEY_NAME" ]; then
  echo "Usage: $0 <email> <role-id> <key-name>"
  exit 1
fi

# Create an invitation for the provided email address with the provided role ID
clickhousectl cloud --json invitation create --email "$EMAIL" --role-id "$ROLE_ID"

# Create an API key with the provided API key name and the provided role ID
clickhousectl cloud --json key create --name "$KEY_NAME" --role-id "$ROLE_ID"
