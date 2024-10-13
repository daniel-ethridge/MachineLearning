from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def perform_pca(csv_file, axes_to_drop: list, n_components=None):
    # pd.set_option("display.max_columns", None)

    # Read in data
    orig = pd.read_csv(csv_file)
    df = orig.copy()
    df = df.drop(axes_to_drop, axis=1)

    df = df.dropna()

    # Perform scaling
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)

    # perform pca
    pca = PCA()
    pca_out = pca.fit_transform(scaled_df)

    shape = pca.components_.shape[0]
    feature_names = list(df.columns)

    most_important = [np.abs(pca.components_[i]).argmax() for i in range(shape)]
    most_important_names = [feature_names[most_important[i]] for i in range(shape)]

    feat_dict = {f"PC{i}": most_important_names[i] for i in range(shape)}
    important_df = pd.DataFrame(feat_dict.items())

    data_dict = {
        "transformed_data": pca_out,
        "eigenvalues": pca.explained_variance_,
        "relative_eigenvalues": pca.explained_variance_ratio_,
        "important_features": important_df
    }

    return data_dict


def create_spotify_eigenvalue_chart(pca_data):
    bottom = 0
    i = 1
    for eigenvalue in pca_data["relative_eigenvalues"]:
        plt.bar("Relative Eigenvalues", eigenvalue, label=f"Eigenvalue {i}", bottom=bottom)
        i += 1
        bottom += eigenvalue

    plt.axhline(y=0.95, linestyle=":", label="95% of Data")
    plt.ylabel("Percent Variance Explained")
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.legend(loc="upper right")
    plt.title("Eigenvalues: Percentage of Variance/Information\nfor Spotify Feature Data")
    plt.show()


def main():

    df = pd.read_csv("./unsynced-data/spotify.csv", index_col=0)
    print(np.max(df["acousticness"]))
    pca_data = perform_pca("./unsynced-data/spotify.csv",
                           ["spotify_id",
                            "lastfm_id",
                            "mode",
                            "manual_check",
                            "Unnamed: 0"])

    # create_spotify_eigenvalue_chart(pca_data)

    pca_out = pca_data["transformed_data"]
    # print(pca_data["relative_eigenvalues"])
    #
    #
    pca_data = perform_pca("./data/hot-100-current.csv",
                           ["chart_week", "title", "performer"])

    print(pca_data["relative_eigenvalues"])
    print(pca_data["important_features"])

    pca_out = pca_data["transformed_data"]

    kmean = KMeans(n_clusters=5)
    kmean.fit(pca_out[:, :2])

    sns.boxplot(x=pca_out[:, 0], y=pca_out[:, 1])
    plt.show()


if __name__ == "__main__":
    main()
