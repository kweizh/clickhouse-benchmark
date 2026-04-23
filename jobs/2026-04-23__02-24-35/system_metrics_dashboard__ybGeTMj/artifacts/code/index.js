const express = require('express');
const { createClient } = require('@clickhouse/client');
const path = require('path');

const app = express();
const port = 3000;

const client = createClient({
  url: process.env.CLICKHOUSE_HOST || 'https://localhost:REDACTED',
  password: process.env.CLICKHOUSE_PASSWORD || 'REDACTED',
  database: 'REDACTED',
});

app.use(express.static('public'));

app.get('/api/metrics', async (req, res) => {
  try {
    const resultSet = await client.query({
      query: 'SELECT metric, value FROM system.metrics LIMIT 10',
      format: 'JSONEachRow',
    });
    const dataset = await resultSet.json();
    res.json(dataset);
  } catch (error) {
    console.error('Error fetching metrics:', error);
    res.status(500).json({ error: 'Failed to fetch metrics' });
  }
});

app.listen(port, () => {
  console.log(`Dashboard listening at http://localhost:${port}`);
});
