import analytics.EuropeanOptionBoundaryConditions
import numpy as np
import unittest
import math

'''
These set of tests are used to ensure the EuropeanOptionBoundaryConditions
class s working correctly.
It tests the  __str__, upper boundary and lower boundary for both call
and put options.
'''


class TestEuropeanOptionBoundaryConditions(unittest.TestCase):

    def setUp(self):

        # Set data to price the option
        self.__fltStrike = 50
        self.__fltVol = 0.2
        self.__fltRiskFreeRate = 0.01
        self.__fltTimeToMaturity = 1

        # Build some stock prices to run the test against
        self.__npStock = np.empty(100)
        for i in range(0, 100):
            self.__npStock[i] = (i + 50) * self.__fltStrike / 100

        # Build bondary condition objects
        self.__objBoundCall = analytics.EuropeanOptionBoundaryConditions. \
            EuropeanOptionBoundaryConditions(
                self.__fltStrike,
                True,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity)

        self.__objBoundPut = analytics.EuropeanOptionBoundaryConditions. \
            EuropeanOptionBoundaryConditions(
                self.__fltStrike,
                False,
                self.__fltRiskFreeRate,
                self.__fltTimeToMaturity)

    def testCallBoundaryConditionStr(self):

        # Test to ensure the Str representation of Boundary condition
        # class is ok

        # Get what the format should look like
        strF = 'OptionBoundaryConditions: [Strike:{strike}; IsCall:{iscall};]'
        strF = strF.format(strike=self.__fltStrike, iscall=True)

        self.assertEqual(str(self.__objBoundCall), strF)

    def testPutBoundaryConditionStr(self):

        # Test to ensure the Str representation of Boundary condition
        # class is ok

        # Get what the format should look like
        strF = 'OptionBoundaryConditions: [Strike:{strike}; IsCall:{iscall};]'
        strF = strF.format(strike=self.__fltStrike, iscall=False)

        self.assertEqual(str(self.__objBoundPut), strF)

    def testCallUpperBoundary(self):

        uBound = self.__objBoundCall.getUpperBoundary(self.__npStock)

        # Call upper boundary should be the stock price
        for i in range(0, len(self.__npStock)):
            diff = abs(self.__npStock[i] - uBound[i])
            self.assertLess(diff, 0.01*self.__npStock[i])

    def testCallLowerBoundary(self):

        lBound = self.__objBoundCall.getLowerBoundary(self.__npStock)

        # Call Lower Boundary should be max max( S - K x Exp(-rT), 0)
        for i in range(0, len(self.__npStock)):
            a1 = self.__npStock[i] - \
                self.__fltStrike * \
                math.exp(-self.__fltRiskFreeRate * self.__fltTimeToMaturity)
            lb = max(a1, 0)
            diff = abs(lb - lBound[i])
            self.assertLessEqual(diff, 0.01*lb)

    def testPutUpperBoundary(self):

        uBound = self.__objBoundPut.getUpperBoundary(self.__npStock)

        # Put upper boundary should be K x exp(-rT)
        for i in range(0, len(self.__npStock)):
            ub = self.__fltStrike * \
                math.exp(-self.__fltRiskFreeRate * self.__fltTimeToMaturity)
            diff = abs(ub - uBound[i])
            self.assertLess(diff, 0.01*ub)

    def testPutLowerBoundary(self):

        lBound = self.__objBoundPut.getLowerBoundary(self.__npStock)

        # Call Lower Boundary should be max max ( K x Exp(-rT) - S, 0)
        for i in range(0, len(self.__npStock)):
            a1 = self.__fltStrike * \
                math.exp(-self.__fltRiskFreeRate * self.__fltTimeToMaturity) \
                - self.__npStock[i]
            lb = max(a1, 0)
            diff = abs(lb - lBound[i])
            self.assertLessEqual(diff, 0.01*lb)
