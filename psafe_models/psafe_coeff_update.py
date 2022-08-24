"""
PSAFE coefficients update

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
# import OS
import numpy as np

def coeff_upd():
    coeff = pd.read_csv('outputs/simple_psafe_models.csv', ',')
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

# run a simulation here at the next stepss....with random variables