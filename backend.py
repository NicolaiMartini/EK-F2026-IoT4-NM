import re
import os
import tarfile
import zipfile
import sqlite3


def find_archive_type(archive: str):
    """
    Determine the type of archive, from zip or tar
    """
    try:
        if zipfile.is_zipfile(archive):
            return "zip"
        elif tarfile.is_tarfile(archive):
            return "tar"
        else:
            return "unknown"
    except Exception as e:
        print(e)


def find_database_location(archive, regexstring):
    """
    Find the in-archive location of desired databases.\n
    Please input a regexstring to search inside the archive. The search is case insensitive.
    """
    try:
        re_matches = []
        if find_archive_type(archive) == "zip":
            with zipfile.ZipFile(archive) as zip:
                zip_content = zipfile.ZipFile.namelist(zip)
                for item in zip_content:
                    match = re.search(regexstring, item, re.IGNORECASE)
                    if match:
                        re_matches.append(match.group())
            return "zip", re_matches
        elif find_archive_type(archive) == "tar":
            with tarfile.open(archive) as tarball:
                tar_content = tarball.getnames()
                for item in tar_content:
                    match = re.search(regexstring, item, re.IGNORECASE)
                    if match:
                        re_matches.append(match.group())
            return "tar", re_matches
    except Exception as e:
        print(e)


def extract_known_databases(archive: str, regex_string: str, output_directory: str):
    """
    Extract the databases to the provided output_directory. Make sure the output directory already exists. \n
    Please input a regexstring. The search is case insensitive.
    """
    try:
        databases = find_database_location(archive, regex_string)
        if databases[0] == "zip":
            with zipfile.ZipFile(archive) as extract_zip:
                for item in databases[1]:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        continue
                    print(f"Extracting: {item_path}")
                    extract_zip.extract(member=item, path=output_directory)

        elif databases[0] == "tar":
            with tarfile.open(archive) as extract_tar:
                for item in databases[1]:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        continue
                    print(f"Extracting: {item_path}")
                    extract_tar.extract(member=item, path=output_directory)
    except Exception as e:
        print(e)


def list_dir_recursively(directory):
    """
    Retrieve the contents of a directory, recursively. \n
    Will list both dirs and files.
    """
    try:
        contents = []
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                continue
                # contents.append(os.path.join(root, name))
            for name in files:
                contents.append(os.path.join(root, name))
        return contents
    except Exception as e:
        return e


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
            tables = [
                row[0] for row in cur.fetchall()
            ]  # fetch only first item in 1-item tuple, of each row
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


def retrieve_db_table_content(database, table):
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
