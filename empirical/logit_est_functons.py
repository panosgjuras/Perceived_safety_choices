"""
Tools to perform logit model estimations

@author: ptzouras
National Technical University of Athens
"""
# import os
# import pandas as pd
import biogeme.messaging as msg
import biogeme.biogeme as bio
from biogeme import models
# import biogeme.results as res
from biogeme.expressions import (PanelLikelihoodTrajectory,MonteCarlo, log)

def MNLest(df, V, av, cho, name):    
    """
    Estimates a multinomial logit (MNL) model using Biogeme.

    Args:
        df (pandas.DataFrame): The dataset containing the choice data.
        V (dict): A dictionary containing the utility functions for each alternative.
        av (dict): A dictionary indicating the availability of each alternative.
        cho (pandas.Series): A series containing the alternatives that are available.
        name (str): The name of the model.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters.

    Example:
        >>> results = MNLest(data, V, av, choice, "MNL_Model")
        >>> print(results)
""" 
    logprob = models.loglogit(V, av, cho) # import utilities in loglogit
    logger = msg.bioMessage() 
    logger.setDetailed()  
    biogeme = bio.BIOGEME(df, logprob) # estimate biogeme based on the defined database
    biogeme.calculateNullLoglikelihood(av)
    biogeme.modelName = name
    results = biogeme.estimate()
    p = results.getEstimatedParameters()
    return p

def MLpanelest(df, V, av, cho, R, name):
    """
    Estimates a mixed logit (ML) panel data model using Biogeme.

    Args:
        df (pandas.DataFrame): The dataset containing the panel data.
        V (dict): A dictionary containing the utility functions for each alternative.
        av (dict): A dictionary indicating the availability of each alternative.
        cho (pandas.Series): A series containing the alternatives that are available.
        R (int): The number of Monte Carlo draws for simulation.
        name (str): The name of the model.

    Returns:
        pandas.DataFrame: A DataFrame containing the estimated parameters.

    Example:
        >>> results = MLpanelest(data, V, av, choice, 1000, "ML_Panel_Model")
        >>> print(results)
"""
    obslogprob = models.logit(V,  av, cho)
    condprobIndiv = PanelLikelihoodTrajectory(obslogprob)
    logprob = log(MonteCarlo(condprobIndiv))
    logger = msg.bioMessage() 
    logger.setDetailed()  
    biogeme = bio.BIOGEME(df, logprob, numberOfDraws=R)
    biogeme.modelName = name
    results = biogeme.estimate()
    p = results.getEstimatedParameters()
    return p

    
    
