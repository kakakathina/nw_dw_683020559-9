from pathlib import Path
import sys
import duckdb

DB_PATH = Path("data/nw_dw.duckdb")

DEFAULT_QUERY = """
SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema IN ('raw', 'legacy')
ORDER BY table_schema, table_name;
"""


def main() -> None:
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}. Run scripts/create_duckdb.py and scripts/load_raw.py first.")
        return

    sql = " ".join(sys.argv[1:]).strip() or DEFAULT_QUERY
    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        rel = con.sql(sql)
        print(rel)
    finally:
        con.close()


if __name__ == "__main__":
    main()
