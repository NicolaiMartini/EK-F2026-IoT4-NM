import sys
import tempfile
from pathlib import Path
from time import sleep

sys.path.insert(    0, str(Path(__file__).resolve().parents[1]))  # Add project root directory to path
import backend

# Find all (.db, -wal, -shm, -journal) related to rejsekort.
# Extract them to separate folders, depending on the original archive.

search_string = r"Dump/data/data/com.android.providers.telephony/databases/.*\.(db|db.*)$"
databases=["databaser/AFU.zip","databaser/BFU.zip","databaser/adb.tar"]

if __name__ == "__main__":
    try:
        print("\nOriginal content of /tmp/, following tmp-naming:")
        for dir in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in dir:
                print(dir)
        print("\nExtraction beginning in 2 seconds.")
        sleep(2)
        for index in range(1, 2):
            with tempfile.TemporaryDirectory(delete=0) as tmpdir:
                print(f"\nExtraction {index}, location {tmpdir}")
                for db in databases:
                    print(f"Extracting {Path(db).stem}")
                    backend.extract_known_databases(db,search_string,f"{tmpdir}/{Path(db).stem}")
        print("\nExtraction complete, listing content of /tmp/:")
        for dir in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in dir:
                print(dir)
    except Exception as e:
        print(e)