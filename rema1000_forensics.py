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
    file_size = os.path.getsize(filename)
    bytes_read = 0
    
    print(f"Behandler {filename} ({file_size} bytes)...")
    
    with open(filename, "rb") as f:
        while True:
            byte_block = f.read(4096)
            if not byte_block:
                break
            
            sha256_hash.update(byte_block)
            bytes_read += len(byte_block)
            
            percent = (bytes_read / file_size) * 100
            
            bar_length = 20
            filled_length = int(bar_length * bytes_read // file_size)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            sys.stdout.write(f'\r[{bar}] {percent:.1f}%')
            sys.stdout.flush()
            
    print()
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
        databases = find_database_location(archive)
        with tempfile.TemporaryDirectory(delete=0,prefix=f"{datetime.datetime.now()}_") as tmpdir:
            print(f"Location: {tmpdir}")
            database_list = []
            with zipfile.ZipFile(archive) as zip_to_extract:
                for database in databases:
                    database_path = os.path.join(tmpdir,database)
                    if os.path.exists(database_path):
                        print(f"springer '{database_path}' over - findes allerede.")
                        database_list.append(database_path)
                        continue
                    print(f"Udhenter {database_path}")
                    zip_to_extract.extract(member=database,path=tmpdir)
                    database_list.append(database_path)
                return database_list
                
def retrieve_database_tables(database):
    with sqlite3.connect(database) as sql:
        cur=sql.cursor()
        cur.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type='table'
                    AND name NOT LIKE 'sqlite_%'
                    ORDER BY name;
                    """)
        tables=[row[0] for row in cur.fetchall()]
        return tables
    
def retrieve_table_headers(database,table):
    with sqlite3.connect(database) as sql:
        cur=sql.cursor()
        cur.execute(f"""
                    SELECT *
                    FROM {table};
                    """)
        column_headers = [description[0] for description in cur.description]
        return column_headers

def retrieve_table_content(database,table):
    with sqlite3.connect(database) as sql:
        cur=sql.cursor()
        cur.execute(f"""
                    SELECT *
                    FROM {table};
                    """)
        return cur.fetchall()

    
def main():
    try:
        parser = argparse.ArgumentParser(
            description="""Efterforskningsværktøj til android-databaser fra 'Rema1000 | Scan & Go'.
Script-argumenter kan ikke auto-complete med tabulator, men det kan stier.
            """,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Stier kan være fulde eller relative.
Brugseksempler:
python3 rema1000_forensics.py --archive (sti)/fil.zip --sha256
python3 rema1000_forensics.py --archive (sti/fil.zip) --search
python3 rema1000_forensics.py --archive (sti/fil.zip) --extract
python3 rema1000_forensics.py --archive (sti/fil.zip) --output_location (sti) --extract
python3 rema1000_forensics.py --get_database_tables (database)
python3 rema1000_forensics.py --get_table_headers (database) (table-navn)
python3 rema1000_forensics.py --get_table_content (database) (table-navn)
python3 rema1000_forensics.py --get_table_content (database) (table-navn) (antal rækker)
            """
        )
        
        parser.add_argument(
            "--archive",
            default=None,
            metavar=("FILENAME.ZIP"),
            help="Angiv stien til den zip-fil der skal benyttes."
        )
        
        parser.add_argument(
            "--output_location",
            default=None,
            metavar=("PATH/TO/OUTPUT/FOLDER/"),
            help="Angiv stien hvor dataen skal gemmes."
        )
        
        parser.add_argument(
            "--sha256sum",
            action="store_true",
            help="Udregn SHA256-sum af den angivne fil."
        )
        
        parser.add_argument(
            "--search",
            action="store_true",
            help="Bruges til at søge den angivne arkiv-fil for Rema1000-databaser."
        )
        
        parser.add_argument(
            "--extract",
            action="store_true",
            help="Denne kræver '--archive FIL'. Udhent databaser fra den angivne zip-fil til tmp/%%TEMP%%, afhængig af OS, eller til en specificeret lokation (hvis brugt med --output-location)."
        )
        
        parser.add_argument(
            "--get_database_tables",
            default=None,
            metavar=("DATABASE"),
            help="Bruges til at udhente database-tabellerne fra de databaser der er udhentet fra datasikringen."
        )
        
        parser.add_argument(
            "--get_table_headers",
            default=None,
            nargs=2,
            metavar=("DATABASE","TABLE"),
            help="Bruges til at udhente tabellernes kolonne-overskrifter."
        )
        
        parser.add_argument(
            "--get_table_content",
            default=None,
            nargs=3,
            metavar=("DATABASE","TABLE","(ROW_AMOUNT)"),
            help="Bruges til at udhente alt fra en db-table. Specificer database, table og antal rækker der skal outputtes i terminalen. Brug 0 som diste argument, for at få printet samtlige rækker i tabellen."
        )
        
        args = parser.parse_args()
            
        if args.sha256sum:
            print(f"SHA-256-sum af {args.archive}: {calculate_sha256sum(args.archive)}")
            
        if args.search:
            print(f"Søger i: {args.archive}")
            databases=find_database_location(args.archive)
            for database in databases:
                print(database)
                
        if args.extract:
            extract_databases(archive=args.archive,output_location=args.output_location)
            
        if args.get_database_tables:
            tables=retrieve_database_tables(args.get_database_tables)
            for table in tables:
                print(table)
                
        if args.get_table_headers:
            column_names=retrieve_table_headers(database=args.get_table_headers[0],table=args.get_table_headers[1])
            for header in column_names:
                print(header)
                
        if args.get_table_content:
            if int(args.get_table_content[2])==0:
                column_names=retrieve_table_headers(database=args.get_table_content[0],table=args.get_table_content[1])
                database_content=retrieve_table_content(database=args.get_table_content[0],table=args.get_table_content[1])
                for content in database_content:
                    print("\n")
                    for i in range(0,len(column_names)):
                        print(f"{column_names[i]}: {content[i]}")
            if int(args.get_table_content[2])>0:
                column_names=retrieve_table_headers(database=args.get_table_content[0],table=args.get_table_content[1])
                database_content=retrieve_table_content(database=args.get_table_content[0],table=args.get_table_content[1])
                for content in database_content[:int(args.get_table_content[2])]:
                    print("\n")
                    for i in range(0,len(column_names)):
                        print(f"{column_names[i]}: {content[i]}")
        
    except Exception as e:
        logger.error(f"Error has occured: {e}",exc_info=True)
    
if __name__ == "__main__":
    main()
