import sys
import tempfile
from pathlib import Path
from time import sleep

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import backend

search_string=r".*rema1000.*.\.(db|db.*)$"
archives=["databaser/AFU.zip","databaser/BFU.zip","databaser/adb.tar"]

if __name__ == "__main__":
    try:
        print("\nOriginal content of /tmp/, following tmp-naming:")
        for i in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in i:
                print(i)
        print("\nExtraction beginning in 2 seconds.")
        sleep(2)
        for i in range(1, 2):
            with tempfile.TemporaryDirectory(delete=1) as tmpdir:
                print(f"\nExtraction {i}, location {tmpdir}")
                for db in archives:
                    print(f"Extracting {Path(db).stem}")
                    backend.extract_known_databases(db,search_string,f"{tmpdir}/{Path(db).stem}")
        print("\nExtraction complete, listing content of /tmp/:")
        for y in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in y:
                print(y)
    except Exception as e:
        print(e)
