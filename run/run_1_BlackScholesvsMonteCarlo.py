#!../venv/bin/python3
# Notes: 'ensure shebang has suitable path', 'echo $PATH' , 'ls -l',
# 'chmod +x filename'  or 'chmod 744 filename' then run './filename.py'
# or   'configure python launcher as default application for finder etc'
# The commonly used path to env does not exist on my mac, so we cannot use

import analytics.EuropeanOption
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import math
import copy

'''
This section compares the EuropeanOption.BlackScholes model to the
BasicMonteCarloOption option.   Firstly it creates a CALL comparison class
and then plots the price, delta, gamma etc.   Next it creates a PUT
comparison class and then plots the price, delta, gamma etc.
'''


class compareBlackScholesToMonteCarloOption():

    def __init__(self, npStock, fltStrike, fltVol, fltRiskFreeRate,
                 fltTimeToMaturity, boolIsCall, intNoIter):

        # Set the variables to price the option
        self.__npStock = copy.deepcopy(npStock)
        self.__fltStrike = fltStrike
        self.__fltVol = fltVol
        self.__fltRiskFreeRate = fltRiskFreeRate
        self.__fltTimeToMaturity = fltTimeToMaturity
        self.__boolIsCall = boolIsCall
        self.__intNoIter = intNoIter

        # Create an object that represents the Black Scholes calc
        self.__objBlackScholes = analytics.EuropeanOption. \
            BlackScholes(
                fltStrike=self.__fltStrike,
                fltVol=self.__fltVol,
                fltRiskFreeRate=self.__fltRiskFreeRate,
                fltTimeToMaturity=self.__fltTimeToMaturity,
                boolIsCall=self.__boolIsCall
            )

        # Create an object that represents the Monte Carlo calc
        self.__objMonte = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                fltStrike=self.__fltStrike,
                fltVol=self.__fltVol,
                fltRiskFreeRate=self.__fltRiskFreeRate,
                fltTimeToMaturity=self.__fltTimeToMaturity,
                boolIsCall=self.__boolIsCall,
                intNoIter=self.__intNoIter)

    def __comparePrice(self):

        # Compare the Option Price

        # Get the black scholes value
        npBSValue = self.__objBlackScholes.getOptionPrice(self.__npStock)

        # Get the monte carlo value
        # (npMonteValue, npOptionMonteSTD) = self.__objMonte. \
        #     getOptionPrice(npStock)
        npMonteValue = self.__objMonte. \
             getOptionPrice(npStock)[0]

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSPrice': npBSValue,
            'MCPrice': npMonteValue})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSPrice', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCPrice', color='Green', ax=ax)
        plot.show(block=True)

    def __compareDelta(self):

        # Compare the Option Delta

        # Get the black scholes value
        npBSDelta = self.__objBlackScholes.getOptionDelta(self.__npStock)

        # Get the monte carlo value
        npMonteDelta = self.__objMonte. \
            getOptionDelta(npStock)[0]

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSDelta': npBSDelta,
            'MCDelta': npMonteDelta})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSDelta', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCDelta', color='Green', ax=ax)
        plot.show(block=True)

    def __compareGamma(self):

        # Compare the Option Gamma

        # Get the black scholes value
        npBSGamma = self.__objBlackScholes.getOptionGamma(self.__npStock)

        # Get the monte carlo value
        npMonteGamma = self.__objMonte. \
            getOptionGamma(npStock)[0]

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSGamma': npBSGamma,
            'MCGamma': npMonteGamma})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSGamma', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCGamma', color='Green', ax=ax)
        plot.show(block=True)

    def __compareVega(self):

        # Compare the Option Vega

        # Get the black scholes value
        npBSVega = self.__objBlackScholes.getOptionVega(self.__npStock)

        # Get the monte carlo value
        npMonteVega = self.__objMonte. \
            getOptionVega(npStock)[0]

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSVega': npBSVega,
            'MCVega': npMonteVega})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSVega', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCVega', color='Green', ax=ax)
        plot.show(block=True)

    def __compareTheta(self):

        # Compare the Option Theta

        # Get the black scholes value
        npBSTheta = self.__objBlackScholes.getOptionTheta(self.__npStock)

        # Get the monte carlo value
        npMonteTheta = self.__objMonte. \
            getOptionTheta(npStock)[0]

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSTheta': npBSTheta,
            'MCTheta': npMonteTheta})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSTheta', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCTheta', color='Green', ax=ax)
        plot.show(block=True)

    def __compareRho(self):

        # Compare the Option Rho

        # Get the black scholes value
        npBSRho = self.__objBlackScholes.getOptionRho(self.__npStock)

        # Get the monte carlo value
        npMonteRho = self.__objMonte. \
            getOptionRho(npStock)[0]

        # Build a dataframe with the results
        pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'BSRho': npBSRho,
            'MCRho': npMonteRho})

        # Plot the results.
        ax = pdResults.plot.line(x='StockPrice', y='BSRho', color='Blue')
        pdResults.plot.line(x='StockPrice', y='MCRho', color='Green', ax=ax)
        plot.show(block=True)

    # Public Functions

    def compareOptions(self):

        # First, price
        self.__comparePrice()

        # Next, delta
        self.__compareDelta()

        # Next, gamma
        self.__compareGamma()

        # Next, vega
        self.__compareVega()

        # Next, theta
        self.__compareTheta()

        # Next, rho
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

    print(" --- compare CALL options ---")

    # Build a comparison object for call options
    objCompCall = compareBlackScholesToMonteCarloOption(npStock=npStock,
                                                        fltStrike=fltStrike,
                                                        fltVol=0.2,
                                                        fltRiskFreeRate=0.01,
                                                        fltTimeToMaturity=1,
                                                        boolIsCall=True,
                                                        intNoIter=20000)

    # Run the comparison
    objCompCall.compareOptions()

    print(" --- compare PUT options ---")

    # Build a comparison object for put options
    objCompPut = compareBlackScholesToMonteCarloOption(npStock=npStock,
                                                       fltStrike=fltStrike,
                                                       fltVol=0.2,
                                                       fltRiskFreeRate=0.01,
                                                       fltTimeToMaturity=1,
                                                       boolIsCall=False,
                                                       intNoIter=20000)

    # Run the comparison
    objCompPut.compareOptions()
