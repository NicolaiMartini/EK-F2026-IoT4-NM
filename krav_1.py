import backend
from time import sleep

SEARCH_STRING=r".*rema1000.*\/databases\/.*\.db.*$"
ARCHIVE="AFU.zip"

if __name__ == "__main__":
    try:
        print("\nExtraction beginning in 2 seconds.")
        sleep(2)
        backend.get_known_databases(ARCHIVE,SEARCH_STRING)
    except Exception as e:
        print(e)
