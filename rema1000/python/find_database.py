"""
Krav: Udhent Rema1000 database fra datasikring
Accepttest: Det skal være muligt at udhente specifikt Rema1000 databaser fra datasikringen fra UFED eller Android Triage, uden overflødige irrelevante filer.

Hvis dette gøres sucesfuldt 8 ud af 10 gange, anses kravet som opfyldt.
"""

import re
import mimetypes
import tarfile as tf
import zipfile as zf

def find_database_type(database:str):
    try:
        if zf.is_zipfile(database):
            return "zip"
            print(zf.is_zipfile(database))
            print(database, "is a zipfile.")
            # with zf.ZipFile(database) as zip:
                # zip_content = zf.ZipFile.namelist(zip)
                # for item in zip_content:
                #     re_matches = re.findall("*rema1000*", item, re.IGNORECASE)
                #     print(re_matches)
        elif tf.is_tarfile(database):
            return "tar"
            print(database, " is a tarball")
        else:
            return "unknown"
            print(database, " is of type ", mimetypes.guess_file_type(database))


        # kind = mimetypes.guess_file_type(database)
        # # print(database, kind[0])
        # if "zip" in kind[0]:
        #     with zf(database) as zip:
        #         zip_content = zf.namelist(zip)
        #         for i in zip_content:
        #             matches = re.findall("*rema1000*", i, re.IGNORECASE)
        #             print(matches)
        # elif "tar" in kind[0]:
        #     with tf.open("")
    except Exception as e:
        print(e)


find_database_type("AFU_EXTRACTION_FFS.zip")
# find_database_type("EXTRACTION_BFU.zip")
# find_database_type("filesystem.tar")