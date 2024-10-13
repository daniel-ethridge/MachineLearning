import json
import os
import pandas as pd

lfm_data_folder = "../unsynced-data/lastfm"


def create_csv_file():
    num_files_counted = 0
    total_files = 943347

    df_dict = {}

    df = pd.DataFrame(columns=["artist", "title", "lfm_track_id", "lfm_similars", "lfm_tags"])
    for (root, dirs, files) in os.walk(lfm_data_folder):
        for file in files:
            full_path = os.path.join(root, file)
            with open(full_path, "r") as f:
                data = json.load(f)

                # JSON data loaded
                # Get similars
                similars = {}
                for sim in data["similars"]:
                    similars[sim[0]] = sim[1]

                # Get tags
                tags = []
                for tag in data["tags"]:
                    tags.append(tag[0])

                # Create DataFrame Entry
                df.loc[len(df)] = [
                    data["artist"],
                    data["title"],
                    data["track_id"],
                    similars,
                    tags
                ]

            num_files_counted += 1
            if num_files_counted % 1000 == 0:
                print(f"Status: {round(100 * num_files_counted / total_files, 2)}% complete...")
                df_dict[num_files_counted] = df
                df = pd.DataFrame(columns=["artist", "title", "lfm_track_id", "lfm_similars", "lfm_tags"])

    # Concatenate DataFrames
    num_files_counted += 1
    df_dict[num_files_counted] = df
    all_dfs = df_dict.values()
    total_df = pd.concat(all_dfs)
    total_df.to_csv("lastfm.csv")
    print(f"Status: {100 * num_files_counted / total_files}% complete...")


if __name__ == "__main__":
    create_csv_file()
