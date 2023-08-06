import numpy as np
from itertools import combinations_with_replacement

class PolyExp:
    def __init__(self, degree) -> None:
        self.degree = degree
    def evalnum(self, X):
            """Converts ndarray to poly features"""
            ret = []
            for j in range(len(X)):
                l = np.ndarray.tolist(X[j])
                l.append("c")
                t = []
                for i in combinations_with_replacement(l, self.degree):
                    t.append(i)
                t = [list(_) for _ in t]
                for i in range(len(t)):
                    while "c" in t[i]:
                        t[i].remove("c")
                    t[i] = np.prod(t[i])
                t = np.array(t)
                t = np.sort(t)
                ret.append(t)
            ret = np.array(ret)
            ret = np.sort(ret, 1)
            return ret


class Mode:
    def mode(a, axis=0):
        """
        A copy of scipy's mode function

        returns most common values in ndarray along with the amount of values in the indices
        """
        scores = np.unique(np.ravel(a))
        testshape = list(a.shape)
        testshape[axis] = 1
        oldmostfreq = np.zeros(testshape)
        oldcounts = np.zeros(testshape)

        for score in scores:
            template = (a == score)
            counts = np.expand_dims(np.sum(template, axis),axis)
            mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
            oldcounts = np.maximum(counts, oldcounts)
            oldmostfreq = mostfrequent

        return mostfrequent, oldcounts

class Accuracy:
    def accuracy(y, y_hat):
        """
        calculates the accuracy of the prediction (for classification tasks ONLY)

        Parameters:
                y (ndarray): ndarray of the correct values

                y_hat (ndarray): ndarray of the predicted values
                
        returns: float of the accuracy
        """
        return np.sum(y==y_hat)/len(y)