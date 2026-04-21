import os
import sys
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from locate_and_extract import extract_known_databases

re_string=r".*rema1000.*.\.db.*"

extract_known_databases("databaser/filesystem.tar",re_string,os.path.join(os.path.curdir,"rema1000/triage"))
extract_known_databases("databaser/AFU_EXTRACTION_FFS.zip",re_string,"rema1000/AFU")
extract_known_databases("databaser/EXTRACTION_BFU.zip",re_string,"rema1000/BFU")