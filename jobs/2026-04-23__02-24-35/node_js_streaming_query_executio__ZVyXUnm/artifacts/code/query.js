const { createClient } = require('@clickhouse/client');

async function main() {
  const client = createClient({
    url: process.env.CLICKHOUSE_HOST || 'https://localhost:REDACTED',
    username: process.env.CLICKHOUSE_USER || 'REDACTED',
    password: process.env.CLICKHOUSE_PASSWORD || '',
  });

  try {
    const resultSet = await client.query({
      query: 'SELECT * FROM system.tables LIMIT 10',
      format: 'JSONEachRow',
    });

    const results = [];
    const stream = resultSet.stream();

    for await (const rows of stream) {
      rows.forEach((row) => {
        results.push(row.json());
      });
    }

    console.log(JSON.stringify(results, null, 2));
  } catch (error) {
    console.error('Error executing query:', error);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
