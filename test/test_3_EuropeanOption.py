import analytics.EuropeanOptionBoundaryConditions
import analytics.EuropeanOption
import numpy as np
import unittest
import math
import test.ExternalData as ED

'''
These set of tests are used to ensure the EuropeanOptionBoundaryConditions
class is working correctly.
It tests the  __str__, and the values returned from the BlackScholes model
against the BoundaryConditions, put-call parity, delta range and compares
the price and greek calculations against a set of external data that is
stored in the ExternalData.py file.
This is done for both Call and Put options.
'''


class TestEuropeanOption(unittest.TestCase):

    def setUp(self):

        # Set data to price the option
        self.__fltStrike = ED.EO_Strike
        self.__fltVol = ED.EO_Vol
        self.__fltRiskFreeRate = ED.EO_RiskFreeRate
        self.__fltTimeToMaturity = ED.EO_TimeToMaturity

        # Build some stock prices to run the test against
        self.__npStock = np.empty(100)
        for i in range(0, 100):
            self.__npStock[i] = (i + 50) * self.__fltStrike / 100

        # Add a call option
        self.__objEuropeanCall = analytics.EuropeanOption. \
            BlackScholes(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                True)

        # Add a put option
        self.__objEuropeanPut = analytics.EuropeanOption. \
            BlackScholes(
                self.__fltStrike,
                self.__fltVol,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity,
                False)

    def testEuropeanCallStr(self):

        # Evaluate what the call should look like
        strF = 'EuropeanOption: [Strike:{strike}; Vol:{vol}; '\
                'RFRate:{rfrate}; Time:{time}; IsCall:{iscall};]'
        strF = strF.format(strike=self.__fltStrike,
                           vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=True)

        # Compare the string option representation
        self.assertEqual(str(self.__objEuropeanCall), strF)

    def testEuropeanPutStr(self):

        # Evaluate what the call should look like
        strF = 'EuropeanOption: [Strike:{strike}; Vol:{vol}; '\
                'RFRate:{rfrate}; Time:{time}; IsCall:{iscall};]'
        strF = strF.format(strike=self.__fltStrike,
                           vol=self.__fltVol,
                           rfrate=self.__fltRiskFreeRate,
                           time=self.__fltTimeToMaturity,
                           iscall=False)

        # Compare the string option representation
        self.assertEqual(str(self.__objEuropeanPut), strF)

    def testEuropeanCallAgainstBoundaryConditions(self):

        # Get the boundary conditions of a call from the stock
        objBoundCall = analytics.EuropeanOptionBoundaryConditions. \
            EuropeanOptionBoundaryConditions(
                self.__fltStrike,
                True,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity)
        callLowerBound = objBoundCall.getLowerBoundary(self.__npStock)
        callUpperBound = objBoundCall.getUpperBoundary(self.__npStock)

        # Get the call option price
        callPrice = self.__objEuropeanCall. \
            getOptionPrice(self.__npStock)

        # Check the call option price is always between the boundaries
        for i in range(0, len(self.__npStock)):
            # Lower boundary
            self.assertGreaterEqual(callPrice[i], callLowerBound[i])
            # Upper boundary
            self.assertLessEqual(callPrice[i], callUpperBound[i])

    def testEuropeanPutAgainstBoundaryConditions(self):

        # Get the boundary conditions of a put from the stock
        objBoundPut = analytics.EuropeanOptionBoundaryConditions. \
            EuropeanOptionBoundaryConditions(
                self.__fltStrike,
                False,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity)
        putLowerBound = objBoundPut.getLowerBoundary(self.__npStock)
        putUpperBound = objBoundPut.getUpperBoundary(self.__npStock)

        # Get the put option price
        putPrice = self.__objEuropeanPut. \
            getOptionPrice(self.__npStock)

        # Check the put option price is always between the boundaries
        for i in range(0, len(self.__npStock)):
            # Lower boundary
            self.assertGreaterEqual(putPrice[i], putLowerBound[i])
            # Upper boundary
            self.assertLessEqual(putPrice[i], putUpperBound[i])

    def testPutCallParity(self):

        # test to ensure Call + K x Exp(-rT) is the same as Put + Spot

        # get call price
        callPrice = self.__objEuropeanCall.getOptionPrice(self.__npStock)

        # adjust the price by te strke adjustment
        strKAdj = self.__fltStrike * math.exp(-self.__fltRiskFreeRate
                                              * self.__fltTimeToMaturity)
        callPrice = callPrice + strKAdj

        # get the put price
        putPrice = self.__objEuropeanPut.getOptionPrice(self.__npStock)

        # adjust the price by the spot
        putPrice = putPrice + self.__npStock

        # Check the values are always close in value
        for i in range(0, len(self.__npStock)):
            diff = abs(callPrice[i]-putPrice[i])
            self.assertLess(diff, 0.00001)

    def testEuropeanDeltaRange(self):

        # Ensure delta is always between 0 and 1 for a call and -1 and 0
        # for a put

        # Get delta's
        callDelta = self.__objEuropeanCall.getOptionDelta(self.__npStock)
        putDelta = self.__objEuropeanPut.getOptionDelta(self.__npStock)

        # Check the values are always close in value
        for i in range(0, len(self.__npStock)):
            # Call
            self.assertLessEqual(callDelta[i], 1)
            self.assertGreaterEqual(callDelta[i], 0)
            # Put
            self.assertLessEqual(putDelta[i], 0)
            self.assertGreaterEqual(putDelta[i], -1)

    def testEuropeanPricevsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        npCP = self.__objEuropeanCall.getOptionPrice(npStock)
        npPP = self.__objEuropeanPut.getOptionPrice(npStock)

        for i in range(0, len(ED.EO_spot)):
            # Call Price
            diffCallPrice = abs(npCP[i] - ED.EO_callPrice[i])
            self.assertLess(diffCallPrice, 0.00001)
            # Put Price
            diffPutPrice = abs(npPP[i] - ED.EO_putPrice[i])
            self.assertLess(diffPutPrice, 0.00001)

    def testEuropeanDeltavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        npC = self.__objEuropeanCall.getOptionDelta(npStock)
        npP = self.__objEuropeanPut.getOptionDelta(npStock)

        for i in range(0, len(ED.EO_spot)):
            # Call
            diffCall = abs(npC[i] - ED.EO_callDelta[i])
            self.assertLess(diffCall, 0.00001)
            # Put
            diffPut = abs(npP[i] - ED.EO_putDelta[i])
            self.assertLess(diffPut, 0.00001)

    def testEuropeanGammavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        npC = self.__objEuropeanCall.getOptionGamma(npStock)
        npP = self.__objEuropeanPut.getOptionGamma(npStock)

        for i in range(0, len(ED.EO_spot)):
            # Call
            diffCall = abs(npC[i] - ED.EO_callGamma[i])
            self.assertLess(diffCall, 0.00001)
            # Put
            diffPut = abs(npP[i] - ED.EO_putGamma[i])
            self.assertLess(diffPut, 0.00001)

    def testEuropeanVegavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        npC = self.__objEuropeanCall.getOptionVega(npStock)
        npP = self.__objEuropeanPut.getOptionVega(npStock)

        for i in range(0, len(ED.EO_spot)):
            # Call - I change my vega by 0.01, (1% move) so adjust here
            diffCall = abs(npC[i] - 0.01*ED.EO_callVega[i])
            self.assertLess(diffCall, 0.00001)
            # Put - I change my vega by 0.01, (1% move) so adjust here
            diffPut = abs(npP[i] - 0.01*ED.EO_putVega[i])
            self.assertLess(diffPut, 0.00001)

    def testEuropeanRhovsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        npC = self.__objEuropeanCall.getOptionRho(npStock)
        npP = self.__objEuropeanPut.getOptionRho(npStock)

        for i in range(0, len(ED.EO_spot)):
            # Call - I change my rho by 0.01, (1%) so adjust here
            diffCall = abs(npC[i] - 0.01*ED.EO_callRho[i])
            self.assertLess(diffCall, 0.00001)
            # Put - I change my rho by 0.01, (1%) so adjust here
            diffPut = abs(npP[i] - 0.01*ED.EO_putRho[i])
            self.assertLess(diffPut, 0.00001)

    def testEuropeanThetavsExternal(self):

        # These values have been generated externally via the following
        # website:
        # https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

        # Convert the spot into an array
        npStock = np.asarray(ED.EO_spot, dtype=np.float32)

        # Get the price
        npC = self.__objEuropeanCall.getOptionTheta(npStock)
        npP = self.__objEuropeanPut.getOptionTheta(npStock)

        for i in range(0, len(ED.EO_spot)):
            # Call - I express theta in 365 day terms and as a largel
            #  negative value so change here
            diffCall = abs(-365 * npC[i] - ED.EO_callTheta[i])
            self.assertLess(diffCall, 0.00001)
            # Put - I express theta in 365 day terms and as a largely
            # negative value so change here
            diffPut = abs(-365 * npP[i] - ED.EO_putTheta[i])
            self.assertLess(diffPut, 0.00001)


if __name__ == '__main__':
    unittest.main()
