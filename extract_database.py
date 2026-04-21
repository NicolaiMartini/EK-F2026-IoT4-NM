import zipfile as zf
import tarfile as tf
from find_database_location import find_database_location

def extract_known_databases(database:str,regex_string:str,output_directory:str):
    """
    Extract the databases to the provided output_directory. Make sure the output directory already exists. \n
    Please input a regexstring. The search is case insensitive.
    """
    databases=find_database_location(database,regex_string)
    if databases[0] == "zip":
        print("DATABASE IS ZIP")
        for item in databases[1]:
            print(item)
    elif databases[0] == "tar":
        print("DATABASE IS TAR")
        with tf.open(database) as extract_tar:
            for item in databases[1]:
                print(item)
                extract_tar.extract(item,output_directory)