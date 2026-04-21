import tarfile as tf
import zipfile as zf


def find_archive_type(database: str):
    """
    Determine the type of archive, from zip or tar
    """
    try:
        if zf.is_zipfile(database):
            return "zip"
            # print(zf.is_zipfile(database))
            # print(database, "is a zipfile.")
            # with zf.ZipFile(database) as zip:
            # zip_content = zf.ZipFile.namelist(zip)
            # for item in zip_content:
            #     re_matches = re.findall("*rema1000*", item, re.IGNORECASE)
            #     print(re_matches)
        elif tf.is_tarfile(database):
            return "tar"
            # print(database, " is a tarball")
        else:
            return "unknown"
            # print(database, " is of type ", mimetypes.guess_file_type(database))

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


# print("AFU_EXTRACTION_FFS.zip: ", find_archive_type("AFU_EXTRACTION_FFS.zip"))
# print("EXTRACTION_BFU.zip: ", find_archive_type("EXTRACTION_BFU.zip"))
# print("filesystem.tar: ", find_archive_type("filesystem.tar"))
