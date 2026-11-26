from pathlib import Path
import duckdb

DB_PATH = Path("data/nw_dw.duckdb")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        con.execute("CREATE SCHEMA IF NOT EXISTS legacy;")
        con.execute("CREATE SCHEMA IF NOT EXISTS staging;")
        schemas = con.execute(
            "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;"
        ).fetchall()
        print(f"Connected to DuckDB at: {DB_PATH}")
        print("Available schemas:", [s[0] for s in schemas])
    finally:
        con.close()


if __name__ == "__main__":
    main()
