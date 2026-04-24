import sys
import tempfile
from pathlib import Path
from time import sleep

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1])
)  # Add project root directory to path
import backend

# Find all (.db, -wal, -shm, -journal) related to Rema1000.
# Extract them to separate folders, depending on the original archive.


if __name__ == "__main__":
    try:
        original_tmp = backend.list_dir_recursively("/tmp/")
        print("Original content of /tmp/:")
        print(original_tmp)
        print("Extraction beginning.")
        sleep(1)
        for i in range(1, 9):
            print(f"Extraction {i}")
            with tempfile.TemporaryDirectory(delete=0) as tmpdir:
                print("Extracting AFU databases")
                backend.extract_known_databases(
                    "databaser/AFU.zip", r".*{tmpdir}.*.\.db.*", f"{tmpdir}/AFU"
                )
                print("Extracting BFU databases")
                backend.extract_known_databases(
                    "databaser/BFU.zip", r".*{tmpdir}.*.\.db.*", f"{tmpdir}/BFU"
                )
                print("Extracting adb databases")
                backend.extract_known_databases(
                    "databaser/adb.tar", r".*{tmpdir}.*.\.db.*", f"{tmpdir}/adb"
                )
                print("Extraction complete, listing new content of /tmp/")
                for i in backend.list_dir_recursively("/tmp/"):
                    print(i)
    except Exception as e:
        print(e)
