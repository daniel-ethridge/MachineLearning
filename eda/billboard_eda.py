import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


def main():

    # Get DataFrame
    df = pd.read_csv("./data/hot-100-current.csv")

    # Create reduced dataframe to plot
    artists = df["performer"]
    artist_counts = artists.value_counts().reset_index()
    reduced_artist_counts = artist_counts.loc[:49]

    # Plot top 50 artists
    fig = plt.figure()
    ax = fig.add_subplot()
    sns.barplot(reduced_artist_counts, x="performer", y="count", ax=ax)
    ax.set_xticks(ax.get_xticks())
    ax.set_xlabel("Performer")
    ax.set_ylabel("Counts")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    fig.suptitle("Top 50 Artists with the Most Weeks on the Billboard Hot 100")
    plt.tight_layout()
    plt.show()

    # Create bar plot of Weeks on chart for song
    weeks_on_chart = df["wks_on_chart"]
    perf_count = dict(Counter(weeks_on_chart))

    red_pos_count = perf_count.copy()
    for key, value in perf_count.items():
        if value < 445:
            del red_pos_count[key]

    keys = list(red_pos_count.keys())
    vals = [red_pos_count[k] for k in keys]
    sns.barplot(x=keys, y=vals)
    plt.xticks(rotation=75)
    plt.xlabel("Number of Weeks")
    plt.ylabel("Counts")
    plt.title("Weeks on the Chart for a Song")
    plt.tight_layout()
    plt.show()

    # Create bar plot of Weeks on chart for song
    peak_positions = df["peak_pos"]
    pos_count = dict(Counter(peak_positions))

    red_pos_count = pos_count.copy()
    for key, value in pos_count.items():
        if value < 445:
            del red_pos_count[key]

    keys = list(red_pos_count.keys())
    vals = [red_pos_count[k] for k in keys]
    sns.barplot(x=keys, y=vals)
    plt.xticks(rotation=75)
    plt.xlabel("Position")
    plt.ylabel("Counts")
    plt.title("Peak Positions")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
