import re
import os
import tarfile
import zipfile
import tempfile


def find_archive_type(database: str):
    """
    Determine the type of archive, from zip or tar
    """
    try:
        if zipfile.is_zipfile(database):
            return "zip"
        elif tarfile.is_tarfile(database):
            return "tar"
        else:
            return "unknown"
    except Exception as e:
        print(e)


def find_database_location(database, regexstring):
    """
    Find the in-archive location of desired databases.\n
    Please input the archive to search through.\n
    Please input a regexstring to search inside the archive. The search is case insensitive.
    """
    try:
        re_matches = []
        if find_archive_type(database) == "zip":
            with zipfile.ZipFile(database) as zip:
                zip_content = zipfile.ZipFile.namelist(zip)
                for item in zip_content:
                    match=re.search(regexstring, item, re.IGNORECASE)
                    if match:
                        re_matches.append(match.group())
            return "zip", re_matches
        elif find_archive_type(database) == "tar":
            with tarfile.open(database) as tarball:
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
            with zipfile.ZipFile(database) as extract_zip:
                for item in databases[1]:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        continue
                    print(f"Extracting: {item_path}")
                    extract_zip.extract(member=item,path=output_directory)

        elif databases[0] == "tar":
            with tarfile.open(database) as extract_tar:
                for item in databases[1]:
                    item_path = os.path.join(output_directory, item)
                    if os.path.exists(item_path):
                        print(f"skipping '{item} - already exists")
                        continue
                    print(f"Extracting: {item_path}")
                    extract_tar.extract(member=item,path=output_directory)
    except Exception as e:
        print(e)


# Not really useful.
def temp_extract_databases(database:str,regex_string:str,should_delete=True):
    """
    Extract files to temporary directory. \n
    Please input a regexstring. The search is case insensitive. \n
    Will destroy itself immediately after extracting. pass should_delete=False to disable deletion.
    """
    try:
        with tempfile.TemporaryDirectory(delete=should_delete) as tmpdir:
            extract_known_databases(database,regex_string,tmpdir)
    except Exception as e:
        print(e)