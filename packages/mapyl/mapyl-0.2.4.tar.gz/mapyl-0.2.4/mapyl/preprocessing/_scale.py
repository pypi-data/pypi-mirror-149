import numpy as np

class Normalizer:
    def normalize(X):
       '''normalizes a ndarray'''
       X = (X - np.amin(X))/(np.amax(X)-np.amin(X))
       return X

class MinMaxScaler:
    def scale(X, a=0, b=1):
       """
       Scales a ndarray in a set of values

       Parameters:
            X (ndarray): ndarray of the data to be scaled

            a (float): float of the minimum value
            
            b (float): float of the maximum value

       Returns: 
            ndarray of the scaled values
       """
       X = a + ((X - np.amin(X))*(b-a))/(np.amax(X)-np.amin(X))
       return X

class MeanNormalizer:
    def mean_normalize(X):
       '''mean normalizes a ndarray'''
       X = (X - np.average(X))/(np.amax(X)-np.amin(X))
       return X

class StandardScaler:
    def standard_scale(X):
        """Standard scales a ndarray"""
        sd = np.std(X)
        av = np.average(X)
        return (X - av)/sd