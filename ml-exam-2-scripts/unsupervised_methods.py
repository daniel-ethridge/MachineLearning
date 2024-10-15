from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import scipy.cluster.hierarchy as sch
import pandas as pd
from collections import Counter


def run_pca(input_data: pd.DataFrame, n_components: int=None):
    """
    Run PCA
    :param input_data: Input dataframe
    :param n_components: number of components
    :return: pca object and result of pca.fit_transform()
    """
    # Drop any nans
    df = input_data.dropna()

    # Perform scaling
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)

    # perform pca
    pca = PCA(n_components=n_components)
    pca_out = pca.fit_transform(scaled_df)

    return pca, pca_out


def run_kmeans(input_data: pd.DataFrame, n_components: int=None, n_centroids: int=None):
    """

    :param input_data: Pandas dataframe of data
    :param n_components: number of components for pca
    :param n_centroids: number of centroids for kmeans
    :return: cluster labels
    """
    # Run pca on data
    _, pca_out = run_pca(input_data, n_components=n_components)

    # Cluster the data
    clusterer = KMeans(n_clusters=n_centroids)
    cluster_labels = clusterer.fit_predict(pca_out)

    return cluster_labels


def run_hierarchical_clustering(input_data: pd.DataFrame,
                                plot_image_save_file=None,
                                xlabel: str=None,
                                ylabel: str="None",
                                title: str=None,
                                n_components: int=None):
    """
    Run Hierarchical clustering
    :param title: Title of plot
    :param ylabel: y label of plot
    :param xlabel: x label of plot
    :param plot_image_save_file: Save location for plot.
    :param input_data: pandas dataframe
    :param n_components: num components for pca
    """
    if plot_image_save_file is None:
        raise ValueError("Need save location for plot")
    # Run pca on data
    _, pca_out = run_pca(input_data, n_components=n_components)

    # Run hierarchical clustering
    link = sch.linkage(pca_out, method="ward")
    dendrogram = sch.dendrogram(link)

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if title is not None:
        plt.title(title)

    plt.savefig(f"images/{plot_image_save_file}")
    plt.show()


def run_dbscan(
        input_data: pd.DataFrame,
        plot_image_save_file=None,
        xlabel: str=None,
        ylabel: str="None",
        title: str=None,
        n_components: int=None):
    """
    Run Hierarchical clustering
    :param title: Title of plot
    :param ylabel: y label of plot
    :param xlabel: x label of plot
    :param plot_image_save_file: Save location for plot.
    :param input_data: pandas dataframe
    :param n_components: num components for pca
    """
    if plot_image_save_file is None:
        raise ValueError("Need save location for plot")

    # run pca
    _, pca_out = run_pca(input_data, n_components=n_components)


    dbscan = DBSCAN(eps=0.3, min_samples=10)
    labels = dbscan.fit_predict(pca_out)
    print("Label counts:", dict(Counter(labels)))

    # Set cluster and outliers
    outliers_df = pca_out[labels == -1]
    clusters_df = pca_out[labels != -1]


    colors = labels
    colors_clusters = colors[colors != -1]
    color_outliers = "black"

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(clusters_df[:, 0], clusters_df[:, 1], clusters_df[:, 2], c=colors_clusters[:], edgecolors="black")
    ax.scatter(outliers_df[:, 0], outliers_df[:, 1], outliers_df[:, 2], c=color_outliers, edgecolors="black")
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
        
    fig.savefig(f"images/{plot_image_save_file}")
    plt.show()
