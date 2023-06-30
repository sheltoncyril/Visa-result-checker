from datetime import datetime
from pathlib import Path

import pandas as pd

from config import EMAIL_SENDER, MAIL_TO, MG_API_KEY, MG_URL, SEARCH_IDS, TEMP_FOLDER
from utils import pdf_downloader, text_search_pdfs
from utils.mg_client import MGClient

run_datetime = datetime.now()
date = run_datetime.date()
email_subject = f"Visa checker run log for {run_datetime.date()}"
trace = list()
folder_path = Path(TEMP_FOLDER)
if not folder_path.exists():
    folder_path.mkdir(parents=True, exist_ok=True)
print("Starting download")
file_paths, download_stats = pdf_downloader(folder_path)
print("Downloads complete. Processing PDFs.")
results, search_stats = text_search_pdfs(folder_path, file_paths, SEARCH_IDS)
results_file_name = "results-"+str(date)+".csv"
previous_results_file = folder_path.joinpath(results_file_name)
previous_results = None
if previous_results_file.exists() and previous_results_file.stat().st_size > 0:
    previous_results = pd.read_csv(previous_results_file, dtype="str")
results.to_csv(folder_path.joinpath(results_file_name), index=False)
results_dir = folder_path.joinpath(results_file_name)
print(f"Saved results to: {results_dir}")
not_found_message = f"No results found for IDs: {SEARCH_IDS}."
email_body = results.to_string(index=False, columns=["ID", "STATUS"],
                               col_space=20, justify="center") if not results.empty else not_found_message
email_html = results.to_html(
    index=False, justify="left") if not results.empty else not_found_message
trace.append("------------------------- run statistics -------------------------")
trace.append(f"run_datetime: {run_datetime}")
trace.append(f"results_file: {results_dir}")
trace.append(f"seached_ids: {SEARCH_IDS}")
trace.append("---------------------- download statistics ----------------------")
trace.extend(download_stats)
trace.append("----------------------- search statistics -----------------------")
trace.extend(search_stats)
trace.append("------------------------------ end ------------------------------")
email_body += "\n\n\n\n" + "\n".join(trace)
email_html += "<br/><br/><br/>" + "<br/>".join(trace)
mg_client = MGClient(api_key=MG_API_KEY, api_url=MG_URL, sender=EMAIL_SENDER)
if not results.equals(previous_results) and not results.empty:
    mg_client.send_mail(to=MAIL_TO, subject=email_subject, body=email_body, html=email_html)
else:
    print("Not sending an email as the results are unchanged.")
