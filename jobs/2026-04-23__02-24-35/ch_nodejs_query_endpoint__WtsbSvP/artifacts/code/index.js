const express = require('express');
const { createClient } = require('@clickhouse/client');

const app = express();
const port = process.env.PORT || 3000;

const clickhouseHost = process.env.CLICKHOUSE_HOST;
const clickhousePassword = process.env.CLICKHOUSE_PASSWORD;

if (!clickhouseHost || !clickhousePassword) {
  console.error('CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are required.');
  process.exit(1);
}

const client = createClient({
  host: clickhouseHost.includes('://') ? clickhouseHost : `https://${clickhouseHost}:REDACTED`,
  username: 'REDACTED',
  password: clickhousePassword,
});

app.get('/tables', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT name FROM system.tables LIMIT 5',
      format: 'JSONEachRow',
    });
    const dataset = await resultSet.json();
    const tables = dataset.map(row => row.name);
    res.json(tables);
  } catch (error) {
    console.error('Error querying ClickHouse:', error);
    res.status(500).json({ error: 'Internal Server Error', message: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
