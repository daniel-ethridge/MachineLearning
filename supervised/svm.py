import sklearn.svm
import pathlib
import os
import matplotlib.pyplot as plt


def savefig(file_name, figure=None):
    home = pathlib.Path().home()
    savedir = "Documents/daniel-ethridge.github.io/src/assets/ml-assets/ml-supervised/"
    if not figure:
        plt.savefig(os.path.join(home, savedir, file_name + ".png"))
    else:
        figure.savefig(os.path.join(home, savedir, file_name + ".png"))


df