from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""
Set the following variables before running the script:
SPOTIFY_DATA: Path to the spotify data
BILLBOARD_DATA: Path to the billboard data
"""
SPOTIFY_DATA = "./../unsynced-data/spotify.csv"
BILLBOARD_DATA = "../unsynced-data/hot-100-current.csv"


def perform_pca(dataframe: pd.DataFrame, n_components=None):
    """
    Perform PCA on a dataframe. The dataframe must only contain quantitative features. No qualitative, no labels.
    :param dataframe: Data to do PCA on
    :param n_components: Number of components to use for pca. If None, extracts all possible
    :return: Dict {
        "transformed_data",
        "eigenvalues",
        "relative_eigenvalues",
        "important_features",
    }
    """

    # Drop any nans
    df = dataframe.dropna()

    # Perform scaling
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)

    # perform pca
    pca = PCA(n_components=n_components)
    pca_out = pca.fit_transform(scaled_df)

    if n_components == 3:
        print("Top three Eigenvalues:", pca.explained_variance_)

    # Find out most important features
    shape = pca.components_.shape[0]
    feature_names = list(df.columns)

    most_important = [np.abs(pca.components_[i]).argmax() for i in range(shape)]
    most_important_names = [feature_names[most_important[i]] for i in range(shape)]

    feat_dict = {f"PC{i}": most_important_names[i] for i in range(shape)}
    important_df = pd.DataFrame(feat_dict.items())

    return {
        "transformed_data": pca_out,
        "eigenvalues": pca.explained_variance_,
        "relative_eigenvalues": pca.explained_variance_ratio_,
        "important_features": important_df
    }


def create_eigenvalue_chart(pca_data, title):
    bottom = 0
    i = 1
    n_components = pca_data["relative_eigenvalues"].shape[0]
    for eigenvalue in pca_data["relative_eigenvalues"]:
        plt.bar("Relative Eigenvalues", eigenvalue, label=f"Eigenvalue {i}", bottom=bottom)
        i += 1
        bottom += eigenvalue

    plt.axhline(y=0.95, linestyle="-", color="blue", label="95% of Data")
    plt.axhline(y=bottom, linestyle="-", color="red", label=f"{int(100 * np.round(bottom, 2))}% of Data")
    plt.ylabel("Percent Variance Explained")
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.title(title)
    plt.legend(loc="upper right")
    plt.savefig(f"./../images/spotify-{n_components}-eigenvalues")
    plt.show()



def main():
    # Read in Spotify data
    orig_df = pd.read_csv(SPOTIFY_DATA, index_col=0)
    df = orig_df.copy()

    df = df.drop(["spotify_id", "lastfm_id", "mode", "manual_check"], axis=1)
    df.to_csv("./../unsynced-data/spotify-for-pca.csv")

    out = df.corr()
    sns.heatmap(out, annot=True)
    plt.title("Heatmap of Correlation Coefficients")
    plt.tight_layout()
    plt.savefig("../images/heatmap.png")
    plt.show()

    # Perform PCA
    spotify_pca = perform_pca(df, n_components=2)
    plt.scatter(spotify_pca["transformed_data"][:, 0], spotify_pca["transformed_data"][:, 1])
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("First Two Principal Components")
    plt.savefig("../images/two-pc.png")
    plt.show()
    create_eigenvalue_chart(spotify_pca, "Eigenvalues: Percentage of Variance/Information\nfor Spotify Feature Data")

    spotify_pca = perform_pca(df, n_components=3)
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(spotify_pca["transformed_data"][:, 0], spotify_pca["transformed_data"][:, 1],
               spotify_pca["transformed_data"][:, 2])
    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    ax.set_zlabel("Principal Component 3")
    ax.set_title("First Three Principal Components")
    plt.savefig("../images/three-pc.png")
    plt.show()

    scatter = plt.scatter(spotify_pca["transformed_data"][:, 0], spotify_pca["transformed_data"][:, 1],
                c=spotify_pca["transformed_data"][:, 2], alpha=0.5)
    plt.colorbar(scatter)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("First Three Principal Components (Third mapped to Color)")
    plt.savefig("../images/three-pc-color.png")
    plt.show()

    create_eigenvalue_chart(spotify_pca, "Eigenvalues: Percentage of Variance/Information\nfor Spotify Feature Data")

    spotify_pca = perform_pca(df)
    create_eigenvalue_chart(spotify_pca, "Eigenvalues: Percentage of Variance/Information\nfor Spotify Feature Data")


if __name__ == "__main__":
    main()