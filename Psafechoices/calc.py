"""
Tools to calculate perceived safety rates based on a default model

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
import numpy as np
# import os
# import matplotlib.pyplot as plt


def inf_match(s_inf):
    """
    This function converts the sting categories of road infrastructure (inf) attributes into int.

    Parameters
    ----------
    s_inf : str
        The infrastructure type in string format. The main categories are:
            '1: Urban road with sidewalk less than 1.5 m wide'
            '2: Urban road with sidewalk more than 1.5 m wide'
            '3: Urban road with cycle lane'
            '4: Shared space'
    Returns
    -------
    inf: float
        The infrastructure type in int format.

    """
    inf = 999  # 999, if not matched
    if s_inf == '1: Urban road with sidewalk less than 1.5 m wide':
        inf = int(1)
    # standarized categories given to the user in drop-down menu in GIS
    elif s_inf == '2: Urban road with sidewalk more than 1.5 m wide':
        inf = int(2)
    elif s_inf == '3: Urban road with cycle lane':
        inf = int(3)
    elif s_inf == '4: Shared space':
        inf = int(4)
    return inf


x = inf_match('Urban road with sidewalk more than 1.5 m wide')


def pav_match(s_pav):
    """
    This function converts the sting categories of pavement condition (pav) attributes into int.

    Parameters
    ----------
    s_pav : str
        The pavement condition in string format. The main categories are:
            '0: bad condition'
            '1: good condition'
    Returns
    -------
    pav: float
        The pavement condition in int format.

    """
    pav = 999
    if s_pav == '0: bad condition':
        pav = 0
    # standarized coding - binary variable so one beta parameter
    elif s_pav == '1: good condition':
        pav = 1
    return pav


def obst_match(s_obst):
    """
    This function converts the sting categories of obstacles existence (obst) attributes into int.

    Parameters
    ----------
    s_obst : str
        The obstacles existence in string format. The main categories are:
            '0: yes obstacles'
            '1: no obstacles'
    Returns
    -------
    obst: float
        The obstacles existence in int format.

    """
    obst = 999
    if s_obst == '0: yes obstacles':
        obst = 0
    # standarized coding - binary variable so one beta parameter
    elif s_obst == '1: no obstacles':
        obst = 1
    return obst


def cross_match(s_cross):
    """
    This function converts the sting categories of crossing type (cross) attributes into int.

    Parameters
    ----------
    s_cross : str
        The obstacles existence in string format. The main categories are:
           '0: without pedestrian crossings'
           '1: with pedestrian crossings not controlled by traffic lights'
           '2: with pedestrian crossing controlled by traffic lights' 
    Returns
    -------
    cros: float
        The crossing type in int format.

    """
    cross = 999
    # it may need modification if dummy coding to describe non-linearities among categories
    if s_cross == '0: without pedestrian crossings':
        cross = 0
    elif s_cross == '1: with pedestrian crossings not controlled by traffic lights':
        cross = 1
    elif s_cross == '2: with pedestrian crossing controlled by traffic lights':
        cross = 2
    return cross


def coeffUpd(df):
    """
    Kappa thresholds update, if the ordinal model contains a constant

    Parameters
    ----------
    df : pd.DataFrame
        A dataframe with the the default model coefficients.

    Returns
    -------
    df : pd.DataFrame
         The updated model parameters
    """

    # df = df.rename(columns={'Unnamed: 0': 'coeffs'})
    # df = df.set_index('coeffs')
    df.loc['kappa.1'] = df.loc['kappa.1'] - df.loc['constant']
    df.loc['kappa.2'] = df.loc['kappa.2'] - df.loc['constant']
    df.loc['kappa.3'] = df.loc['kappa.3'] - df.loc['constant']
    df.loc['kappa.4'] = df.loc['kappa.4'] - df.loc['constant']
    df.loc['kappa.5'] = df.loc['kappa.5'] - df.loc['constant']
    df.loc['constant'] = - df.loc['constant']
    df = df.rename(index={'constant': 'kappa.0'})
    return df


def latentEst(row, mode, cf):
    """
    It gives the perceived safety llatent variable value (float) for one specific transport mode,
    for one specific link.
    It does not consider kappa thresholds

    Parameters
    ----------
    row : pd.series
        A row of links dataframe contains all the necessary attributes: inf, pav, obst, cross
    mode : str
        The transport mode for which perceived safety level is estimated
    cf : pd.DataFrame
        A dataframe with the the default model coefficients.

    Returns
    -------
    float
    the pecrceived safety latent variable estimation

    """

    inf = inf_match(row['inf'])
    inf1, inf2, inf4 = (inf == 1), (inf == 2), (inf == 4)

    cross = cross_match(row['cross'])
    cross1, cross2 = (cross == 1), (cross == 2)

    pav = pav_match(row['pav'])
    obst = obst_match(row['obst'])

    b_inf1, b_inf2, b_inf4 = cf.loc[['type1', 'type2', 'type4'], mode]
    b_cross1, b_cross2 = cf.loc[['cross1', 'cross2'], mode]
    b_pav, b_obst = cf.loc[['pav', 'obst'], mode]

    y = (b_inf1 * inf1 + b_inf2 * inf2 + b_inf4 * inf4 +
         b_cross1 * cross1 + b_cross2 * cross2 +
         b_pav * pav + b_obst * obst)

    return y


def levelEst(x, cf, mode):
    """
    It gives the perceived safety level (int) for one specific transport mode,
    for one specific link.
    It considers kappa thresholds

    Parameters
    ----------
    x : float
        the latent variable value of perceived safety
    cf : pd.DataFrame
        A dataframe with the the default model coefficients.
    mode : str
        The transport mode for which perceived safety level is estimated

    Returns
    -------
    int
    the pecrceived safety level estimation

    """
    k = cf.loc[['kappa.0', 'kappa.1', 'kappa.2',
                'kappa.3', 'kappa.4', 'kappa.5'], mode].values

    if x != 999:
        return np.searchsorted(k, x) + 1
    return 7


def processRowEst(index, row, modes, cf):
    """
    Parameters
    ----------
    row : pd.series
        A row of links dataframe contains all the necessary attributes: inf, pav, obst, cross
    modes : list
        The transport modes for which the perceived safety will be estimated per link
    cf : pd.DataFrame
        A dataframe with the the default model coefficients.
    Returns
    -------
    pd.Series
        The updated row with perceived safety (Latent Variable and Levels) estimated per transport mode

    """
    results = {}
    index = row.name

    # Check if any of the key columns ('inf', 'pav', 'cross', 'obst') are 999
    if any(row[col] == 999 for col in ['inf', 'pav', 'cross', 'obst']):
        print(
            f"Processed row {index}: Perceived safety not estimated due to 999 value in one of the key columns.")
    else:
        for m in modes:
            latent_var = latentEst(row, m, cf)
            safety_level = levelEst(latent_var, cf, m)
            results[f'LatPsafe{m}'] = latent_var
            results[f'LevPsafe{m}'] = safety_level

        print(
            f"Processed row {index}: Perceived safety estimated successfully.")

    # Return the results (empty if 999 found, or populated with values if not)
    return pd.Series(results)
