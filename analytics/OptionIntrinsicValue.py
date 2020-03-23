import numpy as np
import pandas as pd
import scipy.stats as si

'''
This section calculates the intrinsic value of an option which can be compared
to any European Option calculations to see how it compares.
'''


class OptionIntrinsicValue():

    # Private Functions
    def __init__(self, fltStrike, boolIsCall):
        self.__fltStrike = fltStrike
        self.__boolIsCall = boolIsCall

    def __str__(self):
        strF = 'OptionIntrinsicValue: [Strike:{strike}; IsCall:{iscall};]'
        return strF.format(strike=self.__fltStrike, iscall=self.__boolIsCall)

    def __getCallPrice(self, npStock):
        npCall = np.maximum(npStock - self.__fltStrike, 0)
        # return npCall[:, 0]
        return npCall

    def __getPutPrice(self, npStock):
        npPut = np.maximum(self.__fltStrike - npStock, 0)
        # return npPut[:, 0]
        return npPut

    # Public Functions
    def getOptionPrice(self, npStock):
        if self.__boolIsCall:
            return self.__getCallPrice(npStock)
        else:
            return self.__getPutPrice(npStock)
