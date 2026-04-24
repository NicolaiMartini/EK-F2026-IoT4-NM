__artifacts_v2__ = {
    "rema1000_receipt": {
        "name": "rema1000 receipt",
        "description": "Extracts rema 1000 receipts from the android app 'Rema1000 | Scan & Go'. Includes location, date and time, and payment method.",
        "author": "Nicolai Martini",
        "version": "0.1",
        "date": "2026-04-24",
        "requirements": "Cellebrite UFED After First Unlock data acquisition, or similar",
        "category": "Rema1000 | Scan & Go",
        "notes": "forensics data of supermarket habit and location insights.",
        "paths": "*/Dump/data/data/dk.rema1000.app/databases/receipts.db*",
        "function": "get_receipts"
    }
}

from zoneinfo import ZoneInfo
from datetime import datetime
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import artifact_processor, open_sqlite_db_readonly

@artifact_processor
def get_receipts(files_found, report_folder, seeker, wrap_text):  
    for file_found in files_found:
        file_found = str(file_found)
        if file_found.endswith('.db'):
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
                    list_row[2] = datetime.fromtimestamp(list_row[2]/1000, tz=ZoneInfo("Europe/Copenhagen")).strftime('%Y-%m-%d %H:%M:%S') # Convert from epoch ms to cet/cest
                    entries_list.append(list_row)
                    for i in range(len(list_row)):
                        if list_row[i] is None:
                            list_row[i] = 0
                report = ArtifactHtmlReport('Rema1000 | Scan & Go Receipts')
                report.start_artifact_report(report_folder, 'Rema1000 | Scan & Go')
                report.add_script()
                data_headers = ('ID','Display ID','Payment Date','Payment Source','Store Number','Total Price','Total Price String','Total Discount','Total VAT','Chargeback',' Search Text','ZIP','PP ID','PP Card','PP Masked PAN')
                report.write_artifact_data_table(data_headers,entries_list,file_found,html_escape=False)
                report.end_artifact_report()
            else:
                logfunc('No Rema1000 | Scan & Go data available')