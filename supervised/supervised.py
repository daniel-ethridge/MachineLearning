import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pathlib

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

from imblearn.over_sampling import RandomOverSampler
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree

from sklearn.naive_bayes import GaussianNB as NB


def savefig(file_name, figure=None):
    home = pathlib.Path().home()
    savedir = "Documents/daniel-ethridge.github.io/src/assets/ml-assets/ml-supervised/"
    if not figure:
        plt.savefig(os.path.join(home, savedir, file_name + ".png"))
    else:
        figure.savefig(os.path.join(home, savedir, file_name + ".png"))


# Read in the data
df = pd.read_csv("../unsynced-data/lastfm-spotify-merged.csv")
df = df.drop(["Unnamed: 0", "hot_100", "lastfm_id", "artist", "title", "lfm_similars", "lfm_tags", "spotify_id",
              "manual_check", "mode"], axis=1)

# Spotify says an instrumental value of greater than 0.5 is not instrumental, while below that threshold is. Create the
# label
df["instrumental"] = df["instrumentalness"].apply(lambda x: 0 if x <= 0.5 else 1)
df_inst = df.copy()
print(df.head())
df_inst = df_inst.drop(["instrumentalness"], axis=1)

# Take label off of dataset and create plot showing imbalance
df_labels = df_inst["instrumental"]
df_data = df_inst.drop("instrumental", axis=1)
# sns.countplot(x=df_labels)
# plt.title("Counts for each label")
# savefig("instrumental_counts")

# fix imbalance
# Use RandomOverSampler (from imblearn) to balance the data
samp = RandomOverSampler()
samp_data, samp_labels = samp.fit_resample(df_data, df_labels)
# sns.countplot(x=samp_labels)
# plt.title("Counts for label after oversampling")
# savefig("instrumental_counts_sampled")

# fit logistic regression
x_train, x_test, y_train, y_test = train_test_split(samp_data, samp_labels)
# log_reg = LogisticRegression(max_iter = 1000)
# log_reg.fit(x_train, y_train)
#
# y_pred = log_reg.predict(x_test)
# conf_matrix = confusion_matrix(y_test, y_pred)
# disp = ConfusionMatrixDisplay(conf_matrix).plot()
# savefig("log_reg_conf_matrix", disp.figure_)
#
# prec = precision_score(y_test, y_pred)
# recall = recall_score(y_test, y_pred)
# f1 = f1_score(y_test, y_pred)
# accur = accuracy_score(y_test, y_pred)
# results_df = pd.DataFrame(columns=["Precision", "Recall", "F1", "Accuracy", "model"])
# results_df.loc[0] = [prec, recall, f1, accur, "Logistic Regression"]
#
# # Naive bayes
# nb = NB()
# nb.fit(x_train, y_train)
# y_pred = nb.predict(x_test)
# conf_matrix = confusion_matrix(y_test, y_pred)
# disp = ConfusionMatrixDisplay(conf_matrix).plot()
# savefig("nb_conf_matrix", disp.figure_)
#
# prec = precision_score(y_test, y_pred)
# recall = recall_score(y_test, y_pred)
# f1 = f1_score(y_test, y_pred)
# accur = accuracy_score(y_test, y_pred)
# results_df.loc[1] = [prec, recall, f1, accur, "Naive Bayes"]
#
tree = DecisionTreeClassifier(max_depth = 3, criterion="entropy", splitter="random")
tree.fit(x_train, y_train)
y_pred = tree.predict(x_test)
# conf_matrix = confusion_matrix(y_test, y_pred)
# disp = ConfusionMatrixDisplay(conf_matrix).plot()
# plt.show()
plot_tree(tree, proportion=True, max_depth=3, fontsize=6)
plt.show()

#savefig("tree_conf_matrix", disp.figure_)

prec = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
accur = accuracy_score(y_test, y_pred)
# results_df.loc[2] = [prec, recall, f1, accur, "Decision Tree"]
#
# depth = 25
# depths = np.arange(1, depth + 1)
# plt.show()
#
# d_tree_df = pd.DataFrame(columns = ["train_accuracy", "test_accuracy", "Depth"])
#
# for d in depths:
#     print(d)
#     tree = DecisionTreeClassifier(max_depth=d)
#     tree.fit(x_train, y_train)
#     y_pred_train = tree.predict(x_train)
#     y_pred_test = tree.predict(x_test)
#     f1_train = accuracy_score(y_train, y_pred_train)
#     f1_test = accuracy_score(y_test, y_pred_test)
#     d_tree_df.loc[d-1] = [f1_train, f1_test, d]
#
# plt.scatter(d_tree_df["Depth"], d_tree_df["train_accuracy"], label="Training Data")
# plt.scatter(d_tree_df["Depth"], d_tree_df["test_accuracy"], label="Testing Data")
# plt.ylabel("Accuracy")
# plt.xlabel("Max Depth Parameter of Decision Tree")
# plt.title("Training and Testing Accuracy as a function of Max Depth")
# plt.legend()
# plt.tight_layout()
# savefig("tree-tuning")
