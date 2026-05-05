import sys
import sqlite3
import tempfile
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import backend

search_string = r".*discord.*/(a|a-shm|a-wal)$"
archive = "databaser/AFU.zip"

if __name__ == "__main__":
    try:
        for i in range(1,2):
            print(f"\nExtracting forensics relevant information from database: attempt {i}")
            with tempfile.TemporaryDirectory(delete=1) as tmpdir:
                backend.extract_known_databases(archive, search_string, tmpdir)
                databases = backend.list_dir_recursively(tmpdir)
                for database in databases:
                    if database.endswith("a"):
                        messages_table=backend.get_db_tables(database)[2]
                        with sqlite3.connect(database) as sql:
                            cur=sql.cursor()
                            cur.execute(f"""
                                        SELECT *
                                        FROM {messages_table}
                                        LIMIT 20;
                                        """)
                            for item in cur.fetchall():
                                
    except Exception as e:
        print(e)