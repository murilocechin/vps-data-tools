import json
import os
import time

import psycopg2


# ======================================================
# Configuration
# ======================================================
CONNECTION = "fhirsyncbus"

CSV_FILE = "data/example.csv"

SCHEMA = "analytics"
TABLE = "example_table"

DELIMITER = ","
HEADER = True


# ======================================================
# Functions
# ======================================================
def load_db_config(connection: str) -> dict:
    config_path = f"configs/{connection}.json"

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def import_csv():

    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}"
        )

    db_config = load_db_config(CONNECTION)

    print("=" * 60)
    print("CSV IMPORT")
    print("=" * 60)
    print(f"Connection : {CONNECTION}")
    print(f"File       : {CSV_FILE}")
    print(f"Target     : {SCHEMA}.{TABLE}")

    start = time.perf_counter()

    conn = psycopg2.connect(**db_config)

    try:

        with conn:
            with conn.cursor() as cur:

                sql = f"""
                    COPY {SCHEMA}.{TABLE}
                    FROM STDIN
                    WITH (
                        FORMAT CSV,
                        DELIMITER '{DELIMITER}',
                        {"HEADER TRUE" if HEADER else ""}
                    )
                """

                with open(CSV_FILE, "r", encoding="utf-8") as file:
                    cur.copy_expert(sql, file)

    finally:
        conn.close()

    elapsed = time.perf_counter() - start

    print()
    print("Status : SUCCESS")
    print(f"Time   : {elapsed:.2f} s")
    print("=" * 60)


# ======================================================
# Main
# ======================================================
if __name__ == "__main__":
    import_csv()