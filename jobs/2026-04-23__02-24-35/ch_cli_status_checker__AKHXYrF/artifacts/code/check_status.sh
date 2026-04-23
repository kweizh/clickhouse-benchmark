#!/bin/bash
clickhouse-client --query "SELECT version()" > /home/user/project/status.log
