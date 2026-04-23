CREATE TABLE IF NOT EXISTS users (
    id UInt64,
    name String
) ENGINE = MergeTree()
ORDER BY id;
