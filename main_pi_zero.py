#! /usr/bin/python3

from datetime import datetime
from pathlib import Path

import pandas as pd

from config import SEARCH_IDS, TEMP_FOLDER
from utils import pdf_downloader, text_search_pdfs
from utils.common import CommonUtils

print_delay = CommonUtils().print_delay
print_delay("Visa result checker", 2)
run_datetime = datetime.now()
date = run_datetime.date()
trace = list()
folder_path = Path(TEMP_FOLDER)
if not folder_path.exists():
    folder_path.mkdir(parents=True, exist_ok=True)
print_delay("Starting download", clear_post=True)
file_paths, download_stats = pdf_downloader(folder_path)
for k, l in enumerate(download_stats):
    print_delay(f"{k}: {download_stats[k]}", pre_clear=False, line=l)
print_delay("Downloads complete. Processing PDFs.")
results, search_stats = text_search_pdfs(folder_path, file_paths, SEARCH_IDS)
for k, l in enumerate(search_stats):
    print_delay(f"{k}: {search_stats[k]}", pre_clear=False, line=l)
results_file_name = "results-"+str(date)+".csv"
previous_results_file = folder_path.joinpath(results_file_name)
previous_results = None
if previous_results_file.exists() and previous_results_file.stat().st_size > 0:
    previous_results = pd.read_csv(previous_results_file, dtype="str")
results.to_csv(folder_path.joinpath(results_file_name), index=False)
results_dir = folder_path.joinpath(results_file_name)
if results.empty:
    print_delay(f"No results found.")
elif results.equals(previous_results):
    print_delay(f"No change in results.")
else:
    print_delay(f"Found results for IDs.")
print_delay(f"Saved results to: {results_dir}", line=2)