import numpy as np
import pandas as pd
import scipy.stats as si
import math
import copy

'''
This section calculates the boundary conditions for a European Option, which
can be used in tests to ensure any european option calculation results are
reasonable.
A call option has a lower boundary of max [S - K x Exp(-rT), 0]
A put option has a lower boundary of max [K x Exp(-rT) - S, 0]
A call has an upper boundary of the stock price
A put has an upper boundary of K x Exp(-rt)

'''


class EuropeanOptionBoundaryConditions():

    # Private Functions
    def __init__(self, fltStrike, boolIsCall, fltRate, fltTimeToMaturity):
        self.__fltStrike = fltStrike
        self.__boolIsCall = boolIsCall
        self.__fltRate = fltRate
        self.__fltTimeToMaturity = fltTimeToMaturity

    def __str__(self):
        strF = 'OptionBoundaryConditions: [Strike:{strike}; IsCall:{iscall};]'
        return strF.format(strike=self.__fltStrike, iscall=self.__boolIsCall)

    # Public Functions
    def getLowerBoundary(self, npStock):

        if self.__boolIsCall:

            # Lower boundary for call is max( S - K x Exp(-rT), 0)
            npLower = np.maximum(
                npStock - self.__fltStrike * math.exp(
                    -self.__fltRate * self.__fltTimeToMaturity),
                0)

        else:

            # Lower boundary for put is max ( K x Exp(-rT) - S, 0)
            npLower = np.maximum(
                self.__fltStrike * math.exp(
                    -self.__fltRate * self.__fltTimeToMaturity)
                - npStock,
                0)

        # return npLower[:, 0]
        return npLower

    def getUpperBoundary(self, npStock):

        if self.__boolIsCall:

            # Call must always be worth less than the stock price
            npUpper = copy.deepcopy(npStock)

        else:

            # Upper boundary for put is K x Exp(-rT)
            fltUB = self.__fltStrike * math.exp(
                    -self.__fltRate * self.__fltTimeToMaturity)

            # Fill numpy array with the result
            npUpper = np.empty(len(npStock))
            npUpper.fill(fltUB)

        # return npUpper[:, 0]
        return npUpper
