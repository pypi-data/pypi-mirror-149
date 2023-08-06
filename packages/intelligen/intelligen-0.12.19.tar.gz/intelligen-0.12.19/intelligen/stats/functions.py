import numpy as np
from intelligen.fortran.functions import erf as erf_fortran

from typing import List, Union
Vector = List[float]

__all__ = ['mean_squared_error', 'mean_absolute_error',
           'erf', 'erfc']

def mean_squared_error(y_real: Vector, y_pred: Vector) -> float:
    """Returns the mean squared error
    Args:
        y_real (Vector): Real data
        y_pred (Vector): Predicted data
    Returns:
        float: mean squared error
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    
    return np.mean((y_real - y_pred)**2)
def mean_absolute_error(y_real: Vector, y_pred: Vector) -> float:
    """Returns the mean absolute error
    Args:
        y_real (Vector): Real data
        y_pred (Vector): Predicted data
    Returns:
        float: mean absolute error
    """
    y_real = np.array(y_real)
    y_pred = np.array(y_pred)
    
    return np.mean(np.abs(y_real - y_pred))


def erf(x: Union[float, Vector]) -> Union[float, Vector]:
    """
    Error Function
    ==============

    Parameters
    ----------
    x : float, Vector
        Value

    Returns
    -------
    float, Vector
        Error function at x
    """
    
    try:
        return erf_fortran(x).item()
    except:
        return erf_fortran(x)

def erfc(x: Union[float, Vector]) -> Union[float, Vector]:
    """
    Complementary Error Function
    ==============

    Parameters
    ----------
    x : float, Vector
        Value

    Returns
    -------
    float, Vector
        Complementary error function at x
    """
    return 1 - erf(x)