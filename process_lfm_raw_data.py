import json
import os
import pandas as pd

lfm_data_folder = "./data/lastfm"

if __name__ == "__main__":
    lfm_df = pd.DataFrame(columns=["artist", "title", "lfm_track_id", "lfm_similars", "lfm_tags"])
    num_files_counted = 0
    total_files = 943347
    num_write_iterations = 0

    for (root, dirs, files) in os.walk(lfm_data_folder):
        for file in files:
            full_path = os.path.join(root, file)
            with open(full_path, "r") as f:
                data = json.load(f)
                similars = {}
                for sim in data["similars"]:
                    similars[sim[0]] = sim[1]

                tags = []
                for tag in data["tags"]:
                    tags.append(tag[0])

                lfm_df.loc[len(lfm_df)] = [
                    data["artist"],
                    data["title"],
                    data["track_id"],
                    similars,
                    tags
                ]

            num_files_counted += 1
            if num_files_counted % 10000 == 0:
                print(f"Status: {round(100 * num_files_counted / total_files, 2)}% complete...")
                lfm_df.to_csv(f"./data/lfm_data.csv")

    print(f"Status: {100 * num_files_counted / total_files}% complete...")
    lfm_df.to_csv(f"./data/lfm_data.csv")
