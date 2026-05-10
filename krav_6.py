__artifacts_v2__ = {
    "rema1000_receipt": {
        "name": "Rema1000 Receipt",
        "description": "Extracts Rema1000 receipts from the android app 'Rema1000 | Scan & Go'. All raw data.",
        "author": "Nicolai Martini",
        "version": "0.1",
        "date": "2026-04-24",
        "requirements": "Cellebrite UFED After First Unlock data acquisition, or similar",
        "category": "EK F2026 IoT4 NM",
        "notes": "forensics data of supermarket habit and location insights.",
        "paths": ("*/dk.rema1000.app/databases/receipts.db*",),
        "function": "get_receipts"
    }
}

from scripts.ilapfuncs import artifact_processor, open_sqlite_db_readonly, get_file_path, logfunc

@artifact_processor
def get_receipts(files_found, report_folder, seeker, wrap_text):  
    source_path = get_file_path(files_found, "receipts.db")  
    for file_found in files_found:
        file_found = str(file_found)
        if file_found.endswith('.db'):
            data_headers = ('ID','Display ID','Payment Date','Payment Source',
                            'Store Number','Total Price','Total Price String',
                            'Total Discount','Total VAT','Chargeback',
                            'Search Text','ZIP','PP ID','PP Card','PP Masked PAN')
            db = open_sqlite_db_readonly(file_found)
            cur = db.cursor()
            cur.execute(f"""
                        SELECT *
                        FROM ReceiptEntity;
                        """)
            rows=cur.fetchall()
            entries=len(rows)
            if entries>0:
                entries_list=[]
                for row in rows:
                    list_row=list(row)
                    for i in range(len(list_row)):
                        if list_row[i] is None:
                            list_row[i]=0
                    entries_list.append(list_row)
                return data_headers, entries_list, source_path
            else:
                logfunc('No Rema1000 | Scan & Go data available')