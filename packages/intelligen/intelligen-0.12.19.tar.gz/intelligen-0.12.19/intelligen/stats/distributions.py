import numpy as np
import matplotlib.pyplot as plt
#from ..fortran.functions import erf
#from intelligen.fortran.functions import erf
from .functions import erf
#from math import erf
from typing import List, Union
Vector = List[float]

from numpy import pi, sqrt
from ..numeric import factorial, combination

__all__ = ['Distribution', 'DiscreteDistribution',
           'Bernoulli', 'Binomial', 'Geometric',
           'NegativeBinomial', 'Hypergeometric',
           'Poisson', 'Normal']

#---------------------- Distributions -----------------------#

class Distribution:
    """Main class for plotting distributions
    """


    def plot_cdf(self, show = True) -> None:
        """Plots the Cumulative distribution function of a distribution

        Args:
            show (bool, optional): Shows the plot or keep editing it. Defaults to True.
        """
        dist_name = self.__class__.__name__
        if not hasattr(self, 'CDF'):
            print(f'{dist_name} distribution doesnt support CDF plotting')
            return None
        plt.title(f'Cumulative distribution function\n{dist_name}')
        data = []
        for i in range(self.plot + 1):
            data.append(self.CDF(i))
        plt.step(range(len(data)), data, where='post')
        if show: plt.show()
    
    def plot_PDF(self, show = True) -> None:
        """Plots the Probability density function of a distribution

        Args:
            show (bool, optional): Shows the plot or keep editing it. Defaults to True.
        """
        dist_name = self.__class__.__name__
        if not hasattr(self, 'PDF'):
            print(f'{dist_name} distribution doesnt support PDF plotting')
            return None
        plt.title(f'Probability density function\n{dist_name}')
        data = []
        iter = np.linspace(-self.plot + self.origin, self.plot + self.origin, 1000)
        for i in iter:
            data.append(self.PDF(i))
        plt.plot(iter, data)
        if show: plt.show()


#------------------- Discrete Distributions --------------------#

class DiscreteDistribution(Distribution):
    
    def pmf(self, k: float) -> float:
        """
        Probability Mass Function
        =========================
        Returns the probability mass function P(x=k)

        Parameters
        ----------
        k : float
            Value
        
        Returns
        -------
        float:
            Probability
        """
    def CDF(k: float) -> float:
        """
        Cumulative Distribution Function
        ================================
        Returns the Cumulative distribution function P(x<=k)

        Parameters
        ----------
        k : float
            Value
        
        Returns
        -------
        float:
            Cumulative probability
        """

    def plot_pmf(self, show = True) -> None:
        """Plots the Probability mass function of a distribution

        Args:
            show (bool, optional): Shows the plot or keep editing it. Defaults to True.
        """
        dist_name = self.__class__.__name__
        if not hasattr(self, 'PMF'):
            print(f'{dist_name} distribution doesnt support PMF plotting')
            return None
        plt.title(f'Probability mass function\n{dist_name}')
        data = []
        for i in range(self.plot + 1):
            data.append(self.pmf(i))
        plt.plot(data)
        if show: plt.show()

class Bernoulli(DiscreteDistribution):
    """
    Bernoulli Distribution
    ======================

    Discrete probability distribution of a random variable
    which takes the value 1 with probability`p`and the
    value 0 with probability `q = 1-p`

    Parameters
    ----------
    p : float
        Probability of success
    
    Attributes
    ----------
    q : float
        `1-p`

    mean : float
        Expected value / mean 

    variance : float
        Measure of dispersion

    skewness : float
        Measure of the asymmetry

    kurtosis: float
        Measure of the "tailedness"

    Examples
    --------
    >>> from intelligen.stats import Bernoulli
    >>> B = Bernoulli(0.65)
    >>> B.pmf(0)
    0.35
    >>> B.skewness
    -0.6289709020331511

    """
    
    def __init__(self, p: float) -> None:
        self.p, self.q = p, 1-p
        self.mean = p
        self.variance = p * self.q
        self.skewness = (self.q - p) / np.sqrt(self.variance)
        self.kurtosis = (1 - 6*self.variance) / self.variance
    
    def __add__(self, distribution: Distribution) -> Distribution:
        if isinstance(distribution, self.__class__):
            if self.p == distribution.p:
                return Binomial(2, self.p)
            else: raise ValueError('Probability must be the same')
        
        elif isinstance(distribution, Binomial):
            if self.p == distribution.p:
                return Binomial(distribution.n + 1, self.p)
            else: raise ValueError('Probability must be the same')
        
        else: raise ValueError('Distributions must be compatible')
    
    def __radd__(self, distribution: Distribution) -> Distribution:
        return self + distribution
    
    def __mul__(self, coef: int) -> Distribution:
        if isinstance(coef, int) : return Binomial(coef, self.p)
        else: raise ValueError('The coeficient must be an integer')
    
    def __rmul__(self, coef: int) -> Distribution:
        return self * coef
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(p={self.p})'
        


    def pmf(self, k: int) -> float:
        if isinstance(k, list) or type(k) == np.ndarray:
            return np.array([self.pmf(i) for i in k])
        else:
            if   k == 0: return self.q
            elif k == 1: return self.p
            else: raise ValueError('R{0,1}')

    def cdf(self, k: float) -> float:
        if isinstance(k, list) or type(k) == np.ndarray:
            return np.array([self.cdf(i) for i in k])
        else:
            if   k < 0: return 0
            elif k < 1: return self.q
            else: return 1

    def plot_pmf(self, show=True):
        plt.title(f'Probability mass function\nBernoulli')
        bar_plot = plt.bar([0,1],self.pmf([1,0]), width=0.4)
        plt.bar_label(bar_plot,['p','1-p'])
        if show: plt.show()
    
    def plot_cdf(self, show=True):
        plt.title(f'Cumulative distribution function\nBernoulli')
        plt.step([-1,0,1,2],self.cdf([-1,0,1,2]), where='post')
        if show: plt.show()

class Binomial(DiscreteDistribution):
    """
    Binomial Distribution
    =====================

    Discrete probability distribution that models the number
    of successes in a sequence of `n` independent experiments
    (Bernoulli trials) with constant probability `p`

    Parameters
    ----------
    n: int
        Number of Bernoulli trials
    
    p : float
        Probability of success

    Attributes
    ----------
    q : float
        `1-p`

    mean : float
        Expected value / mean 

    variance : float
        Measure of dispersion

    skewness : float
        Measure of the asymmetry

    kurtosis: float
        Measure of the "tailedness"

    Examples
    --------
    >>> from intelligen.stats import Binomial
    >>> B = Binomial(17, 0.65)
    >>> B.pmf(10)
    0.1684553555671748
    >>> B.kurtosis
    -0.09437621202327084
    """
    
    def __init__(self, n: int, p: float) -> None:
        self.n, self.p, self.q = n, p, 1-p
        self.plot = n
        self.mean = n * p
        self.variance = n * p * self.q
        self.skewness = (self.q - p) / np.sqrt(self.variance)
        self.kurtosis = (1 - 6*p*self.q) / self.variance
    
    def __add__(self, distribution: Distribution) -> Distribution:
        if isinstance(distribution, self.__class__):
            if self.p == distribution.p:
                return Binomial(self.n + distribution.n, self.p)
            else: raise ValueError('Probability must be the same')
        
        else: raise ValueError('Distributions must be compatible')

    def __mul__(self, coef: int) -> Distribution:
        if isinstance(coef, int) : return Binomial(self.n * coef, self.p)
        else: raise ValueError('The coeficient must be an integer')
    
    def __rmul__(self, coef: int) -> Distribution:
        return self * coef
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(n={self.n}, p={self.p})'

    def pmf(self, k: int) -> float:
        if isinstance(k, list) or type(k) == np.ndarray:
            k = np.asarray(k).astype(int)
            print(k)
            #return np.array([self.pmf(i) for i in k])
        
        return combination(self.n, k) * self.p**k * (1 - self.p)**(self.n - k) 

    def cdf(self, k: float) -> float:
        if isinstance(k, list) or type(k) == np.ndarray:
            return np.array([self.cdf(i) for i in k])
        else:
            result = 0
            for i in range(int(np.floor(k))+1):
                result += combination(self.n, i) * self.p**i * (1 - self.p)**(self.n - i)
            return result

""" B = Binomial(10,0.5)
print(B.pmf([5,4])) """

class Geometric(DiscreteDistribution):
    """
    Geometric Distribution
    ======================

    Discrete probability distribution that models the number of
    Bernoulli trials `k`, needed to get one success, 
    each with success probability ``p`


    Parameters
    ----------
    p : float
        Probability of success

    Attributes
    ----------
    mean : float
        Expected value / mean 

    variance : float
        Measure of dispersion

    skewness : float
        Measure of the asymmetry

    kurtosis: float
        Measure of the "tailedness"

    Examples
    --------
    >>> from intelligen.stats import Geometric
    >>> G = Geometric(0.65)
    >>> G.CDF(3)
    0.957125
    >>> G.variance
    0.8284023668639052
    """
    def __init__(self, p: float, plot: int = None) -> None:
        self.p = p
        if plot is None: self.plot = int(10/p)
        self.mean = 1 / p
        self.variance = (1 - p) / p**2
        self.skewness = (2 - p) / np.sqrt(1 - p)
        self.kurtosis = 6 + p**2 / (1 - p)

    def __add__(self, distribution: Distribution) -> Distribution:
        if isinstance(distribution, self.__class__):
            if self.p == distribution.p:
                return NegativeBinomial(2, self.p)
            else: raise ValueError('Probability must be the same')
        
        elif isinstance(distribution, NegativeBinomial):
            if self.p == distribution.p:
                return NegativeBinomial(distribution.r + 1, self.p)
            else: raise ValueError('Probability must be the same')
        
        else: raise ValueError('Distributions must be compatible')

    def __radd__(self, distribution: Distribution) -> Distribution:
        return self + distribution

    def __mul__(self, coef: int) -> Distribution:
        if isinstance(coef, int) : return NegativeBinomial(coef, self.p)
        else: raise ValueError('The coeficient must be an integer')
    
    def __rmul__(self, coef: int) -> Distribution:
        return self * coef
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(p={self.p})'

    def pmf(self, k: int or Vector) -> float:
        if isinstance(k, int):
            return (1 - self.p)**(k - 1) * self.p
        return (1 - self.p)**(np.array(k) - 1) * self.p
    
    def CDF(self, k: float) -> float:
        return 1 - (1 - self.p)**np.floor(k)

class NegativeBinomial(DiscreteDistribution):
    """
    Negative Binomial Distribution
    =====================

    Discrete probability distribution that models the number
    of successes in a sequence of independent and identically
    distributed Bernoulli trials before a specified
    (non-random) number of failures (denoted r) occurs

    Parameters
    ----------
    r: int
        Number of successes
    
    p : float
        Probability of success

    Attributes
    ----------
    q : float
        `1-p`

    mean : float
        Expected value / mean 

    variance : float
        Measure of dispersion

    skewness : float
        Measure of the asymmetry

    kurtosis: float
        Measure of the "tailedness"

    Examples
    --------
    >>> from intelligen.stats import Binomial
    >>> B = Binomial(17, 0.65)
    >>> B.PMF(10)
    0.1684553555671748
    >>> B.kurtosis
    -0.09437621202327084
    """
    def __init__(self, r: int, p: float, plot: int = None) -> None:
        self.r, self.p = r, p
        if plot is None: self.plot = int((2*(r+4)/(1-self.p)))
        self.mean = p*r / (1 - p)
        self.variance = p*r / (1 - p)**2
        self.skewness = (1 + p) / np.sqrt(p*r)
        self.kurtosis = 6/r + (1 - p)**2 / (p*r)

    def __add__(self, distribution: Distribution) -> Distribution:
        if isinstance(distribution, self.__class__):
            if self.p == distribution.p:
                return NegativeBinomial(self.r + distribution.r, self.p)
            else: raise ValueError('Probability must be the same')
        
        else: raise ValueError('Distributions must be compatible')

    def __mul__(self, coef: int) -> Distribution:
        if isinstance(coef, int) : return NegativeBinomial(self.r * coef, self.p)
        else: raise ValueError('The coeficient must be an integer')
    
    def __rmul__(self, coef: int) -> Distribution:
        return self * coef
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(r={self.r}, p={self.p})'

    def pmf(self, k: int) -> float:
        return combination(k + self.r - 1, k) * (1 - self.p)**self.r * self.p**k
    
    def CDF(self, k: float) -> float:
        Binomial(k + self.r, self.p).CDF(k)
class Hypergeometric(DiscreteDistribution):
    
    def __init__(self, N: int, n: int, r: int) -> None:
        self.N, self.n, self.r, self.plot = N, n, r, r

    def pmf(self, k: int) -> float:
        return combination(self.r, k) * combination(self.N - self.r, self.n - k) / combination(self.N, self.n)


class Poisson(DiscreteDistribution):

    def __init__(self, l: float, plot: float = None) -> None:
        self.l = l
        if plot is None: self.plot = int(l*2) + 5
    
    def pmf(self, k: int) -> float:
        return np.exp(-self.l) * self.l**k / factorial(k)

class Normal(Distribution):

    def __init__(self, mu: float = 0, s: float = 1) -> None:
        self.mu, self.s, self.plot, self.origin = mu, s, 3*(s+1), mu
    
    def pmf(self, k: float) -> float:
        return np.exp((-1/2) * ((k - self.mu)/self.s)**2) / (self.s * np.sqrt(2*np.pi))
    
    def CDF(self, x: float) -> float:
        return 1/2 * (1 + erf((x - self.mu)/(self.s*np.sqrt(2))))
