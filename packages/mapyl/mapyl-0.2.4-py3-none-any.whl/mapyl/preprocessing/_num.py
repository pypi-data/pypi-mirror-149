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