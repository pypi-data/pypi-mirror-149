import numpy as np
import numpy.polynomial as pol
from typing import Callable, List, Union
Vector = List[float]
Function = Callable[[float], float]
Polynomial = pol.Polynomial


def lagrange2(X: Vector, Y: Vector) -> Function:
    """Returns the lagrange interpolation
    Args:
        X (Vector): X-data
        Y (Vector): Y-data
    Returns:
        Callable[[Vector], Vector]: returns the function that evaluates the lagrange interpolation
    """
    X = np.asarray(X)  

    def lagran(x):
        # Checks the input's type
        if type(x) is np.ndarray:
            x = x.reshape(-1, 1)
        
        if isinstance(x, list):
            x = np.array(x).reshape(-1, 1)
        
        else:
            x = np.array([x]).reshape(-1, 1)

        out = 0
        for i in range(len(X)):
            #pi_x = (x - np.array([(X[X != xi]).reshape(-1)] * len(x))) because X[X != xi] autoreshape (-1)
            pi_x = x - np.array([(X[X != X[i]])] * len(x))

            out += Y[i] * (pi_x / (X[i] - X[X != X[i]])).prod(axis = 1)

        return out
    
    return lagran
    
def lagrange(X: Vector, Y: Vector) -> Polynomial:
    p = 0
    for i in range(len(X)):
        qn = pol.Polynomial.fromroots(X[X != X[i]])
        p += Y[i] * qn / qn(X[i])
    return p
    