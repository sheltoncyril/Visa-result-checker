from datetime import datetime
from pathlib import Path

from config import EMAIL_SENDER, MAIL_TO, MG_API_KEY, MG_URL, SEARCH_IDS, TEMP_FOLDER
from utils import pdf_downloader, text_search_pdfs
from utils.mg_client import MGClient

run_datetime = datetime.now()
email_subject = f"Visa checker run log for {run_datetime.date()}"
folder_path = Path(TEMP_FOLDER)
if not folder_path.exists():
    folder_path.mkdir(parents=True, exist_ok=True)
print("Starting download")
file_paths = pdf_downloader(folder_path)
print("Downloads complete. Processing PDFs.")
results = text_search_pdfs(folder_path, file_paths, SEARCH_IDS)
results.to_csv(folder_path.joinpath("results.csv"), index=False)
print(f"Saved results to: {folder_path.joinpath('results.csv')}")
email_body = results.to_string(index=False, columns=["ID", "STATUS"],
                               col_space=20, justify="center") if not results.empty else "No results found."
email_html = results.to_html(index=False, justify="left") if not results.empty else "No results found."
trace = ["--------------------- stats ---------------------",
         f"run_datetime: {run_datetime}",
         f"temp_working_dir: {TEMP_FOLDER}",
         f"seached_ids: {SEARCH_IDS}",
         "-------------------------------------------------"
         ]
email_body += "\n\n\n\n" + "\n".join(trace)
email_html += "<br/><br/><br/>" + "<br/>".join(trace)
mg_client = MGClient(api_key=MG_API_KEY, api_url=MG_URL, sender=EMAIL_SENDER)
mg_client.send_mail(to=MAIL_TO, subject=email_subject, body=email_body, html=email_html)
