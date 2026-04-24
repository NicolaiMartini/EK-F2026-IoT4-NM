import re
import sys
import sqlite3
import tempfile
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime,timezone

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1])
)  # Add project root directory to path
import backend

REMA1000_RECEIPT_DB = r".*rema1000.*receipts\.db.*"  # Find all .db, -wal, -shm and -journal for a specific db. This is crucial - WAL is standard in most android phones today, and excluding the .db-extensions will probably provide an empty db.
CLEAN_DB = r".*db$"  # Only match files ending in exactly .db
AFU = "databaser/AFU.zip"

if __name__ == "__main__":
    try:
        with tempfile.TemporaryDirectory(delete=1) as tmpdir:  # pass delete=False in TemporaryDirectory() to keep the files to inspect, in case output is unexpected
            backend.extract_known_databases(AFU, REMA1000_RECEIPT_DB, tmpdir)
            databases = backend.list_dir_recursively(tmpdir)  # returns a list, but i just want the content, ergo indexing
            matches = []
            for database in databases:
                match = re.search(CLEAN_DB, database)
                if match:
                    matches.append(match.group())  # Creates a list with rel. databases in it
            receipts_db = matches[0]  # Only 1 item in the list.
            receipt_table_name = backend.get_db_tables(receipts_db)[0] # I want to access the first table in the db. It's called ReceiptEntity.
            with sqlite3.connect(receipts_db) as sql:
                cur=sql.cursor()
                cur.execute(f"""
                            SELECT searchText, paymentDate, paymentSource, pp_id, pp_cardType, pp_maskedPan
                            from {receipt_table_name};
                            """) #paymentDate is declared in ms, /1000 to be used in datetime.
                for item in cur.fetchall():
                    parts = item[0].split(';')[:3]
                    modified_first_item = ';'.join(parts) + ';'
                    modified_tuple = (modified_first_item,) + item[1:]
                    print(f"""
                          Location: {modified_tuple[0]}
                          Date and time: {datetime.fromtimestamp(modified_tuple[1]/1000, tz=ZoneInfo("Europe/Copenhagen")).strftime('%Y-%m-%d %H:%M:%S')}
                          Payment method: {modified_tuple[2]}
                          Payment ID: {modified_tuple[3]}
                          Card Type: {modified_tuple[4]}
                          Masked PAN: {modified_tuple[5]}
                          """)
    except Exception as e:
        print(e)