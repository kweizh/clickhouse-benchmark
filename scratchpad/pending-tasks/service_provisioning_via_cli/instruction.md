ClickHouse Cloud offers a unified CLI (`clickhousectl`) to easily spin up and manage cloud infrastructure.

You need to write a bash script named `provision.sh` that uses `clickhousectl` to create a new ClickHouse Cloud service and extracts the newly generated service ID into a file. 

**Constraints:**
- The service must be named `analytics-db`, use the `aws` provider, and be located in the `us-east-1` region.
- The script must parse the output to retrieve the service ID and save it exactly to a file named `service_id.txt`.
- Do NOT include any interactive prompts in your bash script.