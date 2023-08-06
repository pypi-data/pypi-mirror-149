import numpy as np

class GradientDescent:
    """
    Linear Gradient Descent regressor

    Parameter:
        lr(float): The learning rate
    """
    def __init__(self, lr):
        self.lr = lr
        pass

    def _compute(self, X):
        self.theta = np.random.randn(2, self.n)

    def fit(self, X, y, iters):
        """
        Trains the Gradient Descent instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input

            y (ndarray): ndarray of shape (num_samples,) of the output

            iters (int): the number of iteration
        
        Returns:
            self: the fitted instance
        """
        self.m, self.n = X.shape

        X_b = np.c_[np.ones((self.m, 1)), X]
        self._compute(X)
        for i in range(iters):
            grads = 2/(self.m) * X_b.T.dot(X_b.dot(self.theta) - y)
            self.theta = self.theta - self.lr * grads

        return self
    
    def predict(self, X):
        """
        Predicts y value for the supplied X

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input

        Returns:
            ndarray: The output of the supplied X
        """
        x = X
        ones_ = np.ones(x.shape[0])
        x = np.c_[ones_,x]
        result = np.dot(x,self.theta)
        return result 


class SGD:
    """
    Stochastic Gradient descent instance
    """
    def __init__(self):
        pass
    t0 = 5
    t1 = 50

    def _learn_sched(self, t):
        return self.t0/(t+self.t1)
    
    theta = np.random.randn(2, 1)

    def fit(self, X, y, epochs=50):
        """
        Fits the instance

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input values
            y (ndarray): ndarray of shape (num_samples,) of the output values
            epochs (int): The number of epochs. Defaults to 50.

        Returns:
            self: The fitted instance
        """
        m, n = X.shape
        X_b = np.c_[np.ones((m, 1)), X]
        for epoch in range(epochs):
            for i in range(m):
                random_index = np.random.randint(m)
                xi = X_b[random_index:random_index+1]
                yi = y[random_index:random_index+1]
                gradients = 2 * xi.T.dot(xi.dot(self.theta) - yi)
                eta = self._learn_sched(epoch * m + i)
                self.theta = self.theta - eta * gradients
        return self

    def predict(self, X):
        """
        Predicts y value for the supplied X

        Parameters:
            X (ndarray): ndarray of shape (num_samples, num_features) of the input

        Returns:
            ndarray: The output of the supplied X
        """
        x = X
        ones_ = np.ones(x.shape[0])
        x = np.c_[ones_,x]
        result = np.dot(x,self.theta)
        return result 
