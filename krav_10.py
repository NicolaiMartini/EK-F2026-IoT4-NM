import sqlite3
import backend
import folium
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd


if __name__ == "__main__":
    try:
        store_locations=[]
        for database in backend.get_known_databases("AFU.zip",r".*rema1000.*\/databases\/.*receipts\.db.*$"):
            if database.endswith('.db'):
                with sqlite3.connect(database) as sql:
                    cur = sql.cursor()
                    cur.execute(f"""
                                SELECT paymentDate, storeNumber
                                FROM ReceiptEntity;
                                """)
                    receipt_info = cur.fetchall()
                    cur.execute(f"""
                                SELECT storeNumber, ownerName, address1, zip, city, latitude, longitude
                                FROM ReceiptStoreEntity
                                """)
                    store_info = cur.fetchall()
                    visit_amounts={}
                    visit_dates={}
                    for receipt in receipt_info:
                        for store in store_info:
                            if receipt[1] in store[0]:
                                visit_amounts[receipt[1]]=visit_amounts.get(receipt[1],0)+1
                                converted_timestamp=datetime.fromtimestamp(receipt[0]/1000,tz=ZoneInfo("Europe/Copenhagen")).strftime("%Y-%m-%d %H:%M:%S")
                                visit_dates.setdefault(store[0],[]).append(converted_timestamp)
                                store_locations.append({"Store number":f"{store[0]}",
                                                        "Store owner":f"{store[1]}",
                                                        "Store location":f"{store[2]}, {store[3]}, {store[4]}",
                                                        "Visit date":converted_timestamp,
                                                        "lat":float(store[5]),
                                                        "lon":float(store[6])})
                    df=pd.DataFrame(store_locations)
                    m=folium.Map(location=[55.8619722, 10.5931944],zoom_start=7,control_scale=True)
                    pins=[]
                    for store in store_locations:
                        if store["Store number"] in pins:
                            continue
                        else:
                            visit_date_string=""
                            for keys,dates_list in visit_dates.items():
                                for value in visit_dates.get(store["Store number"]):
                                    if value in visit_date_string:
                                        continue
                                    else:
                                        visit_date_string+=f"{value}<br>"
                            popup=folium.Popup(f"""<b>Store owner</b>: {store["Store owner"]}<br>
                                <b>Store number</b>: {store["Store number"]}<br>
                                <b>Address</b>: {store["Store location"]}<br>
                                <b>No. visits</b>: {visit_amounts.get(store["Store number"])}<br>
                                <b>Coordinates</b>: {store["lat"]} {store["lon"]}<br>
                                <b>Visit dates</b>: <br>{visit_date_string}
                                """,min_width=200,max_width=500)
                            folium.Marker(
                                location=[store["lat"],store["lon"]],
                                popup=popup,
                                min_width=(1000),
                                icon=folium.Icon(color="purple")
                                ).add_to(m)
                            pins.append(store["Store number"])
                    m.save(f"krav_10_{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}.html")
    except Exception as e:
        print(e)