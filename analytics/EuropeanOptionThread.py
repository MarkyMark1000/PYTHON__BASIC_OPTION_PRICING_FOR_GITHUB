import numpy as np
import pandas as pd
import scipy.stats as si
import threading
import queue
import matplotlib.pyplot as plot

'''
Within this section, I wanted to explore two things:
i) Having one input which indicates if the model should calculate
the price, delta, gamma etc all at one time.

This means that the calculation uses
ie ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho")
rather than
getOptionPrice(npStock), getOptionDelta(npStock) etc.

In addition to this I wanted to explore using threads to see if it
can improve calculation time.   A package class has been created
where more than one monte carlo object can be added.   In addition
to this a Monte Carlo Option for threading has been created which
uses the calculation method mentioned previously.
'''


class PackageForThreading():

    # Private Functions
    def __init__(self, intPackageID, strPackageName):
        self.__intPackageID = intPackageID
        self.__strPackageName = strPackageName
        self.__lstOptions = list()

    # Public Functions
    def addOption(self, objOption):
        self.__lstOptions.append(objOption)

    def start(self):
        # This is a play on the start of threading.   In the package, I am
        # going to scan through each of the options and run start.
        for obj in self.__lstOptions:
            obj.start()

    def calculateSyncronousResults(self, npStockPrice):
        # Build a dataframe for the results
        pdResults = pd.DataFrame()
        pdSTDResults = pd.DataFrame()
        # Scan through the options calculating the results.
        for opt in self.__lstOptions:
            (pdOptRes, pdOptSTDRes) = opt.calculateOption(npStockPrice)
            # Add the columns to the pdResults dataframe
            cols = list(pdOptRes.columns.values)
            for col in cols:
                if col in pdResults.columns:
                    pdResults[col] += pdOptRes[col]
                else:
                    pdResults[col] = pdOptRes[col]
            # Add the STD columns to the pdSTDResults dataframe
            cols = list(pdOptSTDRes.columns.values)
            for col in cols:
                if col in pdSTDResults.columns:
                    # Combining standard deviation results for multiple
                    # options is meaningless
                    pdSTDResults[col] = np.empty(len(npStockPrice))
                else:
                    pdSTDResults[col] = pdOptSTDRes[col]
        return (pdResults, pdSTDResults)

    def retrieveThreadedResults(self, npStockPrice):
        # Scan through the options and add the stock price to the queue.
        for obj in self.__lstOptions:
            obj.m_q_Stock.put(npStockPrice)
        # Build a pandas dataframe for the calculation results that we
        # return from this function.
        pdReturn = pd.DataFrame()
        pdSTDReturn = pd.DataFrame()
        # Scan through the options and get the results.   Then add them to
        # the dataframe that we are going to return from this function.
        for obj in self.__lstOptions:
            (pdRes, pdSTD) = obj.m_q_Results.get()
            # Get the pdRes to pdReturn dataframe
            cols = list(pdRes.columns.values)
            for col in cols:
                if col in pdReturn.columns:
                    pdReturn[col] += pdRes[col]
                else:
                    pdReturn[col] = pdRes[col]
            # Add the pdSTD columns to the pdSTDReturn dataframe
            cols = list(pdSTD.columns.values)
            for col in cols:
                if col in pdSTDReturn.columns:
                    # Combining standard deviation results for multiple
                    # options is meaningless
                    pdSTDReturn[col] = np.empty(len(npStockPrice))
                else:
                    pdSTDReturn[col] = pdSTD[col]
        return (pdReturn, pdSTDReturn)

    def join(self):
        # Again this is a play on the join of threading.   In the package, I am
        # going to scan through each of the options and run join, ie wait until
        # the package has calculated.
        for obj in self.__lstOptions:
            obj.join()


class BasicMonteCarloOptionThreaded(threading.Thread):

    # Private Functions

    def __init__(self, tpCalcRequirements, fltStrike, fltVol, fltRiskFreeRate,
                 fltTimeToMaturity, boolIsCall, intNoIter, group=None,
                 target=None, name=None, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        # Core option data
        self.__fltStrike = fltStrike
        self.__fltVol = fltVol
        self.__fltRiskFreeRate = fltRiskFreeRate
        self.__fltTimeToMaturity = fltTimeToMaturity
        self.__boolIsCall = boolIsCall
        self.__intNoIter = intNoIter
        self.__tpCalcRequirements = tpCalcRequirements
        # Input Queue of stock prices
        self.m_q_Stock = queue.Queue()
        # Output Queue for calculation results.
        self.m_q_Results = queue.Queue()
        self.stoprequest = threading.Event()

    def __str__(self):
        strF = 'BasicMonteCarloOptionThreaded: [Strike:{strike}; Vol:{vol}; ' \
               'RFRate:{rfrate}; Time:{time}; IsCall:{iscall}; ' \
               'NoIter:{noiter}]'
        return strF.format(strike=self.__fltStrike, vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=self.__boolIsCall,
                           noiter=self.__intNoIter)

    def __buildPayoffMatrixPVd(self, npStock, npMultiplier, fltPV):

        # Get the Final Stock Price
        npFinalStockPrice = np.matmul(npStock, npMultiplier)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = npFinalStockPrice - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - npFinalStockPrice

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)

        # Return the present value of the monte carlo simulations
        return npPayoffAdj * fltPV

    def __addDeltaCalculation(self, pdResults, pdSTDResults, npStockPrice,
                              Mult_PDG, fltPV, npPayoffPVd):

        # Calculate payoff when stock price bumped by 1%
        npPayoffPVd_BUp = self.__buildPayoffMatrixPVd(
            (npStockPrice * 1.01),
            Mult_PDG,
            fltPV)

        # Calculate the delta for each random walk
        npResults = (npPayoffPVd_BUp - npPayoffPVd) / (npStockPrice * 0.01)

        # Calculate the mean and standard deviation
        npForResults = np.mean(npResults, axis=1)
        npSTDForResults = np.std(npResults, axis=1)

        # Add Delta and its standard deviation to the results.
        pdResults['Delta'] = npForResults
        pdSTDResults['DeltaSTD'] = npSTDForResults

    def __addGammaCalculation(self, pdResults, pdSTDResults, npStockPrice,
                              Mult_PDG, fltPV, npPayoffPVd):
        # Note the gamma may become unstable, see the following:
        # https://quant.stackexchange.com/questions/18208/
        # greeks-why-does-my-monte-carlo-give-correct-delta-but-incorrect-gamma

        # Calculate the payoff when the stock price is bumped
        # up and down by 1%
        npPayoffPVd_BUp = self.__buildPayoffMatrixPVd(
            (npStockPrice * 1.01),
            Mult_PDG,
            fltPV)
        npPayoffPVd_BDown = self.__buildPayoffMatrixPVd(
            (npStockPrice * 0.99),
            Mult_PDG,
            fltPV)

        # Calculate the numerator and denominator in the Gamma calc
        n1 = (npPayoffPVd_BUp - (2 * npPayoffPVd) + npPayoffPVd_BDown)
        d1 = ((npStockPrice * 0.01) * (npStockPrice * 0.01))

        # Get the gamma calc for each path
        npResults = n1/d1

        # Calculate the mean and standard deviation
        npForResults = np.mean(npResults, axis=1)
        npSTDForResults = np.std(npResults, axis=1)

        # Add Gamma and its std to the results.
        pdResults['Gamma'] = npForResults
        pdSTDResults['GammaSTD'] = npSTDForResults

    def __addVegaCalculation(self, pdResults, pdSTDResults, npStockPrice, Z,
                             Mult_PDG, fltPV, npPayoffPVd):
        # Bump the vol by fltVegaBumpSize to get the vega, then divide by
        # fltVegaBumpSize, but times by 0.01 to get it in terms of a 0.01
        # bump.

        fltVegaBumpSize = 0.0001
        fltVolBumped = self.__fltVol + fltVegaBumpSize

        # Calculate the multipliers for vega random walk
        a1 = Z * fltVolBumped * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate
              - 0.5 * fltVolBumped ** 2) * self.__fltTimeToMaturity
        Mult_Vega = np.exp(a1 + a2)

        # Get the payoff of the vega simulation
        npPayoffPVd_Vega = self.__buildPayoffMatrixPVd(
                    npStockPrice,
                    Mult_Vega,
                    fltPV)

        # Calculate the differential
        npResults = (npPayoffPVd_Vega - npPayoffPVd) \
            * (0.01 / fltVegaBumpSize)

        # Calculate the mean and std dev
        npForResults = np.mean(npResults, axis=1)
        npSTDForResults = np.std(npResults, axis=1)

        # Add vega to the results
        pdResults['Vega'] = npForResults
        pdSTDResults['VegaSTD'] = npSTDForResults

    def __addThetaCalculation(self, pdResults, pdSTDResults, npStockPrice, Z,
                              Mult_PDG, fltPV, npPayoffPVd):
        # Bump the time by fltThetaBumpSize to get the theta, then divide
        # by fltThetaBumpSize, but times by 1/365 to get it in terms of a
        # 1 day move

        fltThetaBumpSize = 1 / 365
        fltTimeBumped = self.__fltTimeToMaturity - fltThetaBumpSize
        fltPVTimeBumped = np.exp(-self.__fltRiskFreeRate * fltTimeBumped)

        # Calculate the multipliers for theta random walk
        a1 = Z * self.__fltVol * np.sqrt(fltTimeBumped)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * fltTimeBumped
        Mult_Theta = np.exp(a1 + a2)

        # Get the payoff of the theta simulation
        npPayoffPVd_Theta = self.__buildPayoffMatrixPVd(
                                    npStockPrice,
                                    Mult_Theta,
                                    fltPVTimeBumped)

        # Calculate the differential
        npResults = (npPayoffPVd_Theta - npPayoffPVd)

        # Calculate the mean and std dev
        npForResults = np.mean(npResults, axis=1)
        npSTDForResults = np.std(npResults, axis=1)

        # Add theta to the results
        pdResults['Theta'] = npForResults
        pdSTDResults['ThetaSTD'] = npSTDForResults

    def __addRhoCalculation(self, pdResults, pdSTDResults, npStockPrice, Z,
                            Mult_PDG, fltPV, npPayoffPVd):
        # Bump the rate by fltRhoBumpSize to get the rho, then divide by
        # fltRhoBumpSize, but times by 0.01 to get it in terms of a 0.01
        # dmove

        fltRhoBumpSize = 0.0001
        fltRiskFreeRateBumped = self.__fltRiskFreeRate + fltRhoBumpSize
        fltPVRiskFreeRateBumped = np.exp(
            -fltRiskFreeRateBumped * self.__fltTimeToMaturity)

        # Calculate the multipliers for rho random walk
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (fltRiskFreeRateBumped
              - 0.5 * self.__fltVol ** 2) * self.__fltTimeToMaturity
        Mult_Rho = np.exp(a1 + a2)

        # Get the payoff of the theta simulation
        npPayoffPVd_Rho = self.__buildPayoffMatrixPVd(
                                                    npStockPrice,
                                                    Mult_Rho,
                                                    fltPVRiskFreeRateBumped
                                                    )

        # Calculate the differential
        a1 = (npPayoffPVd_Rho - npPayoffPVd)
        a2 = (0.01 / fltRhoBumpSize)
        npResults = a1 * a2

        # Calculate the mean and std dev
        npForResults = np.mean(npResults, axis=1)
        npSTDForResults = np.std(npResults, axis=1)

        # Add rho to the results
        pdResults['Rho'] = npForResults
        pdSTDResults['RhoSTD'] = npSTDForResults

    def __calculateOptionNew(self, npStock):

        # Resize the npStock numpy array so that it is an (? x 1) matrix
        # which is used extensively in the calculations.
        npStockPrice = npStock.copy()
        npStockPrice = np.reshape(npStockPrice, (len(npStock), -1))

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        # Now get the multipliers for price, delta and gamma should we
        # need them
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        Mult_PDG = np.exp(a1 + a2)

        # Now calculate the present value multiplier.
        fltPV = np.exp(-self.__fltRiskFreeRate * self.__fltTimeToMaturity)

        # Get the payoff of the option with no bumps and normal present
        # value calculation.
        npPayoffPVd = self.__buildPayoffMatrixPVd(
            npStockPrice,
            Mult_PDG,
            fltPV)

        # Add this to the result's
        npForResults = np.mean(npPayoffPVd, axis=1)
        npSTDForResults = np.std(npPayoffPVd, axis=1)
        pdResults = pd.DataFrame({'Price': npForResults})
        pdSTDResults = pd.DataFrame({'PriceSTD': npSTDForResults})

        # Now potentially add the delta
        if "Delta" in self.__tpCalcRequirements:
            self.__addDeltaCalculation(pdResults, pdSTDResults, npStockPrice,
                                       Mult_PDG, fltPV, npPayoffPVd)

        # Now potentially add the gamma
        if "Gamma" in self.__tpCalcRequirements:
            self.__addGammaCalculation(pdResults, pdSTDResults, npStockPrice,
                                       Mult_PDG, fltPV, npPayoffPVd)

        # Now potentially add the vega
        if "Vega" in self.__tpCalcRequirements:
            self.__addVegaCalculation(pdResults, pdSTDResults, npStockPrice,
                                      Z, Mult_PDG, fltPV, npPayoffPVd)

        # Now potentially add the theta
        if "Theta" in self.__tpCalcRequirements:
            self.__addThetaCalculation(pdResults, pdSTDResults, npStockPrice,
                                       Z, Mult_PDG, fltPV, npPayoffPVd)

        # Now potentially add the rho
        if "Rho" in self.__tpCalcRequirements:
            self.__addRhoCalculation(pdResults, pdSTDResults, npStockPrice,
                                     Z, Mult_PDG, fltPV, npPayoffPVd)

        # now return the results
        return (pdResults, pdSTDResults)

    # Public Functions
    def run(self):
        while not self.stoprequest.isSet():
            try:
                # Attempt to get the stock price
                npStockPrice = self.m_q_Stock.get(True, 1)
                # Attept to calculate the results, but price/delta etc only,
                # no stddev hence the use of [0]
                (pdResults, pdResultsSTD) = self.calculateOption(npStockPrice)
                # Attempt to push the results back out of to the results queue
                self.m_q_Results.put((pdResults, pdResultsSTD))
            except queue.Empty:
                continue

    def join(self, timeout=None):
        # Request the thread to stop and then wait.
        self.stoprequest.set()
        super(BasicMonteCarloOptionThreaded, self).join(timeout)

    def calculateOption(self, npStockPrice):
        # This should return a tuple containing the results and
        # the std dev of the monte carlo calc's.
        return self.__calculateOptionNew(npStockPrice)
