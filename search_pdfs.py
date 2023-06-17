
import sys
from pathlib import Path
from typing import List

import camelot
import pandas as pd


def search_pdfs(folder, filepaths: List[Path], search_ids: List) -> pd.DataFrame:
    cached = 0
    processed = 0
    skipped = 0
    parsed_csv_folder = Path(folder).joinpath("parsed_csv")
    cache_df_file = Path(folder).joinpath("cache_df.csv")
    if cache_df_file.exists() and cache_df_file.stat().st_size > 0:
        cache_df = pd.read_csv(cache_df_file, dtype="str")
    else:
        cache_df_file.parent.mkdir(parents=True, exist_ok=True)
        cache_df_file.touch()
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
            tables = camelot.read_pdf(str(filepath),
                                      pages="all")
            if not tables:
                skipped += 1
                continue
            df = pd.concat([table.df for table in tables], ignore_index=True)
            df.columns = ["ID", "STATUS", "REASON"]
            df = df[1:]  # Remove first line of dataframe as it contains the names of columns
            df.to_csv(csv_filepath, index=False)
            processed += 1
        cache_df = pd.concat([cache_df, df], ignore_index=True)
        file_progress += 1
        print(f"File {file_progress}/{total_files} complete.", end="\r")
    cache_df.drop_duplicates(subset=["ID"], keep="last", inplace=True)
    cache_df.to_csv(cache_df_file, index=False)
    print(f"Processed: {processed}, Cached: {cached}, Skipped: {skipped}.")
    results = cache_df.loc[cache_df["ID"].isin(search_ids)]
    print(f"Found {len(results)} matching rows in {len(cache_df)} rows.")
    return results


if __name__ == "__main__":
    print("This file cannot be run as a script.")
else:
    sys.modules[__name__] = search_pdfs
