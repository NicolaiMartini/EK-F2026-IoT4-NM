# """
# CLI-venlige script til digital efterforskning af 'Rema1000 | Scan & Go' databaser datasikriet fra Android-telefoner.
# Scriptet er udarbejdet baseret på en 'After First Unlock'-datasikring fra Cellebrite UFED.

# Brug '-h' for at se muligheder.
# """

import re
import os
import sys
import logging
import hashlib
import argparse
import zipfile
import tempfile
import sqlite3
import datetime
import zoneinfo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("rema1000_forensics.log"),
        logging.StreamHandler()
    ]
)

logger=logging.getLogger(__name__)

REGEX_SEARCH_STRING=r".*rema1000.*\/databases\/.*\.db.*$"

def calculate_sha256sum(filename):
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
    

def find_database_location(archive):
    re_matches = []
    with zipfile.ZipFile(archive) as zip:
        zip_content = zipfile.ZipFile.namelist(zip)
        for item in zip_content:
            match = re.search(REGEX_SEARCH_STRING, item, re.IGNORECASE)
            if match:
                re_matches.append(match.group())
    return re_matches

def extract_databases(archive,output_location=None):
    if output_location is not None:
        os.makedirs(output_location,exist_ok=True)
        databases = find_database_location(archive)
        with zipfile.ZipFile(archive) as zip_to_extract:
            database_list = []
            for database in databases:
                database_path = os.path.join(output_location,database)
                if os.path.exists(database_path):
                    print(f"springer '{database_path}' over - findes allerede.")
                    database_list.append(database_path)
                    continue
                print(f"Udhenter {database_path}")
                zip_to_extract.extract(member=database,path=output_location)
                database_list.append(database_path)
            return database_list
    if output_location is None:
        with tempfile.TemporaryDirectory(prefix="EXTRACTION_") as tmpdir:
            print(f"Location: {tmpdir}")
            database_list = []
            for database in databases:
                database_path = os.path.join(output_location,database)
                if os.path.exists(database_path):
                    print(f"springer '{database_path}' over - findes allerede.")
                    database_list.append(database_path)
                    continue
                print(f"Udhenter {database_path}")
                zip_to_extract.extract(member=database,path=output_location)
                database_list.append(database_path)
            return database_list
                

    
def main():
    try:
        parser = argparse.ArgumentParser(
            description="Efterforskningsværktøj til android-databaser fra 'Rema1000 | Scan & Go'.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
            python3 rema1000_forensics.py --archive <ful/sti/til/filnavn.zip> --yderligere-argumenter <argument>
            Eksempel:
            python3 rema1000_forensics.py --archive /home/peter/Downloads/android.zip --sha256
            python3 rema1000_forensics.py --archive ~/Documents/AFU.zip --search
            """
        )
        
        parser.add_argument(
            "--archive",
            required=True,
            help="Angiv stien til den zip-fil der skal benyttes."
        )
        
        parser.add_argument(
            "--output_location",
            default=None,
            help="Angiv stien hvor dataen skal gemmes"
        )
        
        parser.add_argument(
            "--sha256",
            action="store_true",
            help="Opnå Sha256-sum af den angivne fil."
        )
        
        parser.add_argument(
            "--search",
            action="store_true",
            help="--search benyttes til at søge den angivne arkiv-fil for Rema1000-databaser."
        )
        
        parser.add_argument(
            "--extract",
            action="store_true",
            help="--extract-temp bruges til at extracte filen til tmp/%%TEMP%%, afhængig af OS."
        )
        
        args = parser.parse_args()
        
        if args.archive:
            print(f"Arkiv er: {args.archive}")
            
        elif args.sha256:
            print(f"Udregner SHA256-sum af: {args.archive}")
            print(calculate_sha256sum(args.archive))
            
        elif args.search:
            print(f"Søger i: {args.archive}")
            databases=find_database_location(args.archive)
            for database in databases:
                print(database)
                
        elif args.extract:
            extract_databases(archive=args.archive,output_location=args.output_location)
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error has occured: {e}",exc_info=True)
    
if __name__ == "__main__":
    main()


# import folium # requires install (pip or global). To be used with krav 9 and 10
# import pandas # requires install (pip or global). To be used with krav 9 and 10