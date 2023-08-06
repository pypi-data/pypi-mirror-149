from typing import List
Vector = List[float]
Matrix2D = List[Vector]

import numpy as np
import matplotlib.pyplot as plt
from .stats import mean_squared_error

# Bibliography https://github.com/arseniyturin/SGD-From-Scratch/blob/master/Gradient%20Descent.ipynb

class LinearRegression:

    def fit(self, X: Matrix2D, y: Vector) -> None:
        """
        Fits the data and calculates the coefficients of the linear regression

        Parameters
        ----------
        X : Matrix2D
            Data
        y : Vector
            Target
        """
        
        self.X = np.asarray(X)
        self.y = np.asarray(y)
        X, y = self.X, self.y

        if len(X.shape) == 1 or X.shape[1:] == np.ones(X.shape[1:]).all():
            # Least Square Error (minimizes mean square error)
            self.coeffs = ((np.mean(X) * np.mean(y) - np.mean(X*y)) / ((np.mean(X)**2) - np.mean(X**2)))
            self.b = np.mean(y) - self.coeffs * np.mean(X)
            self.uni_dim = True
        else:
            self.coeffs = np.linalg.inv(X.T @ X) @ X.T @ y
            self.b = np.mean(y) - np.mean(X, axis=0) @ self.coeffs
            self.uni_dim = False
    
    def coef_(self) -> Vector:
        """
        Returns the coefficients

        Returns
        -------
        Vector
            The vector of coefficients
        """
        
        return self.coeffs
    
    def intercept_(self) -> float:
        """Returns the intercept value
        Returns:
            float: Intercept value
        """
        return self.b

    def predict(self, X: Matrix2D = None) -> Vector:
        """Returns the predicted data once fitted
        Args:
            X (Matrix2D, optional): Data to predict. Defaults to None (takes the fitted data)
        Returns:
            Vector: The predicted data
        """
        if X is None: X = self.X

        if self.uni_dim: self.y_pred = X * self.coeffs + self.b
        else: self.y_pred = X @ self.coeffs + self.b
        return self.y_pred
    
    def mse(self, y_real: Vector = None, y_pred: Vector = None) -> float:
        """Returns the mean squared error
        Args:
            y_real (Vector, optional): Real data. Defaults to None (takes the fitted data)
            y_pred (Vector, optional): Predicted data. Defaults to None (takes the predicted data)
        Returns:
            float: Mean squared error
        """
        if y_real is None: y_real = self.y
        if y_pred is None: y_pred = self.y_pred
        return mean_squared_error(y_real, y_pred)

    def plot(self, show: bool = True, delimeters: bool = False) -> None:
        """Plots the linear regression data against the real data
        Args:
            show (bool, optional): This shows the plot. Defaults to True.
            delimeters (bool, optional): This shows the delimeters of the surface that is plot. Defaults to False.
        """
        if self.uni_dim:
            plt.title('Simple Linear Regression')
            plt.ylim(min(self.y), max(self.y))
            plt.plot(self.X, self.y_pred, c='red')
            plt.scatter(self.X, self.y, c='#325aa8', s=15)
            if show: plt.show()

        elif self.X.shape[1] == 2:
            plt.title('Multiple Linear Regression')
            ax = plt.axes(projection = '3d')

            min_x = np.min(self.X, axis = 0)
            max_x = np.max(self.X, axis = 0)

            x_axis = np.array([min_x[0],max_x[0]])
            y_axis = np.array([min_x[1],max_x[1]])

            x1, x2 = np.meshgrid(x_axis, y_axis)
            y = x1 * self.coeffs[0] + x2 * self.coeffs[1] + self.b

            ax.plot_surface(x1, x2, y, color = 'royalblue', alpha = 0.5)
            ax.scatter(self.X[:, 0], self.X[:, 1], self.y, c = 'lightcoral')
            if delimeters: ax.scatter(x1, x2, y, c = 'royalblue', alpha = 0.5)
            if show: plt.show()

class GradientDescent:

    def __init__(self) -> None:
        """Initialize the parameters
        """
        self.m, self.b = 0.2, 0.2
        self.log, self.mse = [], []

    def fit(self, X: Vector, y: Vector, lr: float = 0.05, epoch: int = 10, stochastic: bool = False, batch_size: int = 2) -> None:
        """Calculates the parameters to fit the data
        Args:
            X (Vector): Data
            y (Vector): Target
            lr (float, optional): Describes how big are the steps in every iteration. Defaults to 0.05.
            epoch (int, optional): Describes how many iterations will perform. Defaults to 10.
            stochastic (bool, optional): Performs the sthochastic gradient descend instead. Defaults to False.
            batch_size (int, optional): The size of the data that takes the sthochastic gradient descend. Defaults to 2.
        """
        self.X = np.array(X)
        self.y = np.array(y)
        self.sgd = stochastic
        N, X, y = len(X), self.X, self.y

        for _ in range(epoch):
            if stochastic:
                indexes = np.random.randint(0, len(self.X), batch_size)
                X = np.take(self.X, indexes)
                y = np.take(self.y, indexes)
                N = len(X)
            
            f = y - (self.m * X + self.b)
            # Updating m and b
            self.m -= lr * ((-2 * X @ f).sum() / N)
            self.b -= lr * (-2 * f.sum() / N)
            
            self.log.append((self.m, self.b))
            self.mse.append(mean_squared_error(self.y, (self.m * self.X + self.b)))

    def predict(self, X: Vector = None) -> Vector:
        """Returns the predicted data once fitted
        Args:
            X (Vector, optional): Data to predict. Defaults to None (takes the fitted data)
        Returns:
            Vector: The predicted data
        """
        if X is None: X = self.X
        self.y_pred = self.m * X + self.b
        return self.y_pred

    def plot(self, log: bool = False, show: bool = True, mse: bool = True) -> None:
        """Plots the predicted data against the real data
        Args:
            log (bool, optional): This shows the evolution of the predicted data. Defaults to False.
            show (bool, optional): This shows the plot. Defaults to True.
            mse (bool, optional): This shows the evolution of the error. Defaults to True.
        """
        if mse:
            fig, axs = plt.subplots(2)
            fig.set_size_inches(6.4, 9, forward = True)
            if self.sgd:
                axs[0].set_title('Stochastic Gradient Descent')
                axs[1].set_title('Stochastic Gradient Descent Optimization')
            else:
                axs[0].set_title('Gradient Descent')
                axs[1].set_title('Gradient Descent Optimization')

            axs[1].plot(range(len(self.mse)), self.mse)
            axs[1].set_xlabel('Epochs')
            axs[1].set_ylabel('MSE')

            if log: 
                for i in range(len(self.log)):
                    axs[0].plot(self.X, self.log[i][0] * self.X + self.log[i][1], lw=1, c='orange', alpha=0.25)
            
            axs[0].plot(self.X, self.y_pred, c='red')
            axs[0].scatter(self.X, self.y, c='#325aa8', s=15)
            if show: plt.show()
        
        else:
            if self.sgd:
                plt.title('Stochastic Gradient Descent Optimization')
            else:
                plt.title('Gradient Descent Optimization')
            plt.ylim(min(self.y), max(self.y))
            
            if log: 
                for i in range(len(self.log)):
                    plt.plot(self.X, self.log[i][0] * self.X + self.log[i][1], lw=1, c='orange', alpha=0.25)
            
            plt.plot(self.X, self.y_pred, c='red')
            plt.scatter(self.X, self.y, c='#325aa8', s=15)
            if show: plt.show()

    def plot_mse(self, show: bool = True) -> None:
        """This plots the evolution of the error
        Args:
            show (bool, optional): This shows the plot. Defaults to True.
        """
        plt.title('Gradient Descent Optimization')
        plt.plot(range(len(self.mse)), self.mse)
        plt.xlabel('Epochs')
        plt.ylabel('MSE')
        if show: plt.show()       

    def show_mse(self, y_real: Vector = None, y_pred: Vector = None) -> float:
        """Returns the mean squared error
        Args:
            y_real (Vector, optional): Real data. Defaults to None (takes the fitted data)
            y_pred (Vector, optional): Predicted data. Defaults to None (takes the predicted data)
        Returns:
            float: Mean squared error
        """
        if y_real is None: y_real = self.y
        if y_pred is None: y_pred = self.y_pred
        return mean_squared_error(y_real, y_pred)


def main() -> None:
    """ x = np.random.rand(1000) * 4 -2
    y = np.random.rand(1000) * 4 -2 
    X = np.array([x, y]).T
    Y = x * np.exp(-x**2 - y**2) """
    
    X = np.random.rand(10000) * 4 -2
    Y = X + np.random.random(X.shape)*4

    """ X = np.concatenate((X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X))
    y = np.concatenate((y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y))
    X = np.concatenate((X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X))
    y = np.concatenate((y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y))
    X = np.concatenate((X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X))
    Y = np.concatenate((y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y,y)) """

    s = time()
    MLR = LinearRegression()
    MLR.fit(X, Y)
    y_pred = MLR.predict()
    f = time()
    MLR.plot()
    print(f'Error linr: {MLR.mse()}, time:{f-s}')


    s = time()
    GD = GradientDescent()
    GD.fit(X, Y, epoch=50)
    y_pred2 = GD.predict()
    f = time()
    GD.plot(log = True)
    #GD.plot_mse()
    print(f'Error GD  : {GD.mse[-1]}, time:{f-s}')


    s = time()
    SGD = GradientDescent()
    SGD.fit(X, Y, epoch=50, stochastic=True)
    y_pred2 = SGD.predict()
    f = time()
    SGD.plot(log = True)
    #GD.plot_mse()
    print(f'Error SGD : {SGD.mse[-1]}, time:{f-s}')


if __name__ == '__main__':
    from time import time
    main()