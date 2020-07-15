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


def compareEuropeanOptionToIntrinsicValue(npStock, fltStrike):
    # Within this function I am going to compare the intrinsic value of
    # an option to the EuropeanOption calculation.

    print("\n------- compareEuropeanOptionToIntrinsicValue --------\n")

    # Set data to price the option
    fltVol = 0.2
    fltRiskFreeRate = 0.01
    fltTimeToMaturity = 1

    # Initiate Call Option's
    objIntrinsicCall = analytics.OptionIntrinsicValue. \
        OptionIntrinsicValue(
            fltStrike,
            True)
    print(objIntrinsicCall)
    objEuropeanCall = analytics.EuropeanOption. \
        BlackScholes(
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            True)
    print(objEuropeanCall)

    # Plot the Call Option intrinsic value and price, add it to a dataframe
    # and then plot it.
    npIntrinsicPrice = objIntrinsicCall.getOptionPrice(npStock)
    npCallPrice = objEuropeanCall.getOptionPrice(npStock)
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'IntrinsicValue': npIntrinsicPrice,
         'EuropeanCall': npCallPrice})
    ax = pdResults.plot.line(x='StockPrice', y='IntrinsicValue')
    pdResults.plot.line(x='StockPrice', y='EuropeanCall', ax=ax)
    plot.show(block=True)

    # Print out a sample price
    intI = int(npStock.shape[0] / 2)
    strF = "\nSample Price Comparison Spot, Intrinisc, BlackScholes: \
        {spot}, {pIntrinsic}, {pBS}\n"
    print(strF.format(
        spot=npStock[intI],
        pIntrinsic=npIntrinsicPrice[intI],
        pBS=npCallPrice[intI]))

    # Initiate Put Option's
    objIntrinsicPut = analytics.OptionIntrinsicValue. \
        OptionIntrinsicValue(
            fltStrike,
            False)
    print(objIntrinsicPut)
    objEuropeanPut = analytics.EuropeanOption. \
        BlackScholes(
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            False)
    print(objEuropeanPut)

    # Plot the Call Option intrinsic value and price, add it to a dataframe
    # and then plot it.
    npIntrinsicPrice = objIntrinsicPut.getOptionPrice(npStock)
    npPutPrice = objEuropeanPut.getOptionPrice(npStock)
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'IntrinsicValue': npIntrinsicPrice,
         'EuropeanPut': npPutPrice})
    ax = pdResults.plot.line(x='StockPrice', y='IntrinsicValue')
    pdResults.plot.line(x='StockPrice', y='EuropeanPut', ax=ax)
    plot.show(block=True)

    # Print out a sample price
    intI = int(npStock.shape[0] / 2)
    strF = "\nSample Price Comparison Spot, Intrinisc, BlackScholes: \
        {spot}, {pIntrinsic}, {pBS}\n"
    print(strF.format(
        spot=npStock[intI],
        pIntrinsic=npIntrinsicPrice[intI],
        pBS=npPutPrice[intI]))


def compareEuropeanOptionToMonteCarloOption(npStock, fltStrike):
    # Within this function I am going to compare the Black Scholes European
    # Option to a monte carlo calculation.

    print("\n------- compareEuropeanOptionToMonteCarloOption --------\n")

    # Set data to price the option
    fltVol = 0.2
    fltRiskFreeRate = 0.01
    fltTimeToMaturity = 1
    intNoIter = 20000

    # Initiate a EuropeanCall, EuropeanPut, MonteCarloCall, MonteCarloPut
    objEuroCall = analytics.EuropeanOption. \
        BlackScholes(
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            True)
    objEuroPut = analytics.EuropeanOption. \
        BlackScholes(
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            False)
    objMonteCall = analytics.EuropeanOption. \
        BasicMonteCarloOption(
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            True,
            intNoIter)
    objMontePut = analytics.EuropeanOption. \
        BasicMonteCarloOption(
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            False,
            intNoIter)
    print(objEuroCall)
    print(objEuroPut)
    print(objMonteCall)
    print(objMontePut)

    # Compare the Call Option Price
    npOptionPrice = objEuroCall.getOptionPrice(npStock)
    (npOptionMontePrice, npOptionMonteSTD) = objMonteCall. \
        getOptionPrice(npStock)

    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSCallPrice': npOptionPrice,
         'MCCallPrice': npOptionMontePrice})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallPrice', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallPrice', color='Green', ax=ax)
    plot.show(block=True)

    # Print out a sample price
    intI = int(npStock.shape[0] / 2)
    strF = "\nSample Price Comparison Spot, BlackScholes, Monte: \
        {spot}, {pBS}, {pMonte}\n"
    print(strF.format(spot=npStock[intI],
                      pBS=npOptionPrice[intI],
                      pMonte=npOptionMontePrice[intI]))

    # Compare the Put Option Price
    npOptionPrice = objEuroPut.getOptionPrice(npStock)
    (npOptionMontePrice, npOptionMonteSTD) = objMontePut. \
        getOptionPrice(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSPutPrice': npOptionPrice,
         'MCPutPrice': npOptionMontePrice})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutPrice', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutPrice', color='Green', ax=ax)
    plot.show(block=True)

    # Print out a sample price
    intI = int(npStock.shape[0] / 2)
    strF = "\nSample Price Comparison Spot, BlackScholes, Monte: \
        {spot}, {pBS}, {pMonte}\n"
    print(strF.format(spot=npStock[intI],
                      pBS=npOptionPrice[intI],
                      pMonte=npOptionMontePrice[intI]))

    # Compare the Call Option Delta
    npOptionDelta = objEuroCall.getOptionDelta(npStock)
    (npOptionMonteDelta, npOptionMonteSTD) = objMonteCall. \
        getOptionDelta(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSCallDelta': npOptionDelta,
         'MCCallDelta': npOptionMonteDelta})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallDelta', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallDelta', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Put Option Delta
    npOptionDelta = objEuroPut.getOptionDelta(npStock)
    (npOptionMonteDelta, npOptionMonteSTD) = objMontePut. \
        getOptionDelta(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSPutDelta': npOptionDelta,
         'MCPutDelta': npOptionMonteDelta})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutDelta', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutDelta', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Call Option Gamma
    npOptionGamma = objEuroCall.getOptionGamma(npStock)
    (npOptionMonteGamma, npOptionMonteSTD) = objMonteCall. \
        getOptionGamma(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSCallGamma': npOptionGamma,
         'MCCallGamma': npOptionMonteGamma})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallGamma', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallGamma', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Put Option Gamma
    npOptionGamma = objEuroPut.getOptionGamma(npStock)
    (npOptionMonteGamma, npOptionMonteSTD) = objMontePut. \
        getOptionGamma(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSPutGamma': npOptionGamma,
         'MCPutGamma': npOptionMonteGamma})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutGamma', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutGamma', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Call Option Vega
    npOptionVega = objEuroCall.getOptionVega(npStock)
    (npOptionMonteVega, npOptionMonteSTD) = objMonteCall.getOptionVega(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSCallVega': npOptionVega,
         'MCCallVega': npOptionMonteVega})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallVega', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallVega', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Put Option Vega
    npOptionVega = objEuroPut.getOptionVega(npStock)
    (npOptionMonteVega, npOptionMonteSTD) = objMontePut.getOptionVega(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSPutVega': npOptionVega,
         'MCPutVega': npOptionMonteVega})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutVega', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutVega', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Call Option Theta
    npOptionTheta = objEuroCall.getOptionTheta(npStock)
    (npOptionMonteTheta, npOptionMonteSTD) = objMonteCall. \
        getOptionTheta(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSCallTheta': npOptionTheta,
         'MCCallTheta': npOptionMonteTheta})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallTheta', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallTheta', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Put Option Theta
    npOptionTheta = objEuroPut.getOptionTheta(npStock)
    (npOptionMonteTheta, npOptionMonteSTD) = objMontePut. \
        getOptionTheta(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSPutTheta': npOptionTheta,
         'MCPutTheta': npOptionMonteTheta})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutTheta', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutTheta', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Call Option Rho
    npOptionRho = objEuroCall.getOptionRho(npStock)
    (npOptionMonteRho, npOptionMonteSTD) = objMonteCall.getOptionRho(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSCallRho': npOptionRho,
         'MCCallRho': npOptionMonteRho})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallRho', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallRho', color='Green', ax=ax)
    plot.show(block=True)

    # Compare the Put Option Rho
    npOptionRho = objEuroPut.getOptionRho(npStock)
    (npOptionMonteRho, npOptionMonteSTD) = objMontePut.getOptionRho(npStock)
    # Build a dataframe with the results
    pdResults = pd.DataFrame(
        {'StockPrice': npStock,
         'BSPutRho': npOptionRho,
         'MCPutRho': npOptionMonteRho})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutRho', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutRho', color='Green', ax=ax)
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

    pdStock = pd.Series(npStock, name='StockPrice')

    # Compare European Option to Intrinsic Value
    compareEuropeanOptionToIntrinsicValue(npStock, fltStrike)

    # Now Compare European Option to Monte Carlo Option
    compareEuropeanOptionToMonteCarloOption(npStock, fltStrike)
