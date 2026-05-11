import backend
import datetime
from time import sleep

if __name__ == "__main__":
    try:
        print("EXTRACTING TO SPECIFIED LOCATION")
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$",f"/tmp/{datetime.datetime.now()}/"):
            if database.endswith('.db'):
                print(database)
                print(backend.get_db_tables(database))
                for table in backend.get_db_tables(database):
                    print(backend.get_table_headers(database,table))
                    print(backend.get_table_content(database,table))
                print("\n")
                sleep(2)
        print("EXTRACTING TO TEMP")
        sleep(2)
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$"):
            if database.endswith('.db'):
                print(database)
                print(backend.get_db_tables(database))
                for table in backend.get_db_tables(database):
                    print(backend.get_table_headers(database,table))
                    print(backend.get_table_content(database,table))
                print("\n")
                sleep(2)
    except Exception as e:
        print(e)