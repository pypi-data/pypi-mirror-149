import numpy as np
import queue

class DBSCAN:
    """
    DBSCAN instance, this instance does NOT have methods which return values or predict, 
    so it is important to access the computes values by using the attributes.

    Parameters:
        eps (float): The minimum radius of the distances for neighboring instances. Defaults to 2

        minpoints (int): The minimum number of points for an instance to become a core. Defaults to 5
    
    Attributes:
        labels (ndarray): The list of the sample indices.

        core_sample_indices (ndarray):The indices of the core samples

        noncore_sample_indices (list): The indices of the noncore samples (includes outliers)

        cl (int): The number of clusters.

    """
    def __init__(self, eps = 2, minpoints = 5):
        self.eps = eps
        self.minpoints = minpoints

    def _neigh_point(self,X , index, eps):
        """Checks for neighboring points"""
        points = []
        for i in range(len(X)):
            if (np.linalg.norm(X[i] - X[index]) <= eps):
                points.append(i)
        return points
    
    def fit(self, X):
        """
        Fits the instance

        Parameters:
            X (ndarray): ndarray of the X values
        
        Returns:
            self: The fitted instance
        """
        pointlabel  = [0] * len(X)
        pointcount = []
        corepoint=[]
        noncore=[]
        
        for i in range(len(X)):
            pointcount.append(self._neigh_point(X ,i ,self.eps))
        
        for i in range(len(pointcount)):
            if (len(pointcount[i])>=self.minpoints):
                pointlabel[i]=-1
                corepoint.append(i)
            else:
                noncore.append(i)

        for i in noncore:
            for j in pointcount[i]:
                if j in corepoint:
                    pointlabel[i]=-2

                    break

        self.cl = 0
        for i in range(len(pointlabel)):
            q = queue.Queue()
            if (pointlabel[i] == -1):
                pointlabel[i] = self.cl
                for x in pointcount[i]:
                    if(pointlabel[x]==-1):
                        q.put(x)
                        pointlabel[x]=self.cl
                    elif(pointlabel[x]==-1):
                        pointlabel[x]=self.cl
                while not q.empty():
                    neighbors = pointcount[q.get()]
                    for y in neighbors:
                        if (pointlabel[y]==-1):
                            pointlabel[y]=self.cl
                            q.put(y)
                        if (pointlabel[y]==-1):
                            pointlabel[y]=self.cl            
                self.cl=self.cl+1
        self.core_indices = np.array(corepoint)
        self.noncore_indices = np.array(noncore)
        self.labels = np.array(pointlabel)
        return self