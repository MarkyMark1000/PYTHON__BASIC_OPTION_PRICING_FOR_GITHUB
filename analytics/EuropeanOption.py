import numpy as np
import pandas as pd
import scipy.stats as si

'''
This section is highly dependent upon knowledge of the black & scholes formula
for option pricing and using Monte Carlo methods to price options.   There are
a number of terms such as d1, d2, delta, gamma, vega that are specific to
option ricing and I will not add comments to explain what these are.   If you
are unfamiliar with this, read something like 'Options, Futures and Other
Derivatives' by John Hull.

Note however that I use numpy arrays here, so when a calculation is performed,
I am often calculating multiple values at the same time.   I assume an input
array containing multiple stock prices is passed in, which results n multiple
price, delta, gamma etx values being calculated and which will later be used
to plot graphs.

This module has two classes:

BlackScholes:
This calculates the price, delta, gamma etc of an option using the B&S Formula

BasicMonteCarloOption:
This calculates the price, delta, gamma etc by using monte carlo methods.
With this class I tend to return 2 argument (not 1) from the functions.
The second argument tends to be the standard deviation. So I may have
(optPrice, optStdDev) = calculateSomeValue( numpyArrayOfStockPrices )

This section is only for European Options and it does not include things such
as interest rate curves, borrow curves, volatility surface etc etc.
(ie it is a simplified version)

'''


class BlackScholes():

    # Private Functions

    def __init__(self, fltStrike, fltVol, fltRiskFreeRate, fltTimeToMaturity,
                 boolIsCall):
        # Set the variables
        self.__fltStrike = fltStrike
        self.__fltVol = fltVol
        self.__fltRiskFreeRate = fltRiskFreeRate
        self.__fltTimeToMaturity = fltTimeToMaturity
        self.__boolIsCall = boolIsCall

    def __str__(self):
        strF = 'EuropeanOption: [Strike:{strike}; Vol:{vol}; '\
                'RFRate:{rfrate}; Time:{time}; IsCall:{iscall};]'
        return strF.format(strike=self.__fltStrike,
                           vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=self.__boolIsCall)

    def __getD1(self, npStock):
        npSK = np.log(npStock / self.__fltStrike)
        npTopD1 = npSK + (
                          self.__fltRiskFreeRate
                          + (self.__fltVol ** 2) / 2
                          ) * self.__fltTimeToMaturity
        npD1 = npTopD1 / (self.__fltVol * np.sqrt(self.__fltTimeToMaturity))
        return npD1

    def __getD2(self, npStock):
        npD1 = self.__getD1(npStock)
        npD2 = npD1 - (self.__fltVol * np.sqrt(self.__fltTimeToMaturity))
        return npD2

    def __getD2FromD1(self, npD1):
        npD2 = npD1 - (self.__fltVol * np.sqrt(self.__fltTimeToMaturity))
        return npD2

    def __getCallPrice(self, npStock):
        npD1 = self.__getD1(npStock)
        npD2 = self.__getD2FromD1(npD1)
        npCall = npStock * si.norm.cdf(npD1)\
            - (self.__fltStrike
               * np.exp(-self.__fltRiskFreeRate * self.__fltTimeToMaturity)
               * si.norm.cdf(npD2))
        return npCall

    def __getCallDelta(self, npStock):
        npD1 = self.__getD1(npStock)
        npDelta = si.norm.cdf(npD1)
        return npDelta

    def __getCallTheta(self, npStock):
        npD1 = self.__getD1(npStock)
        npD2 = self.__getD2FromD1(npD1)
        npArg1 = -(npStock * si.norm.pdf(npD1) * self.__fltVol) \
            / (2 * np.sqrt(self.__fltTimeToMaturity))
        npArg2 = -self.__fltRiskFreeRate * self.__fltStrike * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity) \
            * si.norm.cdf(npD2)
        npTheta = (npArg1 + npArg2) / 365
        return npTheta

    def __getCallRho(self, npStock):
        npD2 = self.__getD2(npStock)
        npRho = (self.__fltStrike * self.__fltTimeToMaturity * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
            * si.norm.cdf(npD2)) * 0.01
        return npRho

    def __getPutPrice(self, npStock):
        npD1 = self.__getD1(npStock)
        npD2 = self.__getD2FromD1(npD1)
        npPut = self.__fltStrike * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity) \
            * si.norm.cdf(-npD2) - npStock * si.norm.cdf(-npD1)
        return npPut

    def __getPutDelta(self, npStock):
        npD1 = self.__getD1(npStock)
        npDelta = (si.norm.cdf(npD1) - 1)
        return npDelta

    def __getPutTheta(self, npStock):
        npD1 = self.__getD1(npStock)
        npD2 = self.__getD2FromD1(npD1)
        npArg1 = -(npStock * si.norm.pdf(npD1) * self.__fltVol) \
            / (2 * np.sqrt(self.__fltTimeToMaturity))
        npArg2 = self.__fltRiskFreeRate * self.__fltStrike * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity) \
            * si.norm.cdf(-npD2)
        npTheta = (npArg1 + npArg2) / 365
        return npTheta

    def __getPutRho(self, npStock):
        npD2 = self.__getD2(npStock)
        npRho = (- self.__fltStrike * self.__fltTimeToMaturity * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
            * si.norm.cdf(-npD2)) * 0.01
        return npRho

    # Public Functions

    def getOptionPrice(self, npStock):
        if self.__boolIsCall:
            return self.__getCallPrice(npStock)
        else:
            return self.__getPutPrice(npStock)

    def getOptionDelta(self, npStock):
        if self.__boolIsCall:
            return self.__getCallDelta(npStock)
        else:
            return self.__getPutDelta(npStock)

    def getOptionGamma(self, npStock):
        # Gamma is Call/Put independent
        npD1 = self.__getD1(npStock)
        n1 = (si.norm.pdf(npD1))
        d1 = (npStock * self.__fltVol * np.sqrt(self.__fltTimeToMaturity))
        npGamma = n1 / d1
        return npGamma

    def getOptionVega(self, npStock):
        # Vega is Call/Put independent
        npD1 = self.__getD1(npStock)
        npVega = npStock * (si.norm.pdf(npD1)) \
            * np.sqrt(self.__fltTimeToMaturity) / 100
        return npVega

    def getOptionTheta(self, npStock):
        if self.__boolIsCall:
            return self.__getCallTheta(npStock)
        else:
            return self.__getPutTheta(npStock)

    def getOptionRho(self, npStock):
        if self.__boolIsCall:
            return self.__getCallRho(npStock)
        else:
            return self.__getPutRho(npStock)


class BasicMonteCarloOption():

    # Private Functions

    def __init__(self, fltStrike, fltVol, fltRiskFreeRate, fltTimeToMaturity,
                 boolIsCall, intNoIter):
        self.__fltStrike = fltStrike
        self.__fltVol = fltVol
        self.__fltRiskFreeRate = fltRiskFreeRate
        self.__fltTimeToMaturity = fltTimeToMaturity
        self.__boolIsCall = boolIsCall
        self.__intNoIter = intNoIter

    def __str__(self):
        strF = 'BasicMonteCarloOption: [Strike:{strike}; Vol:{vol}; ' \
               'RFRate:{rfrate}; Time:{time}; IsCall:{iscall}; ' \
               'NoIter:{noiter}]'
        return strF.format(strike=self.__fltStrike, vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=self.__boolIsCall,
                           noiter=self.__intNoIter)

    def getOptionPrice(self, npStock):

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        # Now get the multipliers to find the final stock price
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        Mult = np.exp(a1 + a2)

        # For every stock price, get m_intNoIter final stock prices by doing
        # a matrix multiplication.   We multiply the initial stock price,by
        # the multipliers to get the final stock price.   I do need to change
        # the stocks to a matrix to achive this.
        npMatrix = npStock.copy()
        npMatrix = np.reshape(npMatrix, (len(npStock), -1))
        FinalS = np.matmul(npMatrix, Mult)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = FinalS - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - FinalS

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)

        # Get the present value of the monte carlo simulations
        npPV = npPayoffAdj * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)

        # Calculate the mean for each axis.
        npPrice = np.mean(npPV, axis=1)

        # Calculate the stdev for each axis.
        npSTD = np.std(npPV, axis=1)

        # Return the option price.
        return (npPrice, npSTD)

    def getOptionDelta(self, npStock):

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        # Now get the multipliers to find the final stock price
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        Mult = np.exp(a1 + a2)

        # For every stock price, get m_intNoIter final stock prices by doing
        # a matrix multiplication.   We multiply the initial stock price,by
        # the multipliers to get the final stock price.   I do need to change
        # the stocks to a matrix to achive this.
        npMatrix = npStock.copy()
        npMatrix = np.reshape(npMatrix, (len(npStock), -1))
        FinalS = np.matmul(npMatrix, Mult)

        # Get a bumped stockprice and then calculate the final stockprice
        npBump = npMatrix * 0.01
        FinalSBump = np.matmul(npMatrix + npBump, Mult)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = FinalS - self.__fltStrike
            npPayoffBump = FinalSBump - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - FinalS
            npPayoffBump = self.__fltStrike - FinalSBump

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)
        npPayoffAdjBump = np.maximum(npPayoffBump, npZeros)

        # Get the present value of the monte carlo simulations
        npPV = npPayoffAdj * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
        npPVBump = npPayoffAdjBump * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)

        # Calculate the delta
        npAllDelta = (npPVBump - npPV) / npBump

        # Calculate the mean for each axis.
        npDelta = np.mean(npAllDelta, axis=1)

        # Calculate the stdev for each axis.
        npDeltaSTD = np.std(npAllDelta, axis=1)

        # Return the option price.
        return (npDelta, npDeltaSTD)

    def getOptionRho(self, npStock):

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        fltBump = 0.0001
        fltRiskFreeRateBump = self.__fltRiskFreeRate + fltBump

        # Now get the multipliers to find the final stock price
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        Mult = np.exp(a1 + a2)
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (fltRiskFreeRateBump - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        MultBump = np.exp(a1 + a2)

        # For every stock price, get m_intNoIter final stock prices by
        # doing a matrix multiplication.   We multiply the initial stock
        # price,by the transpose of the multipliers to get the final stock
        # price
        npMatrix = npStock.copy()
        npMatrix = np.reshape(npMatrix, (len(npStock), -1))
        FinalS = np.matmul(npMatrix, Mult)

        # Get a bumped stockprice and then calculate the final stockprice
        FinalSBump = np.matmul(npMatrix, MultBump)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = FinalS - self.__fltStrike
            npPayoffBump = FinalSBump - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - FinalS
            npPayoffBump = self.__fltStrike - FinalSBump

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)
        npPayoffAdjBump = np.maximum(npPayoffBump, npZeros)

        # Get the present value of the monte carlo simulations
        npPV = npPayoffAdj * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
        npPVBump = npPayoffAdjBump * np.exp(
            -fltRiskFreeRateBump * self.__fltTimeToMaturity)

        # Calculate the delta
        npAllRho = (npPVBump - npPV) * (0.01 / fltBump)

        # Calculate the mean for each axis.
        npRho = np.mean(npAllRho, axis=1)

        # Calculate the stdev for each axis.
        npRhoSTD = np.std(npAllRho, axis=1)

        # Return the option price.
        return (npRho, npRhoSTD)

    def getOptionGamma(self, npStock):
        # Note the gamma may become unstable, see the following:
        # https://quant.stackexchange.com/questions/18208/
        # greeks-why-does-my-monte-carlo-give-correct-delta-but-incorrect-gamma

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        # Now get the multipliers to find the final stock price
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        Mult = np.exp(a1 + a2)

        # For every stock price, get m_intNoIter final stock prices by
        # doing a matrix multiplication.   We multiply the initial stock
        # price,by the transpose of the multipliers to get the final stock
        # price
        npMatrix = npStock.copy()
        npMatrix = np.reshape(npMatrix, (len(npStock), -1))
        FinalS = np.matmul(npMatrix, Mult)

        # Get a bumped stockprice and then calculate the final stockprice
        npBump = npMatrix * 0.01
        FinalSBumpPlus = np.matmul((npMatrix + npBump), Mult)
        FinalSBumpMinus = np.matmul((npMatrix - npBump), Mult)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = FinalS - self.__fltStrike
            npPayoffBumpPlus = FinalSBumpPlus - self.__fltStrike
            npPayoffBumpMinus = FinalSBumpMinus - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - FinalS
            npPayoffBumpPlus = self.__fltStrike - FinalSBumpPlus
            npPayoffBumpMinus = self.__fltStrike - FinalSBumpMinus

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)
        npPayoffAdjBumpPlus = np.maximum(npPayoffBumpPlus, npZeros)
        npPayoffAdjBumpMinus = np.maximum(npPayoffBumpMinus, npZeros)

        # Get the present value of the monte carlo simulations
        npPV = npPayoffAdj * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
        npPVBumpPlus = npPayoffAdjBumpPlus * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
        npPVBumpMinus = npPayoffAdjBumpMinus * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)

        # Calculate the numerator and denominator
        n1 = (npPVBumpPlus - (2 * npPV) + npPVBumpMinus)
        d1 = (npBump * npBump)

        # Calculate the delta
        npAllGamma = n1 / d1

        # Calculate the mean for each axis.
        npGamma = np.mean(npAllGamma, axis=1)

        # Calculate the stdev for each axis.
        npGammaSTD = np.std(npAllGamma, axis=1)

        # Return the option price.
        return (npGamma, npGammaSTD)

    def getOptionVega(self, npStock):

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        # Now get the multipliers to find the final stock price
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * (self.__fltVol ** 2)) \
            * self.__fltTimeToMaturity
        Mult = np.exp(a1 + a2)
        fltBump = 0.0001
        volBump = self.__fltVol + fltBump
        a1 = Z * volBump * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * (volBump ** 2)) \
            * self.__fltTimeToMaturity
        MultBump = np.exp(a1 + a2)

        # For every stock price, get m_intNoIter final stock prices by doing
        # a matrix multiplication.   We multiply the initial stock price,by
        # the transpose of the multipliers to get the final stock price
        npMatrix = npStock.copy()
        npMatrix = np.reshape(npMatrix, (len(npStock), -1))
        FinalS = np.matmul(npMatrix, Mult)

        # Get a bumped stockprice and then calculate the final stockprice
        FinalSBump = np.matmul(npMatrix, MultBump)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = FinalS - self.__fltStrike
            npPayoffBump = FinalSBump - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - FinalS
            npPayoffBump = self.__fltStrike - FinalSBump

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)
        npPayoffAdjBump = np.maximum(npPayoffBump, npZeros)

        # Get the present value of the monte carlo simulations
        npPV = npPayoffAdj * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)
        npPVBump = npPayoffAdjBump * np.exp(
            -self.__fltRiskFreeRate * self.__fltTimeToMaturity)

        # Calculate the vega
        npAllVega = (npPVBump - npPV) * (0.01 / fltBump)

        # Calculate the mean for each axis.
        npVega = np.mean(npAllVega, axis=1)

        # Calculate the stdev for each axis.
        npVegaSTD = np.std(npAllVega, axis=1)

        # Return the option price.
        return (npVega, npVegaSTD)

    def getOptionTheta(self, npStock):

        # Get the random numbers
        Z = np.random.standard_normal((1, self.__intNoIter))

        # Get bumped time to maturity
        fltDBump = 1 / 365
        fltTimeBump = self.__fltTimeToMaturity - fltDBump

        # Now get the multipliers to find the final stock price
        a1 = Z * self.__fltVol * np.sqrt(self.__fltTimeToMaturity)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) \
            * self.__fltTimeToMaturity
        Mult = np.exp(a1 + a2)
        a1 = Z * self.__fltVol * np.sqrt(fltTimeBump)
        a2 = (self.__fltRiskFreeRate - 0.5 * self.__fltVol ** 2) * fltTimeBump
        MultBump = np.exp(a1 + a2)

        # For every stock price, get m_intNoIter final stock prices by
        # doing a matrix multiplication.   We multiply the initial stock
        # price,by the transpose of the multipliers to get the final stock
        # price
        npMatrix = npStock.copy()
        npMatrix = np.reshape(npMatrix, (len(npStock), -1))
        FinalS = np.matmul(npMatrix, Mult)

        # Get a bumped stockprice and then calculate the final stockprice
        FinalSBump = np.matmul(npMatrix, MultBump)

        # Calculate the payoff
        if self.__boolIsCall:
            npPayoff = FinalS - self.__fltStrike
            npPayoffBump = FinalSBump - self.__fltStrike
        else:
            npPayoff = self.__fltStrike - FinalS
            npPayoffBump = self.__fltStrike - FinalSBump

        # Build a matrix of zero's the same size as the payoff matrix.
        npZeros = np.zeros(npPayoff.shape)

        # Build a matrix of adjusted payoff, where the P&L if floored at zero.
        npPayoffAdj = np.maximum(npPayoff, npZeros)
        npPayoffAdjBump = np.maximum(npPayoffBump, npZeros)

        # Get the present value of the monte carlo simulations
        npPV = npPayoffAdj * np.exp(
                        - self.__fltRiskFreeRate * self.__fltTimeToMaturity)
        npPVBump = npPayoffAdjBump * np.exp(
                        - self.__fltRiskFreeRate * fltTimeBump)

        # Calculate the Theta
        npAllTheta = (npPVBump - npPV)

        # Calculate the mean for each axis.
        npTheta = np.mean(npAllTheta, axis=1)

        # Calculate the stdev for each axis.
        npThetaSTD = np.std(npAllTheta, axis=1)

        # Return the option price.
        return (npTheta, npThetaSTD)
