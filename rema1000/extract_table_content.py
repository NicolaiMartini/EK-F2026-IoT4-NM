import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])) # Add project root directory to path
import backend
import sqlite3
import zipfile
import os
import tempfile
import time
import glob

RE_STRING=r".*rema1000.*.\.db.*"
AFU="databaser/AFU.zip"

if __name__=="__main__":
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            backend.extract_known_databases(AFU,RE_STRING,tmpdir)
            # for file_path in glob.iglob(os.path.join(tmpdir,'**','*'),recursive=True): # start in tmpdir, traverse every subdir ('**') and grab everything ('*')
            #     if os.path.isfile(file_path):
            #         print(file_path)
            for root, dirs, files in os.walk(tmpdir): # More intuitive? Maybe?
                for name in files:
                    print(os.path.join(root,name))
    except Exception as e:
        print(e)