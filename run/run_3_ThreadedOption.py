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

'''
I wanted to explore what would happen if you calculated monte carlo prices
using threading.   This section creates a packaage of two options, a call
and a put which effectively makes a straddle.   The price and greeks are
then calculated syncronously and the calculation time recorded.   The
package then calculates the greeks by running a thread for each option and
the calculation time is ecorded.
Finally a graph showing the Price of the package calculated syncronously
and using Threads is displayed to ensure the prices are consistent.

I ran it using 20k iterations, 200k iterations and 500k iterations and
found the following:

 No Iter             Sync Calc Time              Thread Calc Time
  20,000             0.6053640842437744          2.4003419876098633
 200,000             9.774694919586182           8.075640201568604
 500,000             24.9134361743927            20.241413831710815

It appears to offer some benefit when doing long calculations, but not when
the number of iterations is small.

The threading is based upon the following example:

https://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping

'''


def testThreadingMonteCarloThreadOption(npStock, fltStrike, fltVol,
                                        fltRiskFreeRate, fltTimeToMaturity,
                                        intNoIter):

    '''
    Within this function I am going to create a package containing 2 monte
    carlo options.   I will then calculate them syncronosly and record
    the time and then using threading and record the time.

    The package will contain a call and put with the same basic characteristics
    (strike etc), ie a straddle
    '''

    # Build the Call Option
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

    # Create a basic monte carlo package
    objPackage = analytics.EuropeanOptionThread. \
        PackageForThreading(1, "Package1")

    # Put the call and put into the package
    objPackage.addOption(objMonteCall)
    objPackage.addOption(objMontePut)

    # Calculate the results of the calculation syncronously and record
    # how long it takes to run
    start = time.time()
    pdPackageResults = objPackage.calculateSyncronousResults(npStock)[0]
    end = time.time()

    print("\nStraddle Syncronous Calculation Time (ie without threading):")
    print(end - start)

    # Now try it threaded

    # Calculate the results of the calculation using threading and
    # record how long it takes to run

    # Start the cald
    start = time.time()
    objPackage.start()

    # calculate the results
    pdThreadResults = objPackage. \
        retrieveThreadedResults(npStock)[0]

    # End the calc and record the time
    objPackage.join()
    # record the calculation time.
    end = time.time()

    print("\nStraddle Threaded Package Calculation Time (ie with threading):")
    print(end - start)
    print("\n\n")

    # Now build a dataframe to compare the syncronous results with the threaded
    # results to ensure that they are similar.
    pdResults = pd.DataFrame({
            'StockPrice': npStock,
            'SyncPrice': pdPackageResults['Price'],
            'ThreadPrice': pdThreadResults['Price']})

    print("\nPlot Syncronous vs Threaded price to ensure they are similar:")

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
    npStock = np.empty(100)
    for i in range(0, 100):
        npStock[i] = (i + 50) * fltStrike / 100

    # Create a straddle (package with call and put), then calculate the results
    # syncronously and asyncronously.
    testThreadingMonteCarloThreadOption(npStock=npStock, fltStrike=fltStrike,
                                        fltVol=0.2, fltRiskFreeRate=0.01,
                                        fltTimeToMaturity=1, intNoIter=200000)
