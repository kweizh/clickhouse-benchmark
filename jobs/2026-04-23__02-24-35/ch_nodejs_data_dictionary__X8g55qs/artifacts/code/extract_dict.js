const { createClient } = require('@clickhouse/client');
const fs = require('fs');
const path = require('path');

async function extractDictionary() {
  let host = process.env.CLICKHOUSE_HOST;
  const password = process.env.CLICKHOUSE_PASSWORD;

  if (!host || !password) {
    console.error('Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are not set.');
    process.exit(1);
  }

  // Ensure host has protocol and port if missing (common for ClickHouse Cloud)
  if (!host.startsWith('http')) {
    host = `https://${host}:REDACTED`;
  }

  const client = createClient({
    url: host,
    username: 'REDACTED',
    password: password,
  });

  try {
    console.log('Connecting to ClickHouse and querying system.columns...');
    const resultSet = await client.query({
      query: "SELECT database, table, name, type FROM system.columns WHERE database = 'system'",
      format: 'JSON',
    });

    const result = await resultSet.json();
    const data = result.data;

    const outputPath = path.join(__dirname, 'dictionary.json');
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));

    console.log(`Successfully extracted ${data.length} columns.`);
    console.log(`Data dictionary saved to ${outputPath}`);
  } catch (error) {
    console.error('Error during extraction:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

extractDictionary();
