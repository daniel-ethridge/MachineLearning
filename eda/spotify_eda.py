import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

'''
spotify_id           object
lastfm_id            object
acousticness        float64
danceability        float64
energy              float64
instrumentalness    float64
loudness            float64
speechiness         float64
valence             float64
tempo               float64
mode                  int64
'''


def create_cut_plot(dataframe, column: str):
    """
    Create a bar chart of the binned audio features
    :param dataframe: Spotify data
    :param column: Column name
    """
    dataframe["cut"], bins = pd.cut(dataframe[column], 10, include_lowest=True, retbins=True, right=True)
    if column != "loudness":
        for i, val in enumerate(bins):
            if val < 0:
                bins[i] = 0

    labels = [f'({round(a, 2)}, {round(b, 2)}]' for a, b in zip(bins, bins[1:])]
    
    fig, ax = plt.subplots()
    sns.countplot(data=dataframe, x="cut")

    ax.set_xticks(ax.get_xticks(), labels=labels, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_ylabel(f"Count")
    if column == "loudness":
        ax.set_xlabel(f"{column.capitalize()} (decibels)")
    elif column == "tempo":
        ax.set_xlabel(f"{column.capitalize()} (beats per minute)")
    else:
        ax.set_xlabel(f"{column.capitalize()}")

    if column == "mode":
        ax.set_title("Mode Ratings")
    else:
        ax.set_title(f"Binned {column.capitalize()} Ratings")
    plt.tight_layout()
    plt.show()

    # Uncomment the lines below to save the plot
    # save_path = ""  # Directory and file name of where to save the plot
    # plt.savefig(save_path)


def main():
    # import spotify data
    orig_spotify = pd.read_csv("unsynced-data/spotify.csv", index_col=0).drop("manual_check", axis=1)
    df = orig_spotify.copy()

    print(df.dtypes)
    df_box = df.drop(columns=["spotify_id", "lastfm_id", "tempo", "mode", "loudness"])
    df_long = pd.melt(df_box, var_name='column', value_name='value')
    sns.boxplot(df_long, x='column', y='value')
    plt.xticks(rotation=45)
    plt.xlabel("Spotify Features")
    plt.ylabel("Value")
    plt.title("Comparison of Select Spotify Features")
    plt.tight_layout()
    plt.show()

    for key in df.keys():
        if df[key].dtype == np.float64:
            create_cut_plot(df, key)


    sns.countplot(df, x="mode")
    plt.title("Mode Ratings")
    plt.xlabel("Mode")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    # Uncomment the lines below to save the plot
    # save_path = ""  # Directory and file name of where to save the plot
    # plt.savefig(save_path)

if __name__ == "__main__":
    main()
