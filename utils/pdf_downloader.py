import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

base_url = "https://www.dfa.ie"
path = "/irish-embassy/india/visas/processing-times-decisions-appeals/"


def pdf_downloader(folder):
    downloaded = 0
    cached = 0
    folder_path = Path(folder).joinpath("pdfs")
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
    file_paths = list()
    page = requests.get(base_url+path)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="tab2").find_all("a", href=True)[1:]
    file_name_to_path_map = {r["href"].split("/")[-1]: r['href'] for r in results}
    for filename, file_download_path in file_name_to_path_map.items():
        file_path = folder_path.joinpath(filename)
        if not file_path.exists():
            f = requests.get(base_url+file_download_path)
            with open(file_path, "wb") as fb:
                fb.write(f.content)
                downloaded += 1
        else:
            cached += 1
        file_paths.append(file_path)
        print(f"Downloaded: {downloaded}, Cached: {cached}", end="\r")
    print(f"\nTotal files: {downloaded+cached}")
    return file_paths


if __name__ == "__main__":
    print("This file cannot be run as a script.")
else:
    sys.modules[__name__] = pdf_downloader
