from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import scipy.cluster.hierarchy as sch
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from collections import Counter


def main():
    # Get billboard data
    df = pd.read_csv("../unsynced-data/spotify.csv", index_col=0)
    df["instrumental_music"] = True


    df.loc[df["instrumentalness"] > 0.5, "instrumental_music"] = False
    df_label = df["instrumental_music"]
    df = df.drop(["spotify_id", "lastfm_id", "mode", "manual_check", "instrumental_music"], axis=1)
    df = df.dropna()
    # df = df[:20000]

    # Standardize and run PCA
    scaler = StandardScaler()
    pca = PCA(n_components=3)
    scaled_data = scaler.fit_transform(df)
    pca_out_orig = pca.fit_transform(scaled_data)
    pca_out = pca_out_orig[:20000, :]

    # link = sch.linkage(pca_out, method="ward")
    # dendrogram = sch.dendrogram(link)
    # plt.show()

    # this code block taken from https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis
    # .html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py
    # range_n_clusters = [2, 3, 4]
    # for n_clusters in range_n_clusters:
    #     # Create a subplot with 1 row and 2 columns
    #     # fig, (ax1, ax2) = plt.subplots(1, 2)
    #     fig = plt.figure()
    #     ax1 = fig.add_subplot(1, 2, 1)
    #     ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    #     fig.set_size_inches(18, 7)
    #
    #     # The 1st subplot is the silhouette plot
    #     # The silhouette coefficient can range from -1, 1 but in this example all
    #     # lie within [-0.1, 1]
    #     ax1.set_xlim([-0.1, 1])
    #     # The (n_clusters+1)*10 is for inserting blank space between silhouette
    #     # plots of individual clusters, to demarcate them clearly.
    #     ax1.set_ylim([0, len(pca_out) + (n_clusters + 1) * 10])
    #
    #     # Initialize the clusterer with n_clusters value and a random generator
    #     # seed of 10 for reproducibility.
    #     clusterer = KMeans(n_clusters=n_clusters)
    #     cluster_labels = clusterer.fit_predict(pca_out)
    #
    #     # The silhouette_score gives the average value for all the samples.
    #     # This gives a perspective into the density and separation of the formed
    #     # clusters
    #     silhouette_avg = silhouette_score(pca_out, cluster_labels)
    #     print(
    #         "For n_clusters =",
    #         n_clusters,
    #         "The average silhouette_score is :",
    #         silhouette_avg,
    #     )
    #
    #     # Compute the silhouette scores for each sample
    #     sample_silhouette_values = silhouette_samples(pca_out, cluster_labels)
    #
    #     y_lower = 10
    #     for i in range(n_clusters):
    #         # Aggregate the silhouette scores for samples belonging to
    #         # cluster i, and sort them
    #         ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
    #
    #         ith_cluster_silhouette_values.sort()
    #
    #         size_cluster_i = ith_cluster_silhouette_values.shape[0]
    #         y_upper = y_lower + size_cluster_i
    #
    #         color = cm.nipy_spectral(float(i) / n_clusters)
    #         ax1.fill_betweenx(
    #             np.arange(y_lower, y_upper),
    #             0,
    #             ith_cluster_silhouette_values,
    #             facecolor=color,
    #             edgecolor=color,
    #             alpha=0.7,
    #         )
    #
    #         # Label the silhouette plots with their cluster numbers at the middle
    #         # ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    #
    #         # Compute the new y_lower for next plot
    #         y_lower = y_upper + 10  # 10 for the 0 samples
    #
    #     ax1.set_title("The silhouette plot for the various clusters.")
    #     ax1.set_xlabel("The silhouette coefficient values")
    #     ax1.set_ylabel("Cluster label")
    #
    #     # The vertical line for average silhouette score of all the values
    #     ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    #
    #     ax1.set_yticks([])  # Clear the yaxis labels / ticks
    #     ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
    #
    #     # 2nd Plot showing the actual clusters formed
    #     colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
    #     ax2.scatter(
    #         pca_out[:, 0], pca_out[:, 1], pca_out[:, 2], marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
    #     )
    #
    #     # Labeling the clusters
    #     centers = clusterer.cluster_centers_
    #     # Draw white circles at cluster centers
    #     ax2.scatter(
    #         centers[:, 0],
    #         centers[:, 1],
    #         centers[:, 2],
    #         marker="o",
    #         c="white",
    #         alpha=1,
    #         s=200,
    #         edgecolor="k",
    #     )
    #
    #     for i, c in enumerate(centers):
    #         ax2.scatter(c[0], c[1], c[2], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")
    #
    #     # ax2.set_title("The visualization of the clustered data.")
    #     ax2.set_xlabel("Feature space for the 1st feature")
    #     ax2.set_ylabel("Feature space for the 2nd feature")
    #
    #     plt.suptitle(
    #         "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
    #         % n_clusters,
    #         fontsize=14,
    #         fontweight="bold",
    #     )
    #
    #     fig.savefig(f"../images/k-testing-{n_clusters}-clusters.png")
    #
    # plt.show()

    # plt.scatter(pca_out[:, 0], pca_out[:, 1],
    #             marker=".", s=30, lw=0, alpha=0.7, edgecolor="k")
    # plt.show()

    dbscan = DBSCAN(eps=0.3, min_samples=10)
    labels = dbscan.fit_predict(pca_out)
    print(dict(Counter(labels)))

    outliers_df = pca_out[labels == -1]
    clusters_df = pca_out[labels != -1]

    colors = labels
    colors_clusters = colors[colors != -1]
    color_outliers = "black"

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(clusters_df[:, 0], clusters_df[:, 1], clusters_df[:, 2], c=colors_clusters[:], edgecolors="black")
    ax.scatter(outliers_df[:, 0], outliers_df[:, 1], outliers_df[:, 2], c="black", edgecolors="black")
    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    ax.set_zlabel("PC 3")
    ax.set_title("DBSCAN of First Three Principal Components")
    plt.show()

    # plt.scatter(df[labels == -1, 0], df[labels == -1, 1], s = 10, c="black")
    # plt.show()


if __name__ == "__main__":
    main()
