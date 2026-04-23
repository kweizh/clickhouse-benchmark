const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function main() {
  const url = `https://${process.env.CLICKHOUSE_HOST}:REDACTED`;
  const password = process.env.CLICKHOUSE_PASSWORD;
  const username = 'REDACTED';

  const client = createClient({
    url,
    username,
    password,
    database: 'REDACTED',
  });

  try {
    // 1. Create table
    await client.command({
      query: `
        CREATE TABLE IF NOT EXISTS employees (
          id UInt32,
          name String,
          department String,
          salary Float64
        ) ENGINE = MergeTree()
        ORDER BY id
      `,
    });

    // 2. Insert data from CSV
    const csvFilePath = '/home/user/ch-task/employees.csv';
    const stream = fs.createReadStream(csvFilePath);

    await client.insert({
      table: 'employees',
      values: stream,
      format: 'CSVWithNames',
    });

    // 3. Write success to log
    fs.writeFileSync('/home/user/ch-task/output.log', 'Success');
    console.log('Success');

  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
