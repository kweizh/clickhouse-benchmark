"""Patch task.toml [environment.env] and [verifier.env] blocks to expose
the env vars each task actually consumes. Idempotent — running twice
produces the same result.
"""
import re
from pathlib import Path

TASKS_DIR = Path(__file__).resolve().parents[1] / "tasks"

# Canonical blocks of env vars per task (lines added to BOTH
# [environment.env] and [verifier.env]). POCHI_LOG / POCHI_API_KEY
# are appended automatically.
PATCHES: dict[str, list[str]] = {
    # --- ClickHouse Cloud SDK connection (CLICKHOUSE_*) ---
    "ch_nodejs_csv_load": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "ch_nodejs_data_dictionary": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "ch_nodejs_query_endpoint": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "ch_python_schema_migration": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "clickhouse_metrics_dashboard": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "node_js_streaming_query_execution": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "python_s3_data_ingestion": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "python_schema_migration_tool": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "python_schema_migration_tool_v2": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "python_sdk_basic_ingestion": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "system_metrics_dashboard": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],

    # --- ClickHouse Cloud SDK connection but with USERNAME (not USER) ---
    "ch_python_github_archive": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USERNAME = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "schema_migration": [
        'CLICKHOUSE_HOST = "${CLICKHOUSE_HOST}"',
        'CLICKHOUSE_PORT = "${CLICKHOUSE_PORT}"',
        'CLICKHOUSE_USERNAME = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],

    # --- ClickHouse Cloud SDK connection (CH_*) ---
    "ch_python_s3_parquet": [
        'CH_HOST = "${CLICKHOUSE_HOST}"',
        'CH_PORT = "${CLICKHOUSE_PORT}"',
        'CH_USER = "${CLICKHOUSE_USER}"',
        'CH_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],
    "ch_python_cold_start_handler": [
        'CH_HOST = "${CLICKHOUSE_HOST}"',
        'CH_PORT = "${CLICKHOUSE_PORT}"',
        'CH_USER = "${CLICKHOUSE_USER}"',
        'CH_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],

    # --- Analytics API: needs a full URL ---
    "ch_nodejs_analytics_api": [
        'CLICKHOUSE_URL = "${CLICKHOUSE_URL}"',
        'CLICKHOUSE_USER = "${CLICKHOUSE_USER}"',
        'CLICKHOUSE_PASSWORD = "${CLICKHOUSE_PASSWORD}"',
    ],

    # --- Cloud Management API tasks ---
    "ch_cli_backup_config": [
        'CH_API_KEY_ID = "${CLICKHOUSE_KEY_ID}"',
        'CH_API_KEY_SECRET = "${CLICKHOUSE_KEY_SECRET}"',
        'CH_ORG_ID = "${CLICKHOUSE_ORG_ID}"',
        'CH_SERVICE_ID = "${CLICKHOUSE_SERVICE_ID}"',
    ],
    "ch_cli_ip_access_list": [
        'CLICKHOUSE_API_URL = "${CLICKHOUSE_API_URL}"',
        'CLICKHOUSE_KEY_ID = "${CLICKHOUSE_KEY_ID}"',
        'CLICKHOUSE_KEY_SECRET = "${CLICKHOUSE_KEY_SECRET}"',
        'CLICKHOUSE_ORG_ID = "${CLICKHOUSE_ORG_ID}"',
        'CLICKHOUSE_SERVICE_ID = "${CLICKHOUSE_SERVICE_ID}"',
    ],
    "ch_cli_role_management": [
        'CLICKHOUSE_KEY_ID = "${CLICKHOUSE_KEY_ID}"',
        'CLICKHOUSE_KEY_SECRET = "${CLICKHOUSE_KEY_SECRET}"',
        'CLICKHOUSE_ORG_ID = "${CLICKHOUSE_ORG_ID}"',
    ],
    "ch_cli_service_deletion": [
        'CLICKHOUSE_KEY_ID = "${CLICKHOUSE_KEY_ID}"',
        'CLICKHOUSE_KEY_SECRET = "${CLICKHOUSE_KEY_SECRET}"',
        'CLICKHOUSE_ORG_ID = "${CLICKHOUSE_ORG_ID}"',
    ],
}

POCHI_LINES = [
    'POCHI_LOG = "debug"',
    'POCHI_API_KEY = "${POCHI_API_KEY}"',
]


def replace_section(text: str, section: str, body: str) -> str:
    """Replace the body of `[section]` with `body`. If the section doesn't
    exist, append it at the end of the file."""
    pattern = re.compile(
        rf"(\[{re.escape(section)}\]\n)(.*?)(?=\n\[|\Z)",
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(rf"\1{body}", text, count=1)
    sep = "" if text.endswith("\n") else "\n"
    return f"{text}{sep}\n[{section}]\n{body}"


def build_block(extra: list[str]) -> str:
    lines = POCHI_LINES + list(extra)
    return "\n".join(lines) + "\n"


def patch_file(path: Path, extra: list[str]) -> bool:
    text = path.read_text()
    body = build_block(extra)
    new = replace_section(text, "environment.env", body)
    new = replace_section(new, "verifier.env", body)
    if new != text:
        path.write_text(new)
        return True
    return False


def main() -> None:
    for task, extra in PATCHES.items():
        toml = TASKS_DIR / task / "task.toml"
        if not toml.exists():
            print(f"MISSING: {toml}")
            continue
        changed = patch_file(toml, extra)
        print(f"{'patched' if changed else 'unchanged'}: {task}")


if __name__ == "__main__":
    main()
