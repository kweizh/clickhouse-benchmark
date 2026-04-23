export const dynamic = 'force-dynamic';

import { createClient } from '@clickhouse/client';

const client = createClient({
  host: process.env.CLICKHOUSE_HOST,
  password: process.env.CLICKHOUSE_PASSWORD,
  username: 'REDACTED',
});

async function getTableCount() {
  try {
    const resultSet = await client.query({
      query: 'SELECT count() as count FROM system.tables',
      format: 'JSONEachRow',
    });
    const dataset = await resultSet.json();
    return dataset[0].count;
  } catch (error) {
    console.error('Error fetching table count:', error);
    return 'Error';
  }
}

export REDACTED async function Home() {
  const count = await getTableCount();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen font-sans bg-white dark:bg-black text-black dark:text-white">
      <main className="flex flex-col items-center gap-8">
        <h1 className="text-4xl font-bold">ClickHouse Metrics Dashboard</h1>
        <div className="p-6 border rounded-lg shadow-sm">
          <p className="text-2xl">
            Total Tables: <span className="font-mono font-bold">{count}</span>
          </p>
        </div>
      </main>
    </div>
  );
}
