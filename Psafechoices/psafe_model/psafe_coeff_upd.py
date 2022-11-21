import pandas as pd
import os
# import numpy as np

def psafe_coeff_upd(coeff):
    coeff = coeff.rename(columns = {'Unnamed: 0':'coeffs'})
    coeff = coeff.set_index('coeffs')
    coeff.loc['kappa.1'] = coeff.loc['kappa.1'] - coeff.loc['constant']
    coeff.loc['kappa.2'] = coeff.loc['kappa.2'] - coeff.loc['constant']
    coeff.loc['kappa.3'] = coeff.loc['kappa.3'] - coeff.loc['constant']
    coeff.loc['kappa.4'] = coeff.loc['kappa.4'] - coeff.loc['constant']
    coeff.loc['kappa.5'] = coeff.loc['kappa.5'] - coeff.loc['constant']
    coeff.loc['constant'] = - coeff.loc['constant']
    coeff = coeff.rename(index = {'constant': 'kappa.0'})
    return coeff

# NEXT STEPS: run a simulation here at the next stepss....with random variables