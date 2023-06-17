from pathlib import Path

import pdf_downloader
import search_pdfs

FOLDER = "./temp"
SEARCH_IDS = []

folder_path = Path(FOLDER)
if not folder_path.exists():
    folder_path.mkdir(parents=True, exist_ok=True)
print("Starting download")
file_paths = pdf_downloader(folder_path)
print("Downloads complete. Processing PDFs.")
results = search_pdfs(folder_path, file_paths, SEARCH_IDS)
print("Processed PDFs.")
results.to_csv(folder_path.joinpath("results.csv"), index=False)
print(f"Saved results to: {folder_path.joinpath('results.csv')}")
