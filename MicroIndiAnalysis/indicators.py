# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import zipfile
# import tempfile
# import os
# import seaborn as sb
# sb.set_theme()

def car_co2(vkm, shICEV = 1.0, shHEV = 0.0, shEV = 0.0):
    x = (0.11 * vkm * (shICEV + shHEV + shEV))
    return x

def car_cost(vkm, shICEV = 1.0, shHEV = 0.0, shEV = 0.0):
    fuelPrice = 1.8 # eur/lt
    fpICEV = fuelPrice # filled from above
    fpHEV = fuelPrice  # filled from above
    fpEV = 0.2
    efICEV = 5.5    # lt/100km
    efHEV = 4.5     # lt/100km
    km_kwh = 4.8
    efEV = 1/km_kwh # Calculated from km_kwh
    x = (efICEV / 100) * fpICEV * (vkm * shICEV) + (efHEV / 100) * fpHEV * (vkm * shHEV) + (efEV / 100) * fpEV * (vkm * shEV)
    return x

def car_safety(vkm):
    x = (6 * 10**(-9)) * vkm
    return x

def escoot_co2(vkm):
    x = ((0.01024 * vkm) / 1000)*628
    return x

def escoot_cost(vkm):
    x = 1 + 0.9375 * vkm
    return x

def escoot_safety(vkm):
    x = (30.6 * 10**(-9)) * vkm
    return x