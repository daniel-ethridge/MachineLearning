import pandas as pd

merged_df = pd.read_csv("../unsynced-data/lastfm-spotify-merged.csv").drop("Unnamed: 0", axis=1)
hot_100_df = pd.read_csv("../data/hot-100-current.csv")

hot_artists = set(hot_100_df["performer"].tolist())
hot_artists = [artist.lower() for artist in hot_artists]
hot_songs = set(hot_100_df["title"].tolist())
hot_songs = [song.lower() for song in hot_songs]
merged_df["hot_100"] = 0

for index, row in merged_df.iterrows():
    if row["title"].lower() in hot_songs:
        row["hot_100"] = 1
        if row["artist"].lower() in hot_artists:
            row["hot_100"] = 2

merged_df.to_csv("../unsynced-data/lastfm-spotify-merged.csv")
