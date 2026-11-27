from pathlib import Path
import duckdb

DB_PATH = Path("scripts/northwind.duckdb")
RAW_DIR = Path("raw_data/raw")
LEGACY_DIR = Path("raw_data/legacy")


def load_csvs_to_schema(con: duckdb.DuckDBPyConnection, folder: Path, schema: str) -> None:
    if not folder.exists():
        print(f"Skip {schema}: {folder} does not exist")
        return

    csv_files = sorted(folder.glob("*.csv"))
    for csv_path in csv_files:
        table_name = csv_path.stem.replace(" ", "_").replace("-", "_").lower()
        full_table = f"{schema}.{table_name}"
        con.execute(
            f"""
            CREATE OR REPLACE TABLE {full_table} AS
            SELECT * FROM read_csv_auto('{csv_path.as_posix()}', header=True);
            """
        )
        row_count = con.execute(f"SELECT COUNT(*) FROM {full_table};").fetchone()[0]
        print(f"Loaded {full_table}: {row_count:,} rows")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        con.execute("CREATE SCHEMA IF NOT EXISTS legacy;")
        load_csvs_to_schema(con, RAW_DIR, "raw")
        load_csvs_to_schema(con, LEGACY_DIR, "legacy")
    finally:
        con.close()


if __name__ == "__main__":
    main()
