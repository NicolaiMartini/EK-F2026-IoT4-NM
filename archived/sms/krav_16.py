__artifacts_v2__ = {
    "android_sms": {
        "name": "Android SMS PoC",
        "description": "Extract SMS from Android, convert timestamp to UTC ISO 8601.",
        "author": "Nicolai Martini",
        "version": "0.1",
        "date": "2026-05-04",
        "requirements": "Cellebrite UFED After First Unlock data acquisition, or similar",
        "category": "EK F2026 IoT4 NM",
        "notes": "PoC for extracting SMS from Android MMSSMS database",
        "paths": ("*/com.android.providers.telephony/databases/mmssms.db*",),
        "function": "get_sms"
    }
}

from zoneinfo import ZoneInfo
from datetime import datetime
from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import artifact_processor, open_sqlite_db_readonly

@artifact_processor
def get_sms(files_found, report_folder, seeker, wrap_text):  
    for file_found in files_found:
        file_found = str(file_found)
        if file_found.endswith('.db'):
            db = open_sqlite_db_readonly(file_found)
            cur = db.cursor()
            cur.execute(f"""
                        SELECT *
                        FROM sms;
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
                    list_row[5] = datetime.fromtimestamp(list_row[5]/1000, tz=ZoneInfo("UTC")).strftime('%Y-%m-%dT%H:%M:%SZ')
                    entries_list.append(list_row)
                report = ArtifactHtmlReport('Android SMS database')
                report.start_artifact_report(report_folder, 'SMS Android Proof of Concept')
                report.add_script()
                data_headers = ('_id', 'thread_id', 'address', 'person', 'date', 'date_sent', 'protocol', 'read', 'status', 'type', 'reply_path_present', 'subject', 'body', 'service_center', 'locked', 'sub_id', 'error_code', 'creator', 'seen', 'priority')
                report.write_artifact_data_table(data_headers,entries_list,file_found,html_escape=False)
                report.end_artifact_report()
            else:
                logfunc('No android sms data avilable.')