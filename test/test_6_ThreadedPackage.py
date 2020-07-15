import analytics.EuropeanOptionBoundaryConditions
import analytics.EuropeanOptionThread
import numpy as np
import unittest
from unittest.mock import patch
import math
import test.ExternalData as ED

'''
These set of tests are used to ensure the BasicMonteCarloOptionThreaded
and the PackageForThreading class is working correctly.
Again, it tests the  __str__ and compares the price and greek calculations
against a set of external data that is stored in the ExternalData.py file.
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
The packages only return std results for packages with 1 option in it, so this
test cannot be run on a package of 2 options at the same time.
'''


class TestBasicMonteCarloOptionThreaded(unittest.TestCase):

    def setUp(self):

        # Set data to price the option
        self.__fltStrike = ED.EO_Strike
        self.__fltVol = ED.EO_Vol
        self.__fltRiskFreeRate = ED.EO_RiskFreeRate
        self.__fltTimeToMaturity = ED.EO_TimeToMaturity
        self.__intNoIterations = 200000

        # Convert the spot into an array
        self.__npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Create a package that contains a call option
        self.__objPackage = analytics.EuropeanOptionThread. \
            PackageForThreading(1, "Package1")

        # Create a threaded call option
        objMonteCall = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                self.__intNoIterations,
                name="MyCallOption")

        # Put the call and put into the package
        self.__objPackage.addOption(objMonteCall)

        # Create a package that contains a call option but with
        # the fixed random numbers from the normal distribution
        self.__objPackageFN = analytics.EuropeanOptionThread. \
            PackageForThreading(1, "Package1FN")

        # Create a threaded call option
        objMonteCallFN = analytics.EuropeanOptionThread. \
            BasicMonteCarloOptionThreaded(
                ("Price", "Delta", "Gamma", "Vega", "Theta", "Rho"),
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                len(ED.lstNormal),
                name="MyCallOptionFN")

        # Put the call and put into the package
        self.__objPackageFN.addOption(objMonteCallFN)

        # Get syncronous version of the results
        (self.__objMonteResultsSync, self.__objMonteSTDSync) = \
            self.__objPackage.calculateSyncronousResults(self.__npStock)

        # Start the package
        self.__objPackage.start()

        # calculate the results
        (self.__objMonteResults, self.__objMonteSTD) = self.__objPackage. \
            retrieveThreadedResults(self.__npStock)

        # Join the package
        self.__objPackage.join()

        # Build the thread results using the fixed normal distribution
        with patch.object(np.random, 'standard_normal',
                          return_value=ED.npNormal) as mock_requests:

            # Start the package with fixed normal
            self.__objPackageFN.start()

            # calculate the results
            (self.__objMonteResultsFN,
             self.__objMonteSTDFN) = self.__objPackageFN. \
                retrieveThreadedResults(self.__npStock)

            # Join the package
            self.__objPackageFN.join()

    def testPricevsFixedRandomNumbers(self):

        # The prices are built earlier using patch to fix the random
        # numbers generated for the monte carlo, hence ensureing a
        # fixed price and then ensures the result received is consistent.
        # The price isn't very accurate because we only use 200 points
        # in the list but the result should be stable

        lstR = list(self.__objMonteResultsFN["Price"])
        lstR = [abs(lstR[i]-ED.FN_CALL_PRICE[i])
                for i in range(0, len(lstR))]
        for Z in lstR:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testPricevsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Price
            diff = abs(self.__objMonteResults["Price"].values[i] -
                       ED.EO_callPrice[i])
            maxErr = 0.1*self.__objMonteSTD["PriceSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Call Price Syncronous
            diff = abs(self.__objMonteResultsSync["Price"].values[i] -
                       ED.EO_callPrice[i])
            maxErr = 0.1*self.__objMonteSTDSync["PriceSTD"].values[i]
            self.assertLess(diff, maxErr)

    def testDeltavsFixedRandomNumbers(self):

        # The delta's are built earlier using patch to fix the random
        # numbers generated for the monte carlo, hence ensureing a
        # fixed delta and then ensures the result received is consistent.
        # The delta isn't very accurate because we only use 200 points
        # in the list but the result should be stable

        lstR = list(self.__objMonteResultsFN["Delta"])
        lstR = [abs(lstR[i]-ED.FN_CALL_DELTA[i])
                for i in range(0, len(lstR))]
        for Z in lstR:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testDeltavsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Delta
            diff = abs(self.__objMonteResults["Delta"].values[i] -
                       ED.EO_callDelta[i])
            maxErr = 0.1*self.__objMonteSTD["DeltaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Call Delta Sync
            diff = abs(self.__objMonteResultsSync["Delta"].values[i] -
                       ED.EO_callDelta[i])
            maxErr = 0.1*self.__objMonteSTDSync["DeltaSTD"].values[i]
            self.assertLess(diff, maxErr)

    def testGammavsFixedRandomNumbers(self):

        # The gamma's are built earlier using patch to fix the random
        # numbers generated for the monte carlo, hence ensureing a
        # fixed gamma and then ensures the result received is consistent.
        # The gamma isn't very accurate because we only use 200 points
        # in the list but the result should be stable

        lstR = list(self.__objMonteResultsFN["Gamma"])
        lstR = [abs(lstR[i]-ED.FN_CALL_GAMMA[i])
                for i in range(0, len(lstR))]
        for Z in lstR:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testGammavsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Gamma
            diff = abs(self.__objMonteResults["Gamma"].values[i] -
                       ED.EO_callGamma[i])
            maxErr = 0.1*self.__objMonteSTD["GammaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Call Gamma Sync
            diff = abs(self.__objMonteResultsSync["Gamma"].values[i] -
                       ED.EO_callGamma[i])
            maxErr = 0.1*self.__objMonteSTDSync["GammaSTD"].values[i]
            self.assertLess(diff, maxErr)

    def testVegavsFixedRandomNumbers(self):

        # The vega's are built earlier using patch to fix the random
        # numbers generated for the monte carlo, hence ensureing a
        # fixed vega and then ensures the result received is consistent.
        # The vega isn't very accurate because we only use 200 points
        # in the list but the result should be stable

        lstR = list(self.__objMonteResultsFN["Vega"])
        lstR = [abs(lstR[i]-ED.FN_CALL_VEGA[i])
                for i in range(0, len(lstR))]
        for Z in lstR:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testVegavsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Vega - I change my vega by 0.01, (1% move) so adjust here
            diff = abs(self.__objMonteResults["Vega"].values[i] -
                       0.01*ED.EO_callVega[i])
            maxErr = 0.1*self.__objMonteSTD["VegaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Call Vega Sync
            diff = abs(self.__objMonteResultsSync["Vega"].values[i] -
                       0.01*ED.EO_callVega[i])
            maxErr = 0.1*self.__objMonteSTDSync["VegaSTD"].values[i]
            self.assertLess(diff, maxErr)

    def testThetavsFixedRandomNumbers(self):

        # The theta's are built earlier using patch to fix the random
        # numbers generated for the monte carlo, hence ensureing a
        # fixed theta and then ensures the result received is consistent.
        # The theta isn't very accurate because we only use 200 points
        # in the list but the result should be stable

        lstR = list(self.__objMonteResultsFN["Theta"])
        lstR = [abs(lstR[i]-ED.FN_CALL_THETA[i])
                for i in range(0, len(lstR))]
        for Z in lstR:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testThetasExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Theta - I express theta in 365 day terms and as a largely
            # negative value, so change here
            diff = abs(self.__objMonteResults["Theta"].values[i] +
                       ED.EO_callTheta[i]/365)
            maxErr = 0.1*self.__objMonteSTD["ThetaSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Call Theta sync
            diff = abs(self.__objMonteResultsSync["Theta"].values[i] +
                       ED.EO_callTheta[i]/365)
            maxErr = 0.1*self.__objMonteSTDSync["ThetaSTD"].values[i]
            self.assertLess(diff, maxErr)

    def testRhovsFixedRandomNumbers(self):

        # The rho's are built earlier using patch to fix the random
        # numbers generated for the monte carlo, hence ensureing a
        # fixed rho and then ensures the result received is consistent.
        # The rho isn't very accurate because we only use 200 points
        # in the list but the result should be stable

        lstR = list(self.__objMonteResultsFN["Rho"])
        lstR = [abs(lstR[i]-ED.FN_CALL_RHO[i])
                for i in range(0, len(lstR))]
        for Z in lstR:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testRhovsExternal(self):

        # This form of monte carlo gets the price and greeks in one go
        # depending on the input tpCalcRequirements

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Rho - I change my rho by 0.01, (1%) so adjust here
            diff = abs(self.__objMonteResults["Rho"].values[i] -
                       0.01*ED.EO_callRho[i])
            maxErr = 0.1*self.__objMonteSTD["RhoSTD"].values[i]
            self.assertLess(diff, maxErr)
            # Call Rho Sync
            diff = abs(self.__objMonteResultsSync["Rho"].values[i] -
                       0.01*ED.EO_callRho[i])
            maxErr = 0.1*self.__objMonteSTDSync["RhoSTD"].values[i]
            self.assertLess(diff, maxErr)
