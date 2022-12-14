import pandas as pd
import os
# import numpy as np

def psafe_coeff_upd(df):
    df = df.rename(columns = {'Unnamed: 0':'coeffs'})
    df = df.set_index('coeffs')
    df.loc['kappa.1'] = df.loc['kappa.1'] - df.loc['constant']
    df.loc['kappa.2'] = df.loc['kappa.2'] - df.loc['constant']
    df.loc['kappa.3'] = df.loc['kappa.3'] - df.loc['constant']
    df.loc['kappa.4'] = df.loc['kappa.4'] - df.loc['constant']
    df.loc['kappa.5'] = df.loc['kappa.5'] - df.loc['constant']
    df.loc['constant'] = - df.loc['constant']
    df = df.rename(index = {'constant': 'kappa.0'})
    return df

# NEXT STEPS: run a simulation here at the next stepss....with random variables