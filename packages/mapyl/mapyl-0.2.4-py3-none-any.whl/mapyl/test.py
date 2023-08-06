import numpy as np
from clustering import KMeans, DBSCAN
from classification.softmax_class import SoftMaxClasser
from sklearn import datasets


# from keras.datasets import mnist
# (train_X, train_y), (test_X, test_y) = mnist.load_data()
# Keep these commented when not used, they take too much time to load
train_x, train_y = datasets.make_blobs(centers = 2)

"""
This is a test file

Here all the tests are done for the library

it is a mess, but dont worry about it
"""
k = KMeans().fit(train_x)
print(k.predict(np.array([2, 6])))