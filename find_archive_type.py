import tarfile as tf
import zipfile as zf


def find_archive_type(database: str):
    """
    Determine the type of archive, from zip or tar
    """
    try:
        if zf.is_zipfile(database):
            return "zip"
        elif tf.is_tarfile(database):
            return "tar"
        else:
            return "unknown"
    except Exception as e:
        print(e)