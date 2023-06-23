from pathlib import Path

from utils import pdf_downloader, text_search_pdfs

FOLDER = "./temp"
SEARCH_IDS = ["58396322"]

folder_path = Path(FOLDER)
if not folder_path.exists():
    folder_path.mkdir(parents=True, exist_ok=True)
print("Starting download")
file_paths = pdf_downloader(folder_path)
print("Downloads complete. Processing PDFs.")
results = text_search_pdfs(folder_path, file_paths, SEARCH_IDS)
results.to_csv(folder_path.joinpath("results.csv"), index=False)
print(f"Saved results to: {folder_path.joinpath('results.csv')}")
