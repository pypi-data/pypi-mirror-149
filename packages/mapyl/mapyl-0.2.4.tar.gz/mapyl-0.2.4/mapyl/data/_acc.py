import numpy as np

def accuracy(y, y_hat):
        """
        calculates the accuracy of the prediction

        Parameters:
                y (ndarray): ndarray of the correct values
                y_hat (ndarray): ndarray of the predicted values
        returns: float of the accuracy

        THIS IS DEPRECATED, USE utils.Accuracy
        """
        return np.sum(y==y_hat)/len(y)