import sys
import tempfile
from pathlib import Path
from time import sleep

sys.path.insert(    0, str(Path(__file__).resolve().parents[1]))  # Add project root directory to path
import backend

# Find all (.db, -wal, -shm, -journal) related to rejsekort.
# Extract them to separate folders, depending on the original archive.

search_string = r".*discord.*\.db.*"

if __name__ == "__main__":
    try:
        print("\nOriginal content of /tmp/, following tmp-naming:")
        for i in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in i:
                print(i)
        print("\nExtraction beginning in 2 seconds.")
        sleep(2)
        for i in range(1, 2):
            with tempfile.TemporaryDirectory(delete=0) as tmpdir: # Will produce temprary folders with naming convention of starting with "tmp" along with randomized suffixes
                print(f"\nExtraction {i}, location {tmpdir}")
                for i in ["databaser/AFU.zip", "databaser/BFU.zip", "databaser/adb.tar"]:
                    print(f"Extracting {Path(i).stem}")
                    backend.extract_known_databases(i,search_string,f"{tmpdir}/{Path(i).stem}")
        print("\nExtraction complete, listing content of /tmp/:")
        for y in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in y:
                print(y)
    except Exception as e:
        print(e)
