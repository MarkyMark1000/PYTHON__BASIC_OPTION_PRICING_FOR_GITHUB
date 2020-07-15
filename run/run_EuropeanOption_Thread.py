#!../venv/bin/python3
# Notes: 'ensure shebang has suitable path', 'echo $PATH' , 'ls -l',
# 'chmod +x filename'  or 'chmod 744 filename'
# then run './filename.py'   or   'configure python launcher as default
# application for finder etc'
# The commonly used path to env does not exist on my mac, so we cannot use

import analytics.EuropeanOption
import analytics.EuropeanOptionThread
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import time
import queue

# When my first attempt at threading option's failed, I tried another approach
# based upon the following example:

# https://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping

# EuropeanOptionThread uses a queue to pass data into the thread and then
# passes data back out once it has finished calculating.


def compareEuropeanOptionToMonteCarloThreadOption(npStock, fltStrike):
    # Within this function I am going to compare the Black Scholes European
    # Option to a monte carlo calculation.

    print("\n------- compareEuropeanOptionToMonteCarloThreadOption --------\n")

    # Set data to price the option
    fltVol = 0.2
    fltRiskFreeRate = 0.01
    fltTimeToMaturity = 1
    intNoIter = 20000

    # Initiate a EuropeanCall, EuropeanPut, MonteCarloCall, MonteCarloPut
    objEuroCall = analytics.EuropeanOption. \
        BlackScholes(fltStrike,
                     fltVol,
                     fltRiskFreeRate,
                     fltTimeToMaturity,
                     True)
    objEuroPut = analytics.EuropeanOption. \
        BlackScholes(fltStrike,
                     fltVol,
                     fltRiskFreeRate,
                     fltTimeToMaturity,
                     False)
    objMonteCall = analytics.EuropeanOptionThread. \
        BasicMonteCarloOptionThreaded(
            ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            True,
            intNoIter,
            name="MyCallOption")
    objMontePut = analytics.EuropeanOptionThread. \
        BasicMonteCarloOptionThreaded(
            ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            False,
            intNoIter,
            name="MyPutOption")
    print(objEuroCall)
    print(objEuroPut)
    print(objMonteCall)
    print(objMontePut)

    # Get the calculation results for the call and put
    (pdResultsCall, pdResultsSTDCall) = objMonteCall.calculateOption(npStock)
    (pdResultsPut, pdResultsSTDPut) = objMontePut.calculateOption(npStock)

    # Get the European Option Price
    npOptionPrice = objEuroCall.getOptionPrice(npStock)

    # Build a dataframe with the results
    pdResults = pd.DataFrame({
        'StockPrice': npStock,
        'BSCallPrice': npOptionPrice,
        'MCCallPrice': pdResultsCall['Price'],
        'minusSTD': (pdResultsCall['Price'] - pdResultsSTDCall['PriceSTD']),
        'plusSTD': (pdResultsCall['Price'] + pdResultsSTDCall['PriceSTD'])})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSCallPrice', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCCallPrice', color='Green', ax=ax)
    pdResults.plot.line(x='StockPrice', y='minusSTD', color='Orange', ax=ax)
    pdResults.plot.line(x='StockPrice', y='plusSTD', color='Orange', ax=ax)
    plot.show(block=True)

    # Compare the European Put Option Price
    npOptionPrice = objEuroPut.getOptionPrice(npStock)

    # Build a dataframe with the results
    pdResults = pd.DataFrame({
        'StockPrice': npStock,
        'BSPutPrice': npOptionPrice,
        'MCPutPrice': pdResultsPut['Price'],
        'minusSTD': (pdResultsPut['Price'] - pdResultsSTDPut['PriceSTD']),
        'plusSTD': (pdResultsPut['Price'] + pdResultsSTDPut['PriceSTD'])})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='BSPutPrice', color='Blue')
    pdResults.plot.line(x='StockPrice', y='MCPutPrice', color='Green', ax=ax)
    pdResults.plot.line(x='StockPrice', y='minusSTD', color='Orange', ax=ax)
    pdResults.plot.line(x='StockPrice', y='plusSTD', color='Orange', ax=ax)
    plot.show(block=True)


def tryThreadingMonteCarloThreadOption(npStock, fltStrike):
    # Within this function I am going to create a package containing 2 monte
    # carlo options.   I will then calculate them syncronosly and record
    # the time and then using threading and record the time.   A problem
    # occurs when I try to re-start a thread.

    print("\n------- tryThreadingMonteCarloThreadOption --------\n")

    # Set data to price the option
    fltVol = 0.2
    fltRiskFreeRate = 0.01
    fltTimeToMaturity = 1
    intNoIter = 200000

    # Build the Options
    objMonteCall = analytics.EuropeanOptionThread. \
        BasicMonteCarloOptionThreaded(
            ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            True,
            intNoIter,
            name="MyCallOption")

    objMontePut = analytics.EuropeanOptionThread. \
        BasicMonteCarloOptionThreaded(
            ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
            fltStrike,
            fltVol,
            fltRiskFreeRate,
            fltTimeToMaturity,
            False,
            intNoIter,
            name="MyPutOption")

    # Create a basic monte carlo package and put the option in
    objPackage = analytics.EuropeanOptionThread. \
        PackageForThreading(1, "Package1")
    objPackage.addOption(objMonteCall)
    objPackage.addOption(objMontePut)
    start = time.time()
    pdPackageResults = objPackage.calculateSyncronousResults(npStock)[0]
    end = time.time()
    print("Number of Iterations: " + str(intNoIter))
    print("\nFull Package Calculation Time (without threading):")
    print(end - start)

    # Now try it threaded

    # Start the Threads
    objPackage.start()
    start = time.time()
    # calculate the results
    pdThreadResults = objPackage.retrieveThreadedResults(npStock)
    # record the calculation time.
    end = time.time()
    # End the threads
    objPackage.join()
    print("Threaded Package Calculation Time:")
    print(end - start)
    print("\n\n")

    # Build a dataframe with the results
    pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'SyncPrice': pdPackageResults['Price'],
            'ThreadPrice': pdThreadResults['Price']})
    # Plot the results.
    ax = pdResults.plot.line(x='StockPrice', y='SyncPrice', color='Blue')
    pdResults.plot.line(x='StockPrice', y='ThreadPrice', color='Green', ax=ax)
    plot.show(block=True)


if __name__ == "__main__":

    print("\n**************************************************************\n")
    print("**********************  START *********************************\n")
    print("***************************************************************\n")

    # Set data to price the option
    fltStrike = 50

    # First build a set of stock prices that go from 50% of the strike
    # price to 150% of the strike price
    # First build a set of stock prices that go from 50% of the strike price
    # to 150% of the strike price
    npStock = np.empty(100)
    for i in range(0, 100):
        npStock[i] = (i + 50) * fltStrike / 100

    pdStock = pd.Series(npStock, name='StockPrice')

    # Compare EuropeanOptionThread_1 to the standard EuropeanOption
    compareEuropeanOptionToMonteCarloThreadOption(npStock, fltStrike)

    # Test out threading using queue's
    tryThreadingMonteCarloThreadOption(npStock, fltStrike)
