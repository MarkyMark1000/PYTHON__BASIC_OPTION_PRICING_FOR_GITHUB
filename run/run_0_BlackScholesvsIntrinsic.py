#!../venv/bin/python3
# Notes: 'ensure shebang has suitable path', 'echo $PATH' , 'ls -l',
# 'chmod +x filename'  or 'chmod 744 filename' then run './filename.py'
# or   'configure python launcher as default application for finder etc'
# The commonly used path to env does not exist on my mac, so we cannot use

import analytics.OptionIntrinsicValue
import analytics.EuropeanOption
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import math
import copy

'''
This section compares the EuropeanOption.BlackScholes model to the Intrinsic
value of an option using the OptionInstrinsicValue class.   It is purely a
plot of the value - no greeks etc.
'''


class compareBlackScholesToIntrinsicValue():

    def __init__(self, npStock, fltStrike, fltVol, fltRiskFreeRate,
                 fltTimeToMaturity, boolIsCall):

        # Set the variables to price the option
        self.__npStock = copy.deepcopy(npStock)
        self.__fltStrike = fltStrike
        self.__fltVol = fltVol
        self.__fltRiskFreeRate = fltRiskFreeRate
        self.__fltTimeToMaturity = fltTimeToMaturity
        self.__boolIsCall = boolIsCall

        # Create an object that represents the intrinsic value
        self.__objIntrinsicOption = analytics.OptionIntrinsicValue. \
            OptionIntrinsicValue(
                fltStrike=self.__fltStrike,
                boolIsCall=self.__boolIsCall
            )

        # Create an object that represents the Black Scholes calc
        self.__objBlackScholes = analytics.EuropeanOption. \
            BlackScholes(
                fltStrike=self.__fltStrike,
                fltVol=self.__fltVol,
                fltRiskFreeRate=self.__fltRiskFreeRate,
                fltTimeToMaturity=self.__fltTimeToMaturity,
                boolIsCall=self.__boolIsCall
            )

    def compareBSwithIntrinsic(self):

        # This compares the black scholes price with the intrinsic value

        # Get the intrinsic price
        npIntrinsicPrice = self.__objIntrinsicOption.getOptionPrice(npStock)

        # Get the BS price
        npBSPrice = self.__objBlackScholes.getOptionPrice(npStock)

        pdResults = pd.DataFrame(
            {'StockPrice': npStock,
             'IntrinsicValue': npIntrinsicPrice,
             'BlackScholesValue': npBSPrice})
        ax = pdResults.plot.line(x='StockPrice', y='IntrinsicValue')
        pdResults.plot.line(x='StockPrice', y='BlackScholesValue', ax=ax)
        plot.show(block=True)


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

    # First compare call option
    print(" ----- compare call option ----")

    # Create a call comparison object
    objCompCall = compareBlackScholesToIntrinsicValue(npStock=npStock,
                                                      fltStrike=fltStrike,
                                                      fltVol=0.2,
                                                      fltRiskFreeRate=0.01,
                                                      fltTimeToMaturity=1,
                                                      boolIsCall=True)

    # Compare the black scholes and intrinsic value
    objCompCall.compareBSwithIntrinsic()

    # Next compare put option
    print(" ----- compare put option ----")

    # Create a put comparison object
    objCompPut = compareBlackScholesToIntrinsicValue(npStock=npStock,
                                                     fltStrike=fltStrike,
                                                     fltVol=0.2,
                                                     fltRiskFreeRate=0.01,
                                                     fltTimeToMaturity=1,
                                                     boolIsCall=False)

    # Compare the black scholes and intrinsic value
    objCompPut.compareBSwithIntrinsic()
