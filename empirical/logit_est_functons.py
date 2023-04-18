import os
import pandas as pd
import biogeme.messaging as msg
import biogeme.biogeme as bio
from biogeme import models
import biogeme.results as res
from biogeme.expressions import (DefineVariable,
                                 PanelLikelihoodTrajectory,
                                 MonteCarlo, log)

def MNLest(df, V, av, cho, name):
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

    
    
