import numpy as np
# this is painfully slow
class SoftMaxClasser:
    """
    SoftMax classifier instance

    Parameters:
        c (int): The number of classes. Defaults to 2

        lr (float): The learning rate. Defaults to 0.01
    """
    def __init__(self, c=2, lr=0.01):
        self.lr = lr
        self.c = c
    
    def _softmax(self, X):
        exp = np.exp(X - np.max(X))
        for i in range(len(X)):
            exp[i] /= np.sum(exp[i])
        return exp
    
    def _one_hot(self,y, c):
        y_hot = np.zeros((len(y), self.c))
        # numpy doesnt seem to like this but it works
        y_hot[np.arange(len(y)), y] = 1
        return y_hot

    
    def fit(self, X, y, iters):
        """
        Trains the SoftMaxClass instance

        Paramaters:
            X (ndarray): ndarray of the input of shape (num_samples, num_features)

            y (ndarray): ndarray of the output of shape (num_samples,)
            
            iters (int): The number of iterations

        Returns: none
        """
        m, n = X.shape
        self.w = np.random.random((n, self.c))
        self.b = np.random.random(self.c)

        losses = []

        for _ in range(iters):

            z = X@self.w + self.b
            y_hat = self._softmax(z)

            y_hot = self._one_hot(y, self.c)

            w_grad = (1/m)*np.dot(X.T, (y_hat - y_hot)) 
            b_grad = (1/m)*np.sum(y_hat - y_hot)

            self.w = self.w - self.lr*w_grad
            self.b = self.b - self.lr*b_grad

            loss = -np.mean(np.log(y_hat[np.arange(len(y)), y]))
            losses.append(loss)
        return self

    def predict(self, X):
        """
        Predicts the class of the X instance

        Parameter:
            X (ndarray): ndarray of shape (num_samples,num_features) to be predicted

        Returns: class of the supplied X
        """
        z = X@self.w + self.b
        y_hat = self._softmax(z)
        return np.argmax(y_hat, axis=1)
