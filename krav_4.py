import sqlite3
import backend
from zoneinfo import ZoneInfo
from datetime import datetime
from time import sleep

SEARCH_STRING=r".*rema1000.*\/databases\/.*\.db.*$"
ARCHIVE="AFU.zip"
TABLE="ReceiptEntity"

if __name__ == "__main__":
    try:
        available_products=[]
        purchased_products=[]
        for database in backend.get_known_databases(ARCHIVE,SEARCH_STRING):
            if database.endswith('shopdatabase.db'):
                with sqlite3.connect(database) as sql:
                    cur=sql.cursor()
                    cur.execute(f"""
                            SELECT shelfText1
                            FROM ProductEntity;
                            """)
                for product in cur.fetchall():
                    product=product[0].replace("Å","A")
                    product=product.replace(".","")
                    available_products.append(product.lower())
                    
            if database.endswith('receipts.db'):
                with sqlite3.connect(database) as sql:
                    cur=sql.cursor()
                    cur.execute(f"""
                                SELECT paymentDate, paymentSource,
                                totalPrice, searchText, zipString,
                                pp_cardType, pp_maskedPan
                                FROM {TABLE};
                                """)
                    for receipt in cur.fetchall():
                        location=f"{receipt[3].split(";")[1].capitalize()}, {receipt[4]}, {receipt[3].split(";")[2].capitalize()}"
                        date_time=f"{datetime.fromtimestamp(receipt[0]/1000, tz=ZoneInfo("Europe/Copenhagen")).strftime('%Y-%m-%d %H:%M:%S')}, local time"
                        items=receipt[3].split(";")[3:]
                        receipt_items=[item for item in items if item in available_products]
                        print(f"""
                              Date and time: {date_time}
                              Location: {location}
                              Items: {receipt_items}
                              Total price: {receipt[2]/100:.2f}
                              Payment card: {receipt[1]}
                              Card type: {receipt[5]}
                              Card PAN: {receipt[6]}
                              """)                                
    except Exception as e:
        print(e)