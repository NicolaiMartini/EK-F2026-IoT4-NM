import backend
import datetime

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
        
        print("EXTRACTING TO TEMP")
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$"):
            if database.endswith('.db'):
                print(database)
                print(backend.get_db_tables(database))
                for table in backend.get_db_tables(database):
                    print(backend.get_table_headers(database,table))
                    print(backend.get_table_content(database,table))
                print("\n")
    except Exception as e:
        print(e)