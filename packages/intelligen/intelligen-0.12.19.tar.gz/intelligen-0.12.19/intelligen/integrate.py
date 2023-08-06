import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Callable, Union

Vector = List[float]
Function = Callable[[float], float]
Function2d = Callable[[float, float], float]

def newton_cotes(y: Vector=None, x: Vector=None, formula: str='trapz', h: float=1,
                 f: Function=None, a: float=None, b: float=None, N: int=100) -> float:
    """
    Newton-Cotes rules
    ==================
    In numerical analysis, the Newton-Cotes formulas, also called the Newton-Cotes quadrature
    rules or simply Newton-Cotes rules, are a group of formulas for numerical integration
    (also called quadrature) based on evaluating the integrand at equally spaced points.
    They are named after Isaac Newton and Roger Cotes.

    Newton-Cotes formulas can be useful if the value of the integrand at equally spaced points is given.
    If it is possible to change the points at which the integrand is evaluated,
    then other methods such as Gaussian quadrature and Clenshaw-Curtis quadrature are probably more suitable.
    `n` is the grade of the polynomial interpolation, also nodes - 1 

    Parameters
    ----------
    y : Vector
        Input array to integrate
    x : Vector, optional
        The sample points corresponding to the y values. If x is None,
        the sample points are assumed to be evenly spaced h apart, by default None
    formula : str, optional
        This defines which Newton-Cotes rule apply
            trapz: trapezoidal rule, `n=1`
            simpson: Simpson's rule, `n=2`
            simpson3_8: Simpson's rule 3/8, `n=3`
            boole : Boole's rule, `n=4`
            weddle: Weddle's rule, `n=6`

            -> For simplicity is recommended to use the functions `trapz`, `simpson` etc.
            
    h : float, optional
        The spacing between sample points when x is None, by default 1
    f : function, optional
        funcion to integrate, if you don't define y/x
    a : float, optional
        Lower limit of the integral
    b : float, optional
        Upper limit of the integral
    N : int, optional
        Number of intervals, must be divisible by n, by default 100

    Returns
    -------
    float
        Definite integral
    
    Examples
    --------
    >>> N, a, b = 12, 1, 4
    >>> x = np.linspace(a, b, N+1)
    >>> y = np.sin(x)
    >>> print(newton_cotes(y,x,'simpson'))
    1.193972031074762
    >>> def fun(x): return np.sin(x)
    >>> print(newton_cotes(f=fun, a=a, b=b, N=N, formula='simpson3_8'))
    1.1940051049177476

    """
    if   formula == 'trapz': 
        n, fs = 1, '(y[i] + y[i+1]) * d[i]/2'
    elif formula == 'simpson':
        n, fs = 2, '(y[n*i] + 4*y[n*i + 1] + y[n*i + 2]) * d[i]/3'
    elif formula == 'simpson3_8': 
        n, fs = 3, '(y[n*i] + 3*y[n*i + 1] + 3*y[n*i + 2] + y[n*i + 3]) * 3*d[i]/8'
    elif formula == 'boole': 
        n, fs = 4, '(7*y[n*i] + 32*y[n*i + 1] + 12*y[n*i + 2] + 32*y[n*i + 3] + 7*y[n*i + 4]) * 2*d[i]/45'
    elif formula == 'weddle': 
        n, fs = 6, '(y[n*i] + 5*y[n*i + 1] + y[n*i + 2] + 6*y[n*i + 3] + y[n*i + 4] + 5*y[n*i + 5] + y[n*i + 6]) * 3*d[i]/10'
    else: raise ValueError('Wrong formula')

    if y is None and x is None:
        if not all(p is not None for p in [f,a,b]): raise ValueError(f"If you don't define y/x you must define f,a and b")
        if N%n != 0: raise ValueError(f'{N=} must be divisible by {n=}')
        x = np.linspace(a,b,N+1)
        y = f(x)   
    
    if (len(y)-1)%n != 0: raise ValueError(f'The length of the array y={len(y)} - 1 must be multiple of {n=} in order to divide the interval')
    nh = int((len(y)-1)/n)

    if x is None: 
        d = np.array([h]*nh)
        # x is only for checking
        x = np.empty(len(y))
    else: d = np.diff(x)[::n]

    if len(y) != len(x): raise ValueError(f'The length of x={len(x)} and y={len(y)} must be the same')

    s = 0
    for i in range(nh):
        s += eval(fs)
    return s

def trapz(y: Vector=None, x: Vector=None, h: float=1,
          f: Function=None, a: float=None, b: float=None, N: int=100) -> float:
    """
    Trapezoidal Rule
    ================
    The trapezoidal rule (also known as the trapezoid rule or trapezium rule)
    is a technique for approximating the definite integral.
    The trapezoidal rule works by approximating the region under the graph of the function 
    `f(x)` as a trapezoid and calculating its area.
    `n=1`, where n is the grade of the polynomial interpolation, also nodes - 1.
    This is a special case of Newton-Cotes formulas  

    Parameters
    ----------
    y : Vector
        Input array to integrate
    x : Vector, optional
        The sample points corresponding to the y values. If x is None,
        the sample points are assumed to be evenly spaced h apart, by default None
    h : float, optional
        The spacing between sample points when x is None, by default 1
    f : function, optional
        funcion to integrate, if you don't define y/x
    a : float, optional
        Lower limit of the integral
    b : float, optional
        Upper limit of the integral
    N : int, optional
        Number of intervals, must be divisible by n, by default 100

    Returns
    -------
    float
        Definite integral
    
    Examples
    --------
    >>> N, a, b = 12, 1, 4
    >>> x = np.linspace(a, b, N+1)
    >>> y = np.sin(x)
    >>> print(trapz(y,x))
    1.187720971137812
    >>> def fun(x): return np.sin(x)
    >>> print(trapz(f=fun, a=a, b=b, N=N))
    1.187720971137812

    """
    return newton_cotes(y, x, 'trapz', h, f, a, b, N)

def simpson(y: Vector=None, x: Vector=None, h: float=1,
            f: Function=None, a: float=None, b: float=None, N: int=100) -> float:
    """
    Simpson's Rule
    ============
    In numerical integration, Simpson's rules are several approximations for definite integrals,
    named after Thomas Simpson (1710-1761).
    This is the  most basic of these rules, called Simpson's 1/3 rule, or just Simpson's rule.
    `n=2`, where n is the grade of the polynomial interpolation, also nodes - 1.
    This is a special case of Newton-Cotes formulas 

    Parameters
    ----------
    y : Vector
        Input array to integrate
    x : Vector, optional
        The sample points corresponding to the y values. If x is None,
        the sample points are assumed to be evenly spaced h apart, by default None
    h : float, optional
        The spacing between sample points when x is None, by default 1
    f : function, optional
        funcion to integrate, if you don't define y/x
    a : float, optional
        Lower limit of the integral
    b : float, optional
        Upper limit of the integral
    N : int, optional
        Number of intervals, must be divisible by n, by default 100

    Returns
    -------
    float
        Definite integral
    
    Examples
    --------
    >>> N, a, b = 12, 1, 4
    >>> x = np.linspace(a, b, N+1)
    >>> y = np.sin(x)
    >>> print(simpson(y,x))
    1.193972031074762
    >>> def fun(x): return np.sin(x)
    >>> print(simpson(f=fun, a=a, b=b, N=N))
    1.193972031074762

    """
    return newton_cotes(y, x, 'simpson', h, f, a, b, N)

def simpson3_8(y: Vector=None, x: Vector=None, h: float=1,
               f: Function=None, a: float=None, b: float=None, N: int=99) -> float:
    """
    Simpson's Rule 3/8
    ================
    In numerical integration, Simpson's rules are several approximations for definite integrals,
    named after Thomas Simpson (1710-1761).
    This is the second of these rules, called Simpson's 3/8 rule or Simpson's second rule.
    `n=3`, where n is the grade of the polynomial interpolation, also nodes - 1.
    This is a special case of Newton-Cotes formulas 

    Parameters
    ----------
    y : Vector
        Input array to integrate
    x : Vector, optional
        The sample points corresponding to the y values. If x is None,
        the sample points are assumed to be evenly spaced h apart, by default None
    h : float, optional
        The spacing between sample points when x is None, by default 1
    f : function, optional
        funcion to integrate, if you don't define y/x
    a : float, optional
        Lower limit of the integral
    b : float, optional
        Upper limit of the integral
    N : int, optional
        Number of intervals, must be divisible by n, by default 99

    Returns
    -------
    float
        Definite integral
    
    Examples
    --------
    >>> N, a, b = 12, 1, 4
    >>> x = np.linspace(a, b, N+1)
    >>> y = np.sin(x)
    >>> print(simpson3_8(y,x))
    1.1940051049177476
    >>> def fun(x): return np.sin(x)
    >>> print(simpson3_8(f=fun, a=a, b=b, N=N))
    1.1940051049177476

    """
    return newton_cotes(y, x, 'simpson3_8', h, f, a, b, N)

def boole(y: Vector=None, x: Vector=None, h: float=1,
          f: Function=None, a: float=None, b: float=None, N: int=100) -> float:
    """
    Boole's Rule 
    ============
    In mathematics, Boole's rule, named after George Boole, is a method of numerical integration.

    `n=4`, where n is the grade of the polynomial interpolation, also nodes - 1
    This is a special case of Newton-Cotes formulas 

    Parameters
    ----------
    y : Vector
        Input array to integrate
    x : Vector, optional
        The sample points corresponding to the y values. If x is None,
        the sample points are assumed to be evenly spaced h apart, by default None
    h : float, optional
        The spacing between sample points when x is None, by default 1
    f : function, optional
        funcion to integrate, if you don't define y/x
    a : float, optional
        Lower limit of the integral
    b : float, optional
        Upper limit of the integral
    N : int, optional
        Number of intervals, must be divisible by n, by default 100

    Returns
    -------
    float
        Definite integral

    """
    return newton_cotes(y, x, 'boole', h, f, a, b, N)

def weddle(y: Vector=None, x: Vector=None, h: float=1,
           f: Function=None, a: float=None, b: float=None, N: int=96) -> float:
    """
    Weddle's Rule 
    ==========

    n=6, where n is the grade of the polynomial interpolation, also nodes - 1 

    Parameters
    ----------
    y : Vector
        Input array to integrate
    x : Vector, optional
        The sample points corresponding to the y values. If x is None,
        the sample points are assumed to be evenly spaced h apart, by default None
    h : float, optional
        The spacing between sample points when x is None, by default 1
    f : function, optional
        funcion to integrate, if you don't define y/x
    a : float, optional
        Lower limit of the integral
    b : float, optional
        Upper limit of the integral
    N : int, optional
        Number of intervals, must be divisible by n, by default 96

    Returns
    -------
    float
        Definite integral

    """
    return newton_cotes(y, x, 'weddle', h, f, a, b, N)

def newton_cotes2(y: Vector=None, x: Vector=None, h: float=1,
                 f: Function=None, a: float=None, b: float=None, n: int=100) -> float:
    n = len(y)-1
    if   n == 1: return trapz(y,x,h)
    elif n == 2: return simpson(y,x,h)
    elif n == 3: return simpson3_8(y,x,h)
    elif n == 4: return boole(y,x,h)
    elif n == 6: return weddle(y,x,h)


def odeEuler(f: Function2d, t0: float, tfin: float, N: int, y0: Union[float, Vector]) -> Tuple[Vector, Vector]:
    """
    Euler Method
    ============

    Parameters
    ----------
    f : Function2d
        Right-hand side of the differential equation `y' = f(t,y), y(t0) = y0`
    t0 : float
        Initial time 
    tfin : float
        Final time
    N : int
        Number of partitions
    y0 : float
        Initial value

    Returns
    -------
    Tuple[Vector, Vector]
        The time and value vectors of the solution
    
    Examples
    --------
    >>> def q(t): return 1/2 + 1/2 * np.cos(t**2)
    >>> def f(t, y): return q(t) - y
    >>> T, U = odeEuler(f, 0, 6, 1000, 0)
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(T,U)
    >>> plt.show()
    plot figure
    >>> T, U = odeEuler(f, 0, 6, 1000, [0,1])
    >>> for i in range(len(T)):
            plt.plot(T[i], U[i])
    >>> plt.show()
    plot figure

    """
    if isinstance(y0, list) or type(y0) == np.ndarray:
        leny0 = len(y0)
        
        T = np.tile(np.linspace(t0, tfin, N+1), (leny0,1))
        h = (tfin - t0) / N

        U = np.empty([leny0, N+1])
        U[:,0] = y0
        for i in range(1, N+1):
            U[:,i] = U[:,i-1] + h*f(T[:,i-1], U[:,i-1])

    else:
        T = np.linspace(t0, tfin, N+1)
        h = (tfin - t0) / N
        U = np.empty(N+1)
        U[0] = y0
        for i in range(1, N+1):
            U[i] = U[i-1] + h*f(T[i-1], U[i-1])

    return T, U

def slope_field(f: Function2d, range: list = None,
                xlim: list = None, ylim: list = None,
                normalize: bool = True, plot_type: str = 'quiver',
                density: int = 20, color: bool = True,
                show: bool = True, cmap: str = 'viridis'):
    """
    Slope Field
    ===========
    Graphical representation of the solutions
    to a first-order differential equation `y' = f(t,y)`

    Parameters
    ----------
    f : Function2d
        Function with 2 parameters `y' = f(t,y)`

    range : list, optional
        Sets both limits x/y of the plot, by default [-5, 5]

    xlim : list, optional
        Sets the x limits of the plot, if `range` is defined, xlim is already set, by default [-5, 5]

    ylim : list, optional
        Sets the y limits of the plot, if `range` is defined, ylim is already set, by default [-5, 5]

    normalize : bool, optional
        Normalize the slope field, by default True

    plot_type : str, optional
        Defines the plot type
            quiver: -> plt.quiver()
            streamplot: -> plt.streamplot()
        by default 'quiver'

    density : int, optional
        Density of arrows, by default 20

    color : bool, optional
        Color of the arrows, by default True
        
    show : bool, optional
        Shows the plot, by default True

    cmap : str, optional
        https://matplotlib.org/stable/tutorials/colors/colormaps.html

    Examples
    --------
    >>> def fun(x,y): return x + np.sin(y)
    >>> slope_field(fun, range=[-2,2], plot_type='streamplot', cmap='plasma')
    plot figure
    >>> slope_field(fun, xlim=[-3,2], ylim=[-1,1], color=False, normalize=False, density=30, show=False)
    >>> T, U = odeEuler(fun, -3, 2, 1000, 0.1)
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(T,U)
    >>> plt.show()
    plot figure

    """
    
    if range is None and xlim is None and ylim is None:
        range = [-5,5]
        x1, x2 = range
        y1, y2 = range
    
    elif xlim is None and ylim is None:
        x1, x2 = range
        y1, y2 = range
    
    elif range is None:
        x1, x2 = xlim
        y1, y2 = ylim
    
    else:
        raise ValueError('Must speciefy either range or xlim/ylim')
    

    x = np.linspace(x1, x2, density)
    y = np.linspace(y1, y2, density)

    X, Y = np.meshgrid(x, y)

    dx, dy = np.ones(X.shape), f(X,Y)
    if normalize:
        norm = np.sqrt(dx**2 + dy**2)
        dx, dy = dx/norm , dy/norm
    
    if plot_type == 'quiver':
        #color = np.sqrt(((dx+4)/2)*2 + ((dy+4)/2)*2)
        if color: plt.quiver(X, Y, dx, dy, dy, cmap=cmap)
        else: plt.quiver(X, Y, dx, dy)

    elif plot_type == 'streamplot':
        if color: plt.streamplot(X, Y, dx, dy, color=dy, cmap=cmap)
        else: plt.streamplot(X, Y, dx, dy, color='k')

    else:
        raise ValueError("It only accepts either 'quiver' or 'streamplot'")
    
    plt.title(f'Slope Field ({plot_type})')
    plt.xlabel('x')
    plt.ylabel('y')
    if show: plt.show()