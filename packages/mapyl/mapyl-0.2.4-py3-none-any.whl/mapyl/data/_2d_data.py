import numpy as np
import random

class GenData:
    def generate_data(deg5 = 0, deg4 = 0, deg3 = 0, deg2 = 0, ang=1.5, yint=2, noise=1, xrange = 10, floor=-5, numins=200):
        '''
        Generates noisy polynomial data for testing

        Parameters:
            deg5 to deg2 (float): The coefficients for the various degrees from 2 to 5, zero to ignore this degree

            ang (float): The angular coefficient (the same as deg in the previous parameter)

            yint (float): The Y-intercept of the polynomial

            noise (float): The amount of noise to be present, keep in mind this does not scale with the y value

            xrange (float): The range for x to be calculated (low values are recommended for perfomarnce)

            floor (float): The minimum value for x to be computed

            numins (int): The amount of x samples to be calculated

        Returns:
            x (array): The x values used (after scale)

            y (array): The y values produced

        '''
        x = xrange * np.random.rand(numins, 1) + floor
        degs =  deg5*x**5 + deg4*x**4 + deg3*x**3 + deg2*x**2 + ang*x
        _noise = yint + (noise * 10 * (np.amax(degs)/70) * np.random.randn(200, 1))
        y = degs + _noise

        return x, y


class SplitData:
    def split(X, y, test_percent):
        """
        Splits a dataset into a test and train percentile along the vertical dimension

        Parameters:
            X (ndarray): The X values

            y (ndarray): The y values

            test_percent (float): The percentage of the dataset that is for testing

        Returns:
            ndarray: the splitted ndarrays of the X and y inputs
        """
        if (len(X) % 2) == 0:
            _test = 1
        test_x = X[:int(((len(X)) + 1)*test_percent)]
        train_x = X[-(int(((len(X)))*(1-test_percent))):]
        if y is not None:
            train_y = y[:int(((len(X))+1)*(1-test_percent))]
            test_y = y[int(((len(X))+1)*test_percent):]
            return train_x, test_x, train_y, test_y
        return train_x, test_x