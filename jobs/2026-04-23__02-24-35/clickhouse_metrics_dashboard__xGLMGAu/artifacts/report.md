# ClickHouse Metrics Dashboard Implementation

## Changes Made
- Installed `@clickhouse/client` in `/home/user/app`.
- Updated `src/app/page.js` to:
    - Connect to ClickHouse Cloud using `CLICKHOUSE_HOST` and `CLICKHOUSE_PASSWORD`.
    - Query `system.tables` for the total count of tables.
    - Display the result with the required text "Total Tables:".
    - Set the page to `force-dynamic` to ensure runtime data fetching.
- Verified the build with `npm run build`.

## Files Modified
- `src/app/page.js`
- `package.json` (dependency added)
