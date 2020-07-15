import analytics.EuropeanOptionBoundaryConditions
import analytics.EuropeanOption
import unittest
from unittest.mock import patch
import math
import test.ExternalData as ED
from analytics.EuropeanOption import np

'''
These set of tests are used to ensure the BasicMonteCarloOption
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


class TestBasicMonteCarloOption(unittest.TestCase):

    def setUp(self):

        # Set data to price the option
        self.__fltStrike = ED.EO_Strike
        self.__fltVol = ED.EO_Vol
        self.__fltRiskFreeRate = ED.EO_RiskFreeRate
        self.__fltTimeToMaturity = ED.EO_TimeToMaturity
        self.__intNoIterations = 200000

        # Add a call option
        self.__objEuropeanMonteCall = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                self.__intNoIterations)

        # Add a call option with number of iterations equal to the
        # fixed list of random normal numbers
        self.__objEuropeanMonteCallFN = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                len(ED.lstNormal))

        # Add a put option
        self.__objEuropeanMontePut = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                False,
                self.__intNoIterations)

        # Add a put option with number of iterations equal to the
        # fixed list of random normal numbers
        self.__objEuropeanMontePutFN = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                False,
                len(ED.lstNormal))

    def testEuropeanCallStr(self):

        # Evaluate what the call should look like
        strF = 'BasicMonteCarloOption: [Strike:{strike}; Vol:{vol}; ' \
               'RFRate:{rfrate}; Time:{time}; IsCall:{iscall}; ' \
               'NoIter:{noiter}]'
        strF = strF.format(strike=self.__fltStrike, vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=True,
                           noiter=self.__intNoIterations)

        # Compare the string option representation
        self.assertEqual(str(self.__objEuropeanMonteCall), strF)

    def testEuropeanPutStr(self):

        # Evaluate what the call should look like
        strF = 'BasicMonteCarloOption: [Strike:{strike}; Vol:{vol}; ' \
               'RFRate:{rfrate}; Time:{time}; IsCall:{iscall}; ' \
               'NoIter:{noiter}]'
        strF = strF.format(strike=self.__fltStrike, vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=False,
                           noiter=self.__intNoIterations)

        # Compare the string option representation
        self.assertEqual(str(self.__objEuropeanMontePut), strF)

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testEuropeanPricevsFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed price and then ensures
        # the result received is consistent.   The price isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testEuropeanPricevsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npCP, stdDevC) = self.__objEuropeanMonteCallFN.getOptionPrice(npStock)
        (npPP, stdDevP) = self.__objEuropeanMontePutFN.getOptionPrice(npStock)

        lstCall = list(npCP)
        lstPut = list(npPP)

        lstCall = [abs(lstCall[i]-ED.FN_CALL_PRICE[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_PRICE[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testEuropeanPricevsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npCP, stdDevC) = self.__objEuropeanMonteCall.getOptionPrice(npStock)
        (npPP, stdDevP) = self.__objEuropeanMontePut.getOptionPrice(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call Price
            diffCallPrice = abs(npCP[i] - ED.EO_callPrice[i])
            self.assertLess(diffCallPrice, 0.1 * stdDevC[i])
            # Put Price
            diffPutPrice = abs(npPP[i] - ED.EO_putPrice[i])
            self.assertLess(diffPutPrice, 0.1 * stdDevP[i])

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testEuropeanDeltasFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed delta and then ensures
        # the result received is consistent.   The delta isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testEuropeanDeltavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCallFN.getOptionDelta(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePutFN.getOptionDelta(npStock)

        lstCall = list(npC)
        lstPut = list(npP)

        lstCall = [abs(lstCall[i]-ED.FN_CALL_DELTA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_DELTA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testEuropeanDeltavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCall.getOptionDelta(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePut.getOptionDelta(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call
            diffCall = abs(npC[i] - ED.EO_callDelta[i])
            self.assertLess(diffCall, 0.1 * stdDevC[i])
            # Put
            diffPut = abs(npP[i] - ED.EO_putDelta[i])
            self.assertLess(diffPut, 0.1 * stdDevP[i])

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testEuropeanGammaFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed gamma and then ensures
        # the result received is consistent.   The gamma isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testEuropeanGammavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCallFN.getOptionGamma(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePutFN.getOptionGamma(npStock)

        lstCall = list(npC)
        lstPut = list(npP)

        lstCall = [abs(lstCall[i]-ED.FN_CALL_GAMMA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_GAMMA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testEuropeanGammavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCall.getOptionGamma(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePut.getOptionGamma(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call
            diffCall = abs(npC[i] - ED.EO_callGamma[i])
            self.assertLess(diffCall, 0.1 * stdDevC[i])
            # Put
            diffPut = abs(npP[i] - ED.EO_putGamma[i])
            self.assertLess(diffPut, 0.1 * stdDevP[i])

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testEuropeanVegaFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed vega and then ensures
        # the result received is consistent.   The vega isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testEuropeanVegavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCallFN.getOptionVega(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePutFN.getOptionVega(npStock)

        lstCall = list(npC)
        lstPut = list(npP)

        lstCall = [abs(lstCall[i]-ED.FN_CALL_VEGA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_VEGA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testEuropeanVegavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCall.getOptionVega(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePut.getOptionVega(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call - I change my vega by 0.01, (1% move) so adjust here
            diffCall = abs(npC[i] - 0.01*ED.EO_callVega[i])
            self.assertLess(diffCall, 0.1 * stdDevC[i])
            # Put - I change my vega by 0.01, (1% move) so adjust here
            diffPut = abs(npP[i] - 0.01*ED.EO_putVega[i])
            self.assertLess(diffPut, 0.1 * stdDevP[i])

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testEuropeanRhoFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed rho and then ensures
        # the result received is consistent.   The rho isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testEuropeanRhovsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCallFN.getOptionRho(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePutFN.getOptionRho(npStock)

        lstCall = list(npC)
        lstPut = list(npP)

        lstCall = [abs(lstCall[i]-ED.FN_CALL_RHO[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_RHO[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testEuropeanRhovsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCall.getOptionRho(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePut.getOptionRho(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call - I change my rho by 0.01, (1%) so adjust here
            diffCall = abs(npC[i] - 0.01*ED.EO_callRho[i])
            self.assertLess(diffCall, 0.1 * stdDevC[i])
            # Put - I change my rho by 0.01, (1%) so adjust here
            diffPut = abs(npP[i] - 0.01*ED.EO_putRho[i])
            self.assertLess(diffPut, 0.1 * stdDevP[i])

    @patch.object(np.random, 'standard_normal', return_value=ED.npNormal)
    def testEuropeanThetaFixedRandomNumbers(self, mock_np_random):

        # This test, uses patch to fix the random numbers generated for
        # the monte carlo, hence ensureing a fixed theta and then ensures
        # the result received is consistent.   The theta isn't very
        # accurate because we only use 200 points in the list but the result
        # should be stable (unlike testEuropeanThetavsExternal)

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCallFN.getOptionTheta(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePutFN.getOptionTheta(npStock)

        lstCall = list(npC)
        lstPut = list(npP)

        lstCall = [abs(lstCall[i]-ED.FN_CALL_THETA[i])
                   for i in range(0, len(lstCall))]
        lstPut = [abs(lstPut[i]-ED.FN_PUT_THETA[i])
                  for i in range(0, len(lstPut))]

        for Z in lstCall:
            self.assertLess(Z, ED.FN_ACCURACY)
        for Z in lstPut:
            self.assertLess(Z, ED.FN_ACCURACY)

    def testEuropeanThetavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        (npC, stdDevC) = self.__objEuropeanMonteCall.getOptionTheta(npStock)
        (npP, stdDevP) = self.__objEuropeanMontePut.getOptionTheta(npStock)

        # This is a very approximate comparison, because we are using a
        # monte carlo method
        for i in range(0, len(ED.EO_spot)):
            # Call - I express theta in 365 day terms and as a largely
            # negative value so change here
            diffCall = abs(npC[i] + ED.EO_callTheta[i]/365)
            self.assertLess(diffCall, 0.1 * stdDevC[i])
            # Put - I express theta in 365 day terms and as a largely
            # negative value so change here
            diffPut = abs(npP[i] + ED.EO_putTheta[i]/365)
            self.assertLess(diffPut, 0.1 * stdDevP[i])


if __name__ == '__main__':
    unittest.main()
