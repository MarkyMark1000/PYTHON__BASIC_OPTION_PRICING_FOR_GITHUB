#!../venv/bin/python3
# Notes: 'ensure shebang has suitable path', 'echo $PATH' , 'ls -l',
# 'chmod +x filename'  or 'chmod 744 filename' then run './filename.py'
# or   'configure python launcher as default application for finder etc'
# The commonly used path to env does not exist on my mac, so we cannot use

import analytics.EuropeanOptionThread
import analytics.EuropeanOption
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import math
import copy

'''
This script compares the black scholes european option against the threaded
monte carlo european option, however no actual threading is performed.   It
is just a comparison of the price, delta, gamma etc to ensure the graphs look
reasonable.
A key difference between the Threaded Monte Carlo and original monte carlo is
that the desired greeks are set once and then the calculation being performed.

ie ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho")
rather than
getOptionPrice(npStock), getOptionDelta(npStock) etc.

'''


class compareEuropeanOptionToThreadedEuropeanOption():

    def __init__(self, npStock, fltStrike, fltVol, fltRiskFreeRate,
                 fltTimeToMaturity, boolIsCall, intNoIter):

        # Initiate the class with the option characteristics that we
        # are interested in.

        self.__npStock = copy.deepcopy(npStock)
        self.__fltStrike = fltStrike
        self.__fltVol = fltVol = 0.2
        self.__fltRiskFreeRate = fltRiskFreeRate
        self.__fltTimeToMaturity = fltTimeToMaturity
        self.__boolIsCall = boolIsCall
        self.__intNoIter = intNoIter

        # Build the black scholes option for comparison
        self.__objEuroBS = analytics.EuropeanOption. \
            BlackScholes(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                self.__boolIsCall)

        # Build the threaded monte carlo option for comparison
        objMonteCall = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                self.__boolIsCall,
                self.__intNoIter,
                name="MyOption")

        # Calculate the threaded monte carlo results here as it is all done
        # in one go for this class, so it is better to get it out of the way
        # once.
        (self.__pdMonteResult, self.__pdMonteSTDResult) = objMonteCall. \
            calculateOption(self.__npStock)

    # Private Functions

    def __comparePrice(self):

        # Compare the BS Price to monte price

        # Get the BS price
        npOptionPrice = self.__objEuroBS.getOptionPrice(npStock)

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSPrice': npOptionPrice,
            'MCPrice': self.__pdMonteResult['Price']})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSPrice', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCPrice', color='Green', ax=ax)
        plot.show(block=True)

    def __compareDelta(self):

        # Compare the BS Delta to monte delta

        # Get the BS delta
        npOptionDelta = self.__objEuroBS.getOptionDelta(npStock)

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSDelta': npOptionDelta,
            'MCDelta': self.__pdMonteResult['Delta']})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSDelta', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCDelta', color='Green', ax=ax)
        plot.show(block=True)

    def __compareGamma(self):

        # Compare the BS Gamma to monte gamma

        # Get the BS gamma
        npOptionGamma = self.__objEuroBS.getOptionGamma(npStock)

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSGamma': npOptionGamma,
            'MCGamma': self.__pdMonteResult['Gamma']})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSGamma', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCGamma', color='Green', ax=ax)
        plot.show(block=True)

    def __compareVega(self):

        # Compare the BS vega to monte vega

        # Get the BS vega
        npOptionVega = self.__objEuroBS.getOptionVega(npStock)

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSVega': npOptionVega,
            'MCVega': self.__pdMonteResult['Vega']})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSVega', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCVega', color='Green', ax=ax)
        plot.show(block=True)

    def __compareTheta(self):

        # Compare the BS Theta to monte theta

        # Get the BS theta
        npOptionTheta = self.__objEuroBS.getOptionTheta(npStock)

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSTheta': npOptionTheta,
            'MCTheta': self.__pdMonteResult['Theta']})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSTheta', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCTheta', color='Green', ax=ax)
        plot.show(block=True)

    def __compareRho(self):

        # Compare the BS rho to monte rho

        # Get the BS rho
        npOptionRho = self.__objEuroBS.getOptionRho(npStock)

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSRho': npOptionRho,
            'MCRho': self.__pdMonteResult['Rho']})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSRho', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCRho', color='Green', ax=ax)
        plot.show(block=True)

    # Public Functions

    def compareBStoThreadedEuropeanOption(self):

        # Compares the results from the black scholes calculation to that
        # from the threaded european monte carlo

        # First, do price
        self.__comparePrice()

        # Next, do the delta
        self.__compareDelta()

        # Next, do gamma
        self.__compareGamma()

        # Next, do vega
        self.__compareVega()

        # Next, do theta
        self.__compareTheta()

        # Finally, do Rho
        self.__compareRho()


if __name__ == "__main__":

    print("\n**************************************************************\n")
    print("**********************  START *********************************\n")
    print("***************************************************************\n")

    # Set data to price the option
    fltStrike = 50

    # First build a set of stock prices that go from 50% of the strike price
    # to 150% of the strike price
    npStock = np.empty(100)
    for i in range(0, 100):
        npStock[i] = (i + 50) * fltStrike / 100

    # Next, compare call option characteristics

    print("\n  ---- comparing call option ---\n\n")

    # Build comparison object
    objCall = compareEuropeanOptionToThreadedEuropeanOption(
        npStock=npStock,
        fltStrike=fltStrike,
        fltVol=0.2,
        fltRiskFreeRate=0.01,
        fltTimeToMaturity=1,
        boolIsCall=True,
        intNoIter=20000)

    # Run comparison
    objCall.compareBStoThreadedEuropeanOption()

    # Next, compare put option characteristics

    print("\n  ---- comparing put option ---\n\n")

    # Build comparison object
    objPut = compareEuropeanOptionToThreadedEuropeanOption(
        npStock=npStock,
        fltStrike=fltStrike,
        fltVol=0.2,
        fltRiskFreeRate=0.01,
        fltTimeToMaturity=1,
        boolIsCall=False,
        intNoIter=20000)

    # Run comparison
    objPut.compareBStoThreadedEuropeanOption()
