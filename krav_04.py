import sqlite3
import backend

if __name__ == "__main__":
    try:
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*\.db.*$"):
            if database.endswith('receipts.db'):
                with sqlite3.connect(database) as sql:
                    cur=sql.cursor()
                    cur.execute(f"""
                                SELECT paymentDate, paymentSource,
                                totalPrice, searchText, zipString,
                                pp_cardType, pp_maskedPan
                                FROM ReceiptEntity;
                                """)
                    for item in cur.fetchall():
                        print(f"""
                              paymentDate: {item[0]}
                              paymentSource: {item[1]}
                              totalPrice: {item[2]}
                              searchText: {item[3]}
                              zipString: {item[4]}
                              pp_cardType: {item[5]}
                              pp_maskedPan:{item[6]}
                              """)              
    except Exception as e:
        print(e)