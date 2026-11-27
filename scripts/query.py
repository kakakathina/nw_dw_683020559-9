import sys
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "scripts" / "northwind.duckdb"


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python scripts/query.py "<SQL_QUERY>"')
        return

    sql = sys.argv[1]
    con = duckdb.connect(str(DB_PATH))
    try:
        result = con.execute(sql).fetchall()
        cols = [desc[0] for desc in con.description] if con.description else []
        if cols:
            print(" | ".join(cols))
            print("-" * 50)
        for row in result:
            print(" | ".join(str(val) for val in row))
    finally:
        con.close()


if __name__ == "__main__":
    main()
