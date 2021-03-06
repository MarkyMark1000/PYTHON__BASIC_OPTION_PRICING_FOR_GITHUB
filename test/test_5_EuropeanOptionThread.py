import analytics.EuropeanOptionBoundaryConditions
import analytics.EuropeanOptionThread
import numpy as np
import unittest
from unittest.mock import patch
import math
import test.ExternalData as ED
from analytics.EuropeanOptionThread import np

'''
These set of tests are used to ensure the BasicMonteCarloOptionThreaded
class is working correctly.
It tests the  __str__ and compares the price and greek calculations against
a set of external data that is stored in the ExternalData.py file.
Because this is a monte carlo calculation, it is very susceptable to
variation in the results, ie it is worth nothing that this is only an
approximate comparison.
I have found that using the data in this file and comparing it to the external
data with an accuracy of 0.1 x StdDev, generally results in a positive test
result. However if the data is changed, especially the number of iterations,
the tests may start to fail.
At a later point, I also generated a list of 200 randomly generated numbers
and built some tests with these random numbers patched into the monte carlo
calculation results.   These tests should produce stable results, but are
not as accurate because only 200 numbers are used.   The results are
compared to an accuracy of 10dp, defined in ExternalData.
'''


class TestBasicMonteCarloOptionThreaded(unittest.TestCase):

    def setUp(self):

        # Set data to price the option
        self.__fltStrike = ED.EO_Strike
        self.__fltVol = ED.EO_Vol
        self.__fltRiskFreeRate = ED.EO_RiskFreeRate
        self.__fltTimeToMaturity = ED.EO_TimeToMaturity
        self.__intNoIterations = 200000

        # Build some stock prices to run the test against
        # self.__npStock = np.empty(100)
        # for i in range(0, 100):
        #    self.__npStock[i] = (i + 50) * self.__fltStrike / 100

        # Add a Threaded Call Option
        self.__objMonteCall = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                self.__intNoIterations,
                name="MyCallOption")

        # Add a Threaded Call Option, BUT WITH FIXED NORMAL DIST VALUES
        self.__objMonteCallFN = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                len(ED.lstNormal),
                name="MyCallOptionFN")

        # Add a Threaded Put Option
        self.__objMontePut = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                False,
                self.__intNoIterations,
                name="MyPutOption")

        # Add a Threaded Put Option, BUT WITH FIXED NORMAL DIST VALUES
        self.__objMontePutFN = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                False,
                len(ED.lstNormal),
                name="MyPutOptionFN")

    def testEuropeanCallStr(self):

        # Evaluate what the call should look like
        strF = 'BasicMonteCarloOptionThreaded: [Strike:{strike}; Vol:{vol}; ' \
               'RFRate:{rfrate}; Time:{time}; IsCall:{iscall}; ' \
               'NoIter:{noiter}]'
        strF = strF.format(strike=self.__fltStrike, vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=True,
                           noiter=self.__intNoIterations)

        # Compare the string option representation
        self.assertEqual(str(self.__objMonteCall), strF)

    def testEuropeanPutStr(self):

        # Evaluate what the put should look like
        strF = 'BasicMonteCarloOptionThreaded: [Strike:{strike}; Vol:{vol}; ' \
               'RFRate:{rfrate}; Time:{time}; IsCall:{iscall}; ' \
               'NoIter:{noiter}]'
        strF = strF.format(strike=self.__fltStrike, vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=False,
                           noiter=self.__intNoIterations)

        # Compare the string option representation
        self.assertEqual(str(self.__objMontePut), strF)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testPricevsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed price and then ensures
        # the result received is consistent.   The price isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testPricevsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (pCP, stdDevC) = self.__objMonteCallFN.calculateOption(npStock)
        (pPP, stdDevP) = self.__objMontePutFN.calculateOption(npStock)

        lstCall = list(pCP['Price'])
        lstPut = list(pPP['Price'])

        lstCall = [abs(lstCall[i]-ED.FN_CALL_PRICE[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_PRICE[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testPricevsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"
        (npCP, stdDevC) = self.__objMonteCall.calculateOption(npStock)
        (npPP, stdDevP) = self.__objMontePut.calculateOption(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Price
            diff = abs(npCP["Price"].values[i] - ED.EO_callPrice[i])
            maxErr = 0.1*stdDevC["PriceSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Put Price
            diff = abs(npPP["Price"].values[i] - ED.EO_putPrice[i])
            maxErr = 0.1*stdDevP["PriceSTD"].values[i]
            self.assertLess(diff, maxErr)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testDeltavsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed delta and then ensures
        # the result received is consistent.   The delta isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testDeltavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (pCP, stdDevC) = self.__objMonteCallFN.calculateOption(npStock)
        (pPP, stdDevP) = self.__objMontePutFN.calculateOption(npStock)

        lstCall = list(pCP['Delta'])
        lstPut = list(pPP['Delta'])

        lstCall = [abs(lstCall[i]-ED.FN_CALL_DELTA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_DELTA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testDeltavsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"
        (npCP, stdDevC) = self.__objMonteCall.calculateOption(npStock)
        (npPP, stdDevP) = self.__objMontePut.calculateOption(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Delta
            diff = abs(npCP["Delta"].values[i] - ED.EO_callDelta[i])
            maxErr = 0.1*stdDevC["DeltaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Put Delta
            diff = abs(npPP["Delta"].values[i] - ED.EO_putDelta[i])
            maxErr = 0.1*stdDevP["DeltaSTD"].values[i]
            self.assertLess(diff, maxErr)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testGammavsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed gamma and then ensures
        # the result received is consistent.   The gamma isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testGammavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (pCP, stdDevC) = self.__objMonteCallFN.calculateOption(npStock)
        (pPP, stdDevP) = self.__objMontePutFN.calculateOption(npStock)

        lstCall = list(pCP['Gamma'])
        lstPut = list(pPP['Gamma'])

        lstCall = [abs(lstCall[i]-ED.FN_CALL_GAMMA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_GAMMA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testGammavsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"
        (npCP, stdDevC) = self.__objMonteCall.calculateOption(npStock)
        (npPP, stdDevP) = self.__objMontePut.calculateOption(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Gamma
            diff = abs(npCP["Gamma"].values[i] - ED.EO_callGamma[i])
            maxErr = 0.1*stdDevC["GammaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Put Gamma
            diff = abs(npPP["Gamma"].values[i] - ED.EO_putGamma[i])
            maxErr = 0.1*stdDevP["GammaSTD"].values[i]
            self.assertLess(diff, maxErr)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testVegavsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed vega and then ensures
        # the result received is consistent.   The vega isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testVegavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (pCP, stdDevC) = self.__objMonteCallFN.calculateOption(npStock)
        (pPP, stdDevP) = self.__objMontePutFN.calculateOption(npStock)

        lstCall = list(pCP['Vega'])
        lstPut = list(pPP['Vega'])

        lstCall = [abs(lstCall[i]-ED.FN_CALL_VEGA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_VEGA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testVegavsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"
        (npCP, stdDevC) = self.__objMonteCall.calculateOption(npStock)
        (npPP, stdDevP) = self.__objMontePut.calculateOption(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Vega - I change my vega by 0.01, (1% move) so adjust here
            diff = abs(npCP["Vega"].values[i] - 0.01*ED.EO_callVega[i])
            maxErr = 0.1*stdDevC["VegaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Put Vega
            diff = abs(npPP["Vega"].values[i] - 0.01*ED.EO_putVega[i])
            maxErr = 0.1*stdDevP["VegaSTD"].values[i]
            self.assertLess(diff, maxErr)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testThetavsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed theta and then ensures
        # the result received is consistent.   The theta isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testThetasExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (pCP, stdDevC) = self.__objMonteCallFN.calculateOption(npStock)
        (pPP, stdDevP) = self.__objMontePutFN.calculateOption(npStock)

        lstCall = list(pCP['Theta'])
        lstPut = list(pPP['Theta'])

        lstCall = [abs(lstCall[i]-ED.FN_CALL_THETA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_THETA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testThetasExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"
        (npCP, stdDevC) = self.__objMonteCall.calculateOption(npStock)
        (npPP, stdDevP) = self.__objMontePut.calculateOption(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Theta - I express theta in 365 day terms and as a largely
            # negative value, so change here
            diff = abs(npCP["Theta"].values[i] + ED.EO_callTheta[i]/365)
            maxErr = 0.1*stdDevC["ThetaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Put Theta
            diff = abs(npPP["Theta"].values[i] + ED.EO_putTheta[i]/365)
            maxErr = 0.1*stdDevP["ThetaSTD"].values[i]
            self.assertLess(diff, maxErr)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testRhovsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed rho and then ensures
        # the result received is consistent.   The rho isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testRhovsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (pCP, stdDevC) = self.__objMonteCallFN.calculateOption(npStock)
        (pPP, stdDevP) = self.__objMontePutFN.calculateOption(npStock)

        lstCall = list(pCP['Rho'])
        lstPut = list(pPP['Rho'])

        lstCall = [abs(lstCall[i]-ED.FN_CALL_RHO[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_RHO[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testRhovsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the "Price", "Delta", "Gamma", "Vega", "Theta", "Rho"
        (npCP, stdDevC) = self.__objMonteCall.calculateOption(npStock)
        (npPP, stdDevP) = self.__objMontePut.calculateOption(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Rho - I change my rho by 0.01, (1%) so adjust here
            diff = abs(npCP["Rho"].values[i] - 0.01*ED.EO_callRho[i])
            maxErr = 0.1*stdDevC["RhoSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Put Rho - I change my rho by 0.01, (1%) so adjust here
            diff = abs(npPP["Rho"].values[i] - 0.01*ED.EO_putRho[i])
            maxErr = 0.1*stdDevP["RhoSTD"].values[i]
            self.assertLess(diff, maxErr)
