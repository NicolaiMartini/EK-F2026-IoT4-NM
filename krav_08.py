import sqlite3
import backend
from zoneinfo import ZoneInfo
from datetime import datetime


if __name__ == "__main__":
    try:
        store_locations=[]
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$"):
            if database.endswith('shopdatabase.db'):
                with sqlite3.connect(database) as sql:
                    cur=sql.cursor()
                    cur.execute(f"""
                            SELECT storeNumber, address1, zip, city, latitude, longitude
                            FROM StoreEntity;
                            """)
                for store in cur.fetchall():
                    store_locations.append(store)      
                    
            if database.endswith('receipts.db'):
                with sqlite3.connect(database) as sql:
                    cur=sql.cursor()
                    cur.execute(f"""
                                SELECT paymentDate, storeNumber
                                FROM ReceiptEntity;
                                """)
                    for receipt in cur.fetchall():
                        for store in store_locations:
                            if receipt[1] in store[0]:
                                print(f"""
                                      Date and time:    {datetime.fromtimestamp(receipt[0]/1000,tz=ZoneInfo("Europe/Copenhagen")).strftime("%Y-%m-%d %H:%M:%S")}
                                      Store number:     {store[0]}
                                      Store location:   {store[1]}, {store[2]}, {store[3]}
                                      GPS, lat-long:    {store[4]}° {store[5]}°
                                      """)
    except Exception as e:
        print(e)