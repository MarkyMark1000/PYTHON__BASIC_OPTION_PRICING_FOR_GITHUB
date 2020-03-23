import analytics.OptionIntrinsicValue
import numpy as np
import unittest

'''
These set of tests are used to ensure the OptionIntrinsicValue class
is working correctly.
It tests the value and the __str__ function for both calls and puts.
'''


class TestIntrinsicOption(unittest.TestCase):

    def setUp(self):

        # Set data to price the option
        self.__fltStrike = 50

        # Build some stock prices to run the test against
        self.__npStock = np.empty(100)
        for i in range(0, 100):
            self.__npStock[i] = (i + 50) * self.__fltStrike / 100

    def testIntrinsicCallValue(self):

        # Get the intrinic value of a call from the stock
        objIntrinsicCall = analytics.OptionIntrinsicValue. \
            OptionIntrinsicValue(
                self.__fltStrike,
                True)
        callIntrinsicValue = objIntrinsicCall.getOptionPrice(
            self.__npStock)

        # Calculate the intrinsic value here iVal and compare it to
        # callIntrinsicValue to ensure it is very close in value
        for i in range(0, len(self.__npStock)):
            iVal = max(self.__npStock[i] - self.__fltStrike, 0)
            diff = abs(callIntrinsicValue[i] - iVal)
            self.assertLess(diff, 0.0000001)

    def testIntrinsicCallStr(self):

        # Get the call
        objIntrinsicCall = analytics.OptionIntrinsicValue. \
            OptionIntrinsicValue(
                self.__fltStrike,
                True)

        # Generate what the repr should look like
        strF = 'OptionIntrinsicValue: [Strike:{strike}; IsCall:{iscall};]'
        strF = strF.format(strike=self.__fltStrike, iscall=True)

        # Ensure the representation is equal
        self.assertEqual(str(objIntrinsicCall), strF)

    def testIntrinsicPutValue(self):

        # Get the intrinic value of a put from the stock
        objIntrinsicPut = analytics.OptionIntrinsicValue. \
            OptionIntrinsicValue(
                self.__fltStrike,
                False)
        putIntrinsicValue = objIntrinsicPut.getOptionPrice(
            self.__npStock)

        # Calculate the intrinsic value here iVal and compare it to
        # putIntrinsicValue to ensure it is very close in value
        for i in range(0, len(self.__npStock)):
            iVal = max(self.__fltStrike - self.__npStock[i], 0)
            diff = abs(putIntrinsicValue[i] - iVal)
            self.assertLess(diff, 0.0000001)

    def testIntrinsicPutStr(self):

        # Get the call
        objIntrinsicPut = analytics.OptionIntrinsicValue. \
            OptionIntrinsicValue(
                self.__fltStrike,
                False)

        # Generate what the repr should look like
        strF = 'OptionIntrinsicValue: [Strike:{strike}; IsCall:{iscall};]'
        strF = strF.format(strike=self.__fltStrike, iscall=False)

        # Ensure the representation is equal
        self.assertEqual(str(objIntrinsicPut), strF)


if __name__ == '__main__':
    unittest.main()
