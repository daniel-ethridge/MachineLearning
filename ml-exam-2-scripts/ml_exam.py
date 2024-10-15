import numpy as np
from sklearn.decomposition import PCA

from unsupervised_methods import *
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    df_orig = pd.read_csv('data_folder/StudentSummerProgramDataQuiz2.csv')
    df = df_orig.drop(["PersonNum", "Gender", "State", "WorkExp", "Decision"], axis=1)
    # df.to_csv("data_folder/summer_clean.csv")

    # pca, pca_out = run_pca(df, n_components=2)

    df = df.dropna()

    # Perform scaling
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)

    pca = PCA(n_components=2)
    pca_out = pca.fit_transform(scaled_df)
    # Cluster the data
    clusterer = KMeans(n_clusters=3)
    cluster_labels = clusterer.fit_predict(pca_out)
    print("Cluster centers\n", clusterer.cluster_centers_)

    plt.scatter(pca_out[:, 0], pca_out[:, 1], c=cluster_labels)
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.title("KMeans on PCA data from\nSummer Program Data")
    plt.show()

    # print("PCA reduced data\n", pca_out)
    # print("Ordered Eigenvalues", pca.explained_variance_)
    # print("Percentage Eigenvalues", pca.explained_variance_ratio_)

   # eigenvectors = pca.components_

   # print("Eigenvectors:\n", pca.components_)
