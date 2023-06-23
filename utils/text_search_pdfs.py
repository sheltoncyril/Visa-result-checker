
import re
import sys
from pathlib import Path
from typing import List

import pandas as pd
from PyPDF2 import PdfReader

id_regex = re.compile("^[54][0-9]{6,10}")


def text_search_pdfs(folder, filepaths: List[Path], search_ids: List) -> pd.DataFrame:
    cached = 0
    processed = 0
    skipped = 0
    parsed_csv_folder = Path(folder).joinpath("parsed_csv")
    cache_df_file = Path(folder).joinpath("cache_df.csv")
    if cache_df_file.exists() and cache_df_file.stat().st_size > 0:
        cache_df = pd.read_csv(cache_df_file, dtype="str")
    else:
        cache_df_file.parent.mkdir(parents=True, exist_ok=True)
        cache_df_file.touch(exist_ok=True)
        cache_df = pd.DataFrame(columns=["ID", "STATUS", "REASON"])
    file_progress = 0
    total_files = len(filepaths)
    for filepath in filepaths:
        csv_filepath = parsed_csv_folder.joinpath(filepath.name).with_suffix(".csv")
        if csv_filepath.exists() and csv_filepath.stat().st_size > 0:
            df = pd.read_csv(csv_filepath, dtype="str")
            cached += 1
        else:
            csv_filepath.parent.mkdir(parents=True, exist_ok=True)
            csv_filepath.touch(exist_ok=True)
            tables = _get_tables(filepath)
            df = tables
            if tables.empty:
                skipped += 1
                continue
            df.to_csv(csv_filepath, index=False)
            processed += 1
        cache_df = pd.concat([cache_df, df], ignore_index=True)
        file_progress += 1
        print(f"File {file_progress}/{total_files} complete.", end="\r")
    cache_df.drop_duplicates(subset=["ID"], keep="last", inplace=True)
    cache_df.to_csv(cache_df_file, index=False)
    print(f"Processed PDFs: {processed}, Cached: {cached}, Skipped: {skipped}.")
    results = cache_df.loc[cache_df["ID"].isin(search_ids)]
    print(f"Found {len(results)} matching rows in {len(cache_df)} rows.")
    return results


def _get_tables(filepath: Path):

    reader = PdfReader(str(filepath))
    parsed_lines = []

    def visitor_body(text, cm, tm, fontDict, fontSize):
        y = tm[5]
        if y < 250 and text != y > -350 and text != "":
            parsed_lines.append(text)

    for page in reader.pages:
        page.extract_text(visitor_text=visitor_body)

    def line_generator(arr: List):
        idx = 0
        ar_len = len(arr)
        buf = []
        part = 1
        while arr and idx < ar_len - 1:
            text = arr[idx]
            idx += 1
            if part < 3:
                text = text.strip("\n")
            part += 1
            buf.append(text)
            if bool(id_regex.search(arr[idx])):
                if len(buf) > 3:
                    buf = [buf[0], buf[1], "".join(buf[2:-1])]
                ret = buf
                buf = []
                part = 1
                yield ret

    return pd.DataFrame(line_generator(parsed_lines), columns=["ID", "STATUS", "REASON"])


if __name__ == "__main__":
    print("This file cannot be run as a script.")
else:
    sys.modules[__name__] = text_search_pdfs
