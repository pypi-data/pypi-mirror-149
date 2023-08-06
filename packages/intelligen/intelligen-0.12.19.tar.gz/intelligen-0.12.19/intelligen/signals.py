import numpy as np
import matplotlib.pyplot as plt
from typing import List
Vector = List[float]

def heaviside(t: Vector) -> Vector:
    return (np.array(t) >= 0).astype(int)

def rect(t: Vector) -> Vector:
    t = np.array(t)
    return heaviside(t + 1/2) - heaviside(t - 1/2)

def delta(n: Vector) -> Vector:
    return (np.array(n) == 0).astype(int)

def time_delay(x: Vector, y: Vector, t: float) -> Vector:
    x, y = np.array(x), np.array(y)
    x = x + t
    return x, y

