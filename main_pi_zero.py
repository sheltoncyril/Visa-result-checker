#! /usr/bin/python3

from datetime import datetime
from pathlib import Path

import pandas as pd

from config import SEARCH_IDS, TEMP_FOLDER
from utils import pdf_downloader, text_search_pdfs
from utils.common import CommonUtils

c = CommonUtils()
print_delay = c.print_delay
buzz = c.buzz
print_delay("Visa result checker", 2)
buzz(0.05, 2, 0.1)
run_datetime = datetime.now()
date = run_datetime.date()
trace = list()
folder_path = Path(TEMP_FOLDER)
if not folder_path.exists():
    folder_path.mkdir(parents=True, exist_ok=True)
print_delay("Starting download")
buzz(0.05, 2, 0.1)
file_paths, download_stats = pdf_downloader(folder_path)
print_delay("", 0)
for l, k in enumerate(download_stats):
    print_delay(k, pre_clear=False, line=l)
print_delay("Downloads complete. Processing PDFs.")
buzz(0.05, 2, 0.1)
results, search_stats = text_search_pdfs(folder_path, file_paths, SEARCH_IDS)
print_delay("", 0)
for l, k in enumerate(search_stats):
    print_delay(k, pre_clear=False, line=l)
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
print_delay(f"IDs: {SEARCH_IDS}", pre_clear=False, line=1)
# print_delay(f"Saved results to: {results_dir}", line=2)
buzz()
