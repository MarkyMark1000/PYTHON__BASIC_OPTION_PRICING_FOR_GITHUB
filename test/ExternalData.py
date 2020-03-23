'''
This data is used to test the price and greeks of a European call and
put option are valid

The price, delta ...Theta values have been generated externally via the
following website:
    https://www.math.drexel.edu/~pg/fin/VanillaCalculator.html

'''

# Fixed values for the test
EO_Strike = 50
EO_Vol = 0.2
EO_RiskFreeRate = 0.01
EO_TimeToMaturity = 1
EO_spot = [25, 45, 65]
# Values generated from external website
EO_callPrice = [0.0005702320, 1.9307066574, 15.9481600990]
EO_putPrice = [24.5030619195, 6.4331983449, 0.4506517865]
EO_callDelta = [0.0004570682, 0.3531602156, 0.9281048725]
EO_putDelta = [-0.9995429318, -0.6468397844, -0.0718951275]
EO_callGamma = [0.0003270398, 0.0412892459, 0.0105424145]
EO_putGamma = [0.0003270398, 0.0412892459, 0.0105424145]
EO_callVega = [0.0408799729, 16.7221446014, 8.9083402750]
EO_putVega = [0.0408799729, 16.7221446014, 8.9083402750]
EO_callRho = [0.0108564724, 13.9615030448, 44.3786566108]
EO_putRho = [-49.4916352150, -35.5409886426, -5.1238350766]
EO_callTheta = [0.0041965620, 1.8118294906, 1.3346205936]
EO_putTheta = [-0.4908283549, 1.3168045737, 0.8395956767]
