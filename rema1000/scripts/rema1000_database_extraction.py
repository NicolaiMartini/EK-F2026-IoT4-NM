import os
import sys
import io
import sqlite3 as sql
import zipfile as zf
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from locate_and_extract import extract_known_databases, find_database_location

re_string=r".*rema1000.*.\.db.*"

# extract_known_databases("databaser/adb.tar",re_string,os.path.join(os.path.curdir,"rema1000/triage"))
# extract_known_databases("databaser/AFU.zip",re_string,"rema1000/AFU")
# extract_known_databases("databaser/BFU.zip",re_string,"rema1000/BFU")

# Følgende printer samtlige databaser ud, som findes i min AFU.zip,
# databases = find_database_location("databaser/AFU.zip", re_string)
# print(databases[0])
# for item in databases[1]:
#     print(item)

# Den db jeg vil undersøge er Dump/data/data/dk.rema1000.app/databases/receipts.db
with zf.ZipFile("databaser/AFU.zip", 'r') as zip_file:
    loaded_db = zip_file.open("Dump/data/data/dk.rema1000.app/databases/receipts.db")
    conn = sql.connect('loaded_db')
    cur = conn.cursor()
    cur.execute("""
                SELECT name FROM sqlite_master WHERE type='table';
                """)
    print(cur.fetchall())