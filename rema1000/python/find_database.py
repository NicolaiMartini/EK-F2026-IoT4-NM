"""
Krav: Udhent Rema1000 database fra datasikring
Accepttest: Det skal være muligt at udhente specifikt Rema1000 databaser fra datasikringen fra UFED eller Android Triage, uden overflødige irrelevante filer.

Hvis dette gøres sucesfuldt 8 ud af 10 gange, anses kravet som opfyldt.
"""

import re
from zipfile import ZipFile as zf
import mimetypes

def find_database(database):
    try:
        kind = mimetypes.guess_file_type(database)
        print(kind)
        # with zf(database) as zip:
        #     zip_content = zf.namelist(zip)
        #     for i in zip_content:
        #         matches = re.findall("*rema1000*", i, re.IGNORECASE)
        #         print(matches)
    except Exception as e:
        print(e)


print(f"AFU: {find_database("AFU_EXTRACTION_FFS.zip")}")
find_database("EXTRACTION_BFU.zip")
find_database("filesystem.tar")


# with zf("AFU_EXTRACTION_FFS.zip") as z:
#     AFU_content = zf.namelist(AFU)
#     for i in AFU_content:
#         print(i)
