import re
import os
import tarfile as tf
from zipfile import is_zipfile,ZipFile


def find_archive_type(database: str):
    """
    Determine the type of archive, from zip or tar
    """
    try:
        if is_zipfile(database):
            return "zip"
        elif tf.is_tarfile(database):
            return "tar"
        else:
            return "unknown"
    except Exception as e:
        print(e)


def find_database_location(database, regexstring):
    """
    Find the in-archive location of desired databases.\n
    Please input a regexstring. The search is case insensitive.
    """
    try:
        re_matches = []
        if find_archive_type(database) == "zip":
            with ZipFile(database) as zip:
                zip_content = ZipFile.namelist(zip)
                for item in zip_content:
                    match=re.search(regexstring, item, re.IGNORECASE)
                    if match:
                        re_matches.append(match.group())
            return "zip", re_matches
        elif find_archive_type(database) == "tar":
            with tf.open(database) as tarball:
                tar_content = tarball.getnames()
                for item in tar_content:
                    match = re.search(regexstring, item, re.IGNORECASE)
                    if match:
                        re_matches.append(match.group())
            return "tar", re_matches
    except Exception as e:
        print(e)


def extract_known_databases(database:str,regex_string:str,output_directory:str):
    """
    Extract the databases to the provided output_directory. Make sure the output directory already exists. \n
    Please input a regexstring. The search is case insensitive.
    """
    try:
        databases=find_database_location(database,regex_string)
        if databases[0] == "zip":
            with ZipFile(database) as extract_zip:
                for item in databases[1]:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        continue
                    print(f"Extracting: {item_path}")
                    extract_zip.extract(member=item,path=output_directory)

        elif databases[0] == "tar":
            with tf.open(database) as extract_tar:
                for item in databases[1]:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        continue
                    print(f"Extracting: {item_path}")
                    extract_tar.extract(member=item,path=output_directory)
    except Exception as e:
        print(e)