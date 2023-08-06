import numpy as np

class KMeans:
    """
    KMeans instance

    Parameters:
        k (int): The number of clusters. Defaults to 2

        tol (float): The tolerance for the cost. Defaults to 0.001
    """
    def __init__(self, k=2, tol=0.001):
        self.k = k
        self.tol = tol

    def fit(self,X, iters=300):
        """
        Fits the instance

        Parameters:
            X (ndarray): The X values to be fitted

            iters (int): The number of iterations. Defaults to 300

        Returns none
        """

        self.cent = {}

        for i in range(self.k):
            self.cent[i] = X[i]

        for i in range(iters):
            self.classifications = {}

            for i in range(self.k):
                self.classifications[i] = []

            for feature in X:
                dist = [np.linalg.norm(feature-self.cent[centroid]) for centroid in self.cent]
                classification = dist.index(min(dist))
                self.classifications[classification].append(feature)

            prev_cent = dict(self.cent)

            for classification in self.classifications:
                self.cent[classification] = np.average(self.classifications[classification],axis=0)

            optimized = True

            for c in self.cent:
                original_centroid = prev_cent[c]
                current_centroid = self.cent[c]
                if np.sum((current_centroid-original_centroid)/original_centroid*100.0) > self.tol:
                    optimized = False

            if optimized:
                break
        return self

    def predict(self,X):
        """
        Predicts the class of an X value

        Patameter:
            X (ndarray): The X values to be predicted

        Returns: The index of the class of the supplied X
        """
        dist = [np.linalg.norm(X-self.cent[centroid]) for centroid in self.cent]
        classification = dist.index(min(dist))
        return classification