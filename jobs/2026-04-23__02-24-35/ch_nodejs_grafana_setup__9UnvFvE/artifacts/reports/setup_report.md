# ClickHouse Setup Report

## Project Details
- Path: `/home/user/project`
- Script: `setup_grafana.js`

## Database Schema
- Database: `grafana_db`
- Table: `metrics`
  - `timestamp` (DateTime)
  - `metric_name` (String)
  - `value` (Float64)
- Engine: `MergeTree`
- Order By: `(metric_name, timestamp)`

## User Configuration
- User: `grafana_user`
- Password: `grafana_pass`
- Privileges: `SELECT` on `grafana_db.metrics`

## Execution Result
The script was executed successfully and the database was configured.
