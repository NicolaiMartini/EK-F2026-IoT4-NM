import sys
import tempfile
from pathlib import Path
from time import sleep

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1])
)  # Add project root directory to path
import backend



if __name__ == "__main__":
    try:
        print("\nOriginal content of /tmp/, following tmp-naming:")
        for i in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in i:
                print(i)
        print("\nExtraction beginning in 2 seconds.")
        sleep(2)
        for i in range(1, 11):
            with tempfile.TemporaryDirectory(delete=0) as tmpdir:
                print(f"\nExtraction {i}, location {tmpdir}")
                print("\nExtracting AFU databases")
                backend.extract_known_databases("databaser/AFU.zip", r".*rejsekort.*.\.db.*", f"{tmpdir}/AFU")
                print("\nExtracting BFU databases")
                backend.extract_known_databases("databaser/BFU.zip", r".*rejsekort.*.\.db.*", f"{tmpdir}/BFU")
                print("\nExtracting adb databases")
                backend.extract_known_databases("databaser/adb.tar", r".*rejsekort.*.\.db.*", f"{tmpdir}/adb")
        print("\nExtraction complete, listing content of /tmp/:")
        for y in backend.list_dir_recursively("/tmp/"):
            if "/tmp/tmp" in y:
                print(y)
    except Exception as e:
        print(e)
