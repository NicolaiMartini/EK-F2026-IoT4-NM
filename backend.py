import re
import os
import zipfile
import tempfile
import sqlite3

def find_database_location(archive, regexstring):
    """
    Find the in-archive location of desired databases.\n
    Please input a regexstring to search inside the archive. The search is case insensitive.
    """
    try:
        re_matches = []
        with zipfile.ZipFile(archive) as zip:
            zip_content = zipfile.ZipFile.namelist(zip)
            for item in zip_content:
                match = re.search(regexstring, item, re.IGNORECASE)
                if match:
                    re_matches.append(match.group())
        return re_matches
    except Exception as e:
        print(e)


def get_known_databases(archive: str, regex_string: str, output_directory:str=None,temporary=0):
    """
    Extract the databases to the provided output_directory. If no directory is provided, it will extract to OS-agnostic temporary directory. This tmp-dir will persist in tmp/%temp% unless temporary=1 is passed as parameter.\n
    Extracted items will also be returned as a list.\n
    Please input a regexstring. The search is case insensitive.\n
    """
    try:
        if output_directory is not None:
            os.makedirs(output_directory, exist_ok=True)
            databases = find_database_location(archive, regex_string)
            with zipfile.ZipFile(archive) as extract_zip:
                items=[]
                for item in databases:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        items.append(item_path)
                        continue
                    print(f"Extracting: {item_path}")
                    extract_zip.extract(member=item, path=output_directory)
                    items.append(item_path)
                return items
        if output_directory is None:
            with tempfile.TemporaryDirectory(delete=temporary,prefix="EXTRACTION_") as tmpdir:
                print(f"Location: {tmpdir}")
                databases = find_database_location(archive, regex_string)
                with zipfile.ZipFile(archive) as extract_zip:
                    items=[]
                    for item in databases:
                        item_path = os.path.join(tmpdir, item)
                        if os.path.exists(item_path):
                            print(f"skipping '{item} - already exists")
                            items.append(item_path)
                            continue
                        print(f"Extracting: {item_path}")
                        extract_zip.extract(member=item, path=tmpdir)
                        items.append(item_path)
                    return items
    except Exception as e:
        print(e)


def get_db_tables(database):
    """
    Retrieve the tables of the specified database.
    """
    try:
        with sqlite3.connect(database) as sql:
            cur = sql.cursor()
            cur.execute("""SELECT name 
                        FROM sqlite_master 
                        WHERE type='table' 
                        AND name NOT LIKE 'sqlite_%'
                        ORDER BY name
                        ;""")
            tables = [row[0] for row in cur.fetchall()]
            return tables
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)


def get_table_headers(database, table):
    """
    Retrieve the table headers of the specified table.
    """
    with sqlite3.connect(database) as sql:
        cur = sql.cursor()
        cur.execute(f"SELECT * FROM {table};")
        column_names = [description[0] for description in cur.description]
        return column_names


def get_table_content(database, table):
    """
    This will print all content from the specified table of the specified database.
    """
    try:
        with sqlite3.connect(database) as sql:
            cur = sql.cursor()
            cur.execute(f"""
                        SELECT *
                        FROM {table};
                        """)
            return cur.fetchall()
    except sqlite3.Error as e:
        print(e)
    except Exception as e:
        print(e)
