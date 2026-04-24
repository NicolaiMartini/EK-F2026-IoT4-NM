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

import re
import json

from scripts.ilapfuncs import artifact_processor, open_sqlite_db_readonly

def get_receipts(files_found, report_folder, seeker, wrap_text):  
    for file_found in files_found:
        file_found = str(file_found)
        if file_found.endswith('.db'):
            db = open_sqlite_db_readonly(file_found)
            cur = db.cursor()
            cur.execute(f"""
                        SELECT *
                        FROM ReceiptEntity
                        """)
            print(cur.fetchall())