import re
import sys
import sqlite3
import tempfile
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1])
)  # Add project root directory to path
import backend

search_string = r"Dump/data/data/com.android.providers.telephony/databases/.*\.(db|db.*)$"
archive = "databaser/AFU.zip"

if __name__ == "__main__":
    try:
        for i in range(1,2):
            print(f"\nExtracting forensics relevant information from database: attempt {i}")
            with tempfile.TemporaryDirectory(delete=1) as tmpdir:  # pass delete=False in TemporaryDirectory() to keep the files to inspect, in case output is unexpected
                backend.extract_known_databases(archive, search_string, tmpdir)
                databases = backend.list_dir_recursively(tmpdir)
                for database in databases:
                    if database.endswith(".db"):
                        # print(backend.get_db_tables(database)) # Find relevant tables inside the database
                        table_sms=backend.get_db_tables(database)[10] # sms_table is index 10
                        with sqlite3.connect(database) as sql:
                            cur=sql.cursor()
                            cur.execute(f"""
                                        SELECT *
                                        FROM {table_sms}
                                        LIMIT 20;
                                        """)
                            [[print(cell) for cell in row] for row in cur.fetchall()]
                            # for row in cur.fetchall():
                                # for table_header, cell_content in zip(backend.get_table_headers(database,table_sms),row):
                                #     display = 0 if cell_content is None else cell_content
                                # print(f"{:>20}: {display:>45}")
    except Exception as e:
        print(e)