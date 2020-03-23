import analytics.EuropeanOptionBoundaryConditions
import analytics.EuropeanOption
import numpy as np
import unittest
import math
import test.ExternalData as ED

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
'''


class TestBasicMonteCarloOption(unittest.TestCase):

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
        #     self.__npStock[i] = (i + 50) * self.__fltStrike / 100

        # Add a call option
        self.__objEuropeanMonteCall = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True,
                self.__intNoIterations)

        # Add a put option
        self.__objEuropeanMontePut = analytics.EuropeanOption. \
            BasicMonteCarloOption(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                False,
                self.__intNoIterations)

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
