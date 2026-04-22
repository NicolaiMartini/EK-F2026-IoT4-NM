import os
import re
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])) # Add project root directory to path
import backend

ALL_REMA1000_DB=r".*rema1000.*.\.db.*" # Find all (.db, -wal, -shm, -journal) related to Rema1000.
REMA1000_RECEIPT_DB=r".*rema1000.*receipts\.db.*" # Find all .db, -wal, -shm and -journal for a specific db. This is crucial - WAL is standard in most android phones today, and excluding the .db-extensions might provide you with an empty db.
AFU="databaser/AFU.zip"

if __name__=="__main__":
    try:
        with tempfile.TemporaryDirectory(delete=True) as tmpdir: #pass delete=False in TemporaryDirectory() to keep the files to inspect, in case output is unexpected
            backend.extract_known_databases(AFU,REMA1000_RECEIPT_DB,tmpdir)
            databases=backend.list_dir_recursively(tmpdir) # returns a list, but i just want the content, ergo indexing
            pattern=re.compile(r".*db$")
            matches=[]
            for database in databases:
                match=pattern.search(database)
                if match:
                    matches.append(match.group()) # Creates a list with rel. databases in it
            receipts=matches[0] # Only 1 item in the list.
            print(backend.get_db_tables(receipts))
    except Exception as e:
        print(e)