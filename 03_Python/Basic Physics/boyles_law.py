# -*- coding: utf-8 -*-
"""
    Boyle's law
    ===========
    
    Boyle's law states that the pressure of a sample of gas is inversely
    proportional to its volume if the temperature of the gas remains constant.
    Robert Boyle published this relationship in 1662 based on experimental data.
    Another way of representing this relationship is through the mathematical 
    equation, 
    
        P1V1 = P2V2, 
        
    which shows that the product of the pressure and volume conditions of a gas
    is a constant. Therefore:
        
        P1V1 = cte, T = cte.

"""


import numpy as np
from matplotlib import pyplot as plt

volume = np.array([48, 46, 44, 42, 40, 38, 36, 34,
                   32, 30, 28, 26, 24, 23, 22, 21,
                   20, 19, 18, 17, 16, 15, 14, 13, 12])

pressure = np.array([29.1250, 30.5625, 31.9375, 33.5000, 35.3125, 37.0000, 39.3125, 41.6250,
                     44.1875, 47.0625, 50.3125, 54.3125, 58.8125, 61.3125, 64.0625, 67.0625,
                     70.6875, 74.1250, 77.8750, 82.7500, 87.8750, 93.0625, 100.4375, 107.8125, 117.5625])

fig, axis = plt.subplots(2, 1)

axis[0].plot(pressure, volume)
axis[1].plot(1 / pressure, volume)


for i in (volume * pressure):
    print(i)