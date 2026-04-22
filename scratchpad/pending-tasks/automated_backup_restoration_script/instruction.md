ClickHouse Cloud automatically handles backups, but developers often need to programmatically list available backups and restore them to provision new developer environments.

You need to write a bash script (`restore_backup.sh`) using `curl` that queries the Cloud Management API to list all backups for a provided service ID, finds the most recent backup, and triggers a restoration. 

**Constraints:**
- The script must accept the target Service ID as its first command-line argument.
- You must parse the JSON response (e.g., using `jq`) to extract the ID of the most recent backup.
- You must make a subsequent POST request to the API to trigger the restore operation for that specific backup ID.