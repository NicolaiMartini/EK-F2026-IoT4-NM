import sqlite3
import backend
from zoneinfo import ZoneInfo
from datetime import datetime

SEARCH_STRING=r".*rema1000.*\/databases\/.*receipts\.db.*$"
ARCHIVE="AFU.zip"
TABLE="ReceiptEntity"

if __name__ == "__main__":
    try:
        for database in backend.get_known_databases(ARCHIVE,SEARCH_STRING):
            if database.endswith('.db'):
                print(database)
                print(backend.get_table_headers(database,TABLE))
                with sqlite3.connect(database) as sql:
                    cur=sql.cursor()
                    cur.execute(f"""
                                SELECT paymentDate, paymentSource,
                                totalPrice, searchText, zipString,
                                pp_cardType, pp_maskedPan
                                FROM {TABLE};
                                """)
                    for item in cur.fetchall():
                        print(f"""
                              Date and time: {datetime.fromtimestamp(item[0]/1000, tz=ZoneInfo("Europe/Copenhagen")).strftime('%Y-%m-%d %H:%M:%S')}
                              Location: {item[3].split(";")[1].capitalize()}, {item[4]}, {item[3].split(";")[2].capitalize()}
                              """)
                            #   Items: {item[4].split(";")[3:]}
                            #   Total price: {item[2]/100:.2f}
                              
                            #   Payment card: {item[1]}
                            #   """)
    except Exception as e:
        print(e)