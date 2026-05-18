import sqlite3
import backend
import folium
import datetime
import pandas as pd


if __name__ == "__main__":
    try:
        store_locations=[]
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*receipts\.db.*$"):
            if database.endswith('.db'):
                with sqlite3.connect(database) as sql:
                    cur = sql.cursor()
                    cur.execute(f"""
                                SELECT storeNumber
                                FROM ReceiptEntity;
                                """)
                    receipt_info = cur.fetchall()
                    cur.execute(f"""
                                SELECT storeNumber, ownerName, address1, zip, city, latitude, longitude
                                FROM ReceiptStoreEntity
                                """)
                    store_info = cur.fetchall()
                    for receipt in receipt_info:
                        for store in store_info:
                            if receipt[0] in store[0]:
                                store_locations.append({"Store number":f"{store[0]}",
                                                        "Store owner":f"{store[1]}",
                                                        "Store location":f"{store[2]}, {store[3]}, {store[4]}",
                                                        "lat":float(store[5]),
                                                        "lon":float(store[6])})
                    df=pd.DataFrame(store_locations)
                    m=folium.Map(location=[55.8619722, 10.5931944],zoom_start=7,control_scale=True)
                    pins=[]
                    for store in store_locations:
                        if store["Store number"] in pins:
                            continue
                        else:
                            popup=folium.Popup(f"""Store owner: {store["Store owner"]}<br>
                                Store number: {store["Store number"]}<br>
                                Address: {store["Store location"]}<br>
                                Coordinates: {store["lat"]} {store["lon"]}<br>
                                """,min_width=200,max_width=500)
                            folium.Marker(
                                location=[store["lat"],store["lon"]],
                                popup=popup,
                                min_width=(1000),
                                icon=folium.Icon(color="purple")
                                ).add_to(m)
                            pins.append(store["Store number"])
                    m.save(f"krav_09_{datetime.datetime.now()}.html")
    except Exception as e:
        print(e)