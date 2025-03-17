"""
@author: ptzouras
National Technical University of Athens
Research project: PhD thesis Tzouras
"""

import os

from logit_est_functons import MLpanelest

root_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(root_dir, 'utilities'))
from util_definition import database, utils
from coeff_definition import betas, sigmas, randoms

# URB FROM ZENODO
url = 'https://zenodo.org/record/14967130/files/choice_dataset_perceivedSafetyChoices.csv?download=1'
link = url
# link = os.path.join(root_dir, 'sample_datasets', 'choice_dataset_perceived_choices_crop.csv')
# t = 2

def car_bin(link, R):
    """
    Estimates a Mixed Logit (ML) model for binary CAR choice using Biogeme.

    Args:
        link (str): The file path or URL to the dataset in CSV format.
        R (int): The number of Monte Carlo draws for simulation.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters for the binary car choice model.

    Example:
        >>> parameters = car_bin("data.csv", 1000)
        >>> print(parameters)
    """
    db = database(link).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'car_binary')
    p = MLpanelest(db, u.get_Bincar_RND(), u.get_modecho_av(), u.get_cho(), R, 'car_binary_logit_model')
    return p

def ebike_bin(link, R):
    """
    Estimates a Mixed Logit (ML) model for E-BIKE car choice using Biogeme.

    Args:
        link (str): The file path or URL to the dataset in CSV format.
        R (int): The number of Monte Carlo draws for simulation.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters for the binary car choice model.

    Example:
        >>> parameters = ebike_bin("data.csv", 1000)
        >>> print(parameters)
    """
    db = database(link).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'ebike_binary')
    p = MLpanelest(db, u.get_Binebike_RND(), u.get_modecho_av(), u.get_cho(), R, 'ebike_binary_logit_model')
    return p

def escoot_bin(link, R):
    """
        Estimates a Mixed Logit (ML) model for binary E-SCOOTER choice using Biogeme.

    Args:
        link (str): The file path or URL to the dataset in CSV format.
        R (int): The number of Monte Carlo draws for simulation.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters for the binary car choice model.

    Example:
        >>> parameters = escoot_bin("data.csv", 1000)
        >>> print(parameters)
    """
    db = database(link).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'escoot_binary')
    p = MLpanelest(db, u.get_Binescoot_RND(), u.get_modecho_av(), u.get_cho(), R, 'escoot_binary_logit_model')
    return p

def walk_bin(link, R):
    """
        Estimates a Mixed Logit (ML) model for binary WALK choice using Biogeme.

    Args:
        link (str): The file path or URL to the dataset in CSV format.
        R (int): The number of Monte Carlo draws for simulation.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters for the binary car choice model.

    Example:
        >>> parameters = walk_bin("data.csv", 1000)
        >>> print(parameters)
    """
    db = database(link).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'walk_binary')
    p = MLpanelest(db, u.get_Binwalk_RND(), u.get_modecho_av(), u.get_cho(), R, 'walk_binary_logit_model')
    return p

def ML_model(link, R):
    """
    Estimates a Mixed Logit (ML) mode choice model using Biogeme.

    Args:
        link (str): The file path or URL to the dataset in CSV format.
        R (int): The number of Monte Carlo draws for simulation.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters for the binary car choice model.

    Example:
        >>> parameters = ML_model("data.csv", 1000)
        >>> print(parameters)
    """
    
    db = database(link).get_dbase()
    b = betas(0, -1000, 1000, 0)
    s = sigmas(0, -1000, 1000, 0)
    rnds = randoms(b, s, 'NORMAL_HALTON2')
    u = utils(db, b, rnds = rnds, exp = 'mode_choice')
    p = MLpanelest(db, u.get_MLVs(), u.get_modecho_av(), u.get_cho(), R, 'mode_choice_ML_model')
    return p


p = ML_model(link, 100)
print(p)