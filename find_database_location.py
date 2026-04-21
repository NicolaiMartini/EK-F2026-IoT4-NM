import re
import zipfile as zf
import tarfile as tf
from find_archive_type import find_archive_type


def find_database_location(database, regexstring):
    """
    Find the in-archive location of desired databases.\n
    Please input a regexstring. The search is case insensitive.
    """
    try:
        re_matches = []
        if find_archive_type(database) == "zip":
            with zf.ZipFile(database) as zip:
                zip_content = zf.ZipFile.namelist(zip)
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