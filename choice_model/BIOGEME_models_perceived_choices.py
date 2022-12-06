"""
@author: ptzouras
National Technical University of Athens
Research project: SIM4MTRAN
"""

import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import os
import numpy as np
import biogeme.messaging as msg
from biogeme import models
from biogeme.expressions import (Beta, 
                                 DefineVariable, 
                                 log, 
                                 bioMultSum,
                                 bioDraws,
                                 MonteCarlo,
                                 exp,
                                 PanelLikelihoodTrajectory)

current_dir = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv('data_process/datasets/choice_dataset_perceived_choices.csv',',')
df.pid = df.pid/100
df = df.drop(columns = ['scenario','choice', 'gender', 'age', 'education', 'employment',
    'income', 'car_own', 'moto_own', 'cycle_own', 'escoot_own',
    'bike_frequency', 'escooter_frequency', 'PT_frequency',
    'metro_frequency', 'young'])
database = db.Database('Perceived&choices', df.dropna()) # create a dataset, whithout nan


globals().update(database.variables) # globalize database variables, still warnings!!

database.panel('pid')
# DefineVariable(name, expression, database)

def dat_defin(x, NAME, expr, database):
    if x == 1:
        var = DefineVariable(NAME, expr, database)
    if x == 2:
        var = database.DefineVariable(NAME, expr)
    return var

typ = 1
CARTIME = dat_defin(typ,'CARTIME',cartime,database)
CARCOST = dat_defin(typ,'CARCOST',carcost,database)
CARPSAFE = dat_defin(typ,'CARPSAFE',carpsafe - 4,database)

EBIKETIME = dat_defin(typ,'EBIKETIME',acttime,database) # new time variables based on the difference among modes
EBIKECOST = dat_defin(typ,'EBIKECOST',ebikecost,database)
EBIKEPSAFE = dat_defin(typ,'EBIKEPSAFE',ebikepsafe - 4,database)
 
ESCOOTIME = dat_defin(typ,'ESCOOTIME', (20/15) * acttime,database) # new time variables based on the difference among modes
ESCOOTCOST = dat_defin(typ,'ESCOOTCOST', escootcost,database) # new time variables based on the difference among modes
ESCOOTPSAFE = dat_defin(typ,'ESCOOTPSAFE', escootpsafe - 4,database)

WALKTIME = dat_defin(typ,'WALKTIME',  (20/5) * acttime,database) # new time variables based on the difference among modes
WALKPSAFE = dat_defin(typ,'WALKPSAFE',walkpsafe - 4,database)

globals().update(database.variables) # globalize database variables, still warnings!!

def set_utils(x, randb):
    ASC_CAR = Beta('ASC_CAR', 0, -1000, 1000, 0)
    BETA_CARTIME = Beta('BETA_CARTIME',0, -1000, 1000, 0)
    BETA_CARCOST = Beta('BETA_CARCOST',0, -1000, 1000, 0) 
    BETA_CARPSAFE = Beta('BETA_CARPSAFE',0, -1000, 1000, 0)
    
    ASC_EBIKE = Beta('ASC_EBIKE', 0, -1000, 1000, 0)
    BETA_EBIKETIME = Beta('BETA_EBIKETIME',0, -1000, 1000, 0)
    BETA_EBIKECOST = Beta('BETA_EBIKECOST',0, -1000, 1000, 0)
    BETA_EBIKEPSAFE = Beta('BETA_EBIKEPSAFE',0, -1000, 1000, 0)
    
    ASC_ESCOOT = Beta('ASC_ESCOOT', 0, -1000, 1000, 0)
    BETA_ESCOOTIME = Beta('BETA_ESCOOTIME',0, -1000, 1000, 0)
    BETA_ESCOOTCOST = Beta('BETA_ESCOOTCOST',0, -1000, 1000, 0)
    BETA_ESCOOTPSAFE = Beta('BETA_ESCOOTPSAFE',0, -1000, 1000, 0)
    
    ASC_WALK = Beta('ASC_WALK', 0, -1000, 1000, 0)
    BETA_WALKPSAFE = Beta('BETA_WALKPSAFE',0, -1000, 1000, 0)
    BETA_WALKCOST = Beta('BETA_WALKTIME',0, -1000, 1000, 0)
    BETA_WALKTIME = Beta('BETA_WALKTIME',0, -1000, 1000, 0)
    
    if randb == True:
        BETA_CARTIME_RND = BETA_CARTIME + Beta('SIGMA_CARTIME', 0, -1000, 1000, 0) * bioDraws('BETA_CARTIME_RND', 'NORMAL_HALTON2')
        

    if x == 'MNL_1':
        V1 = BETA_CARTIME_RND * CARTIME + BETA_CARCOST * CARCOST + BETA_CARPSAFE * CARPSAFE
        V2 = ASC_EBIKE + BETA_EBIKETIME * EBIKETIME + BETA_EBIKECOST * EBIKECOST + BETA_EBIKEPSAFE * EBIKEPSAFE
        V3 = ASC_ESCOOT + BETA_ESCOOTIME * ESCOOTIME + BETA_ESCOOTCOST * ESCOOTCOST + BETA_ESCOOTPSAFE * ESCOOTPSAFE
        V4 = ASC_WALK + BETA_WALKTIME * WALKTIME + BETA_WALKPSAFE * WALKPSAFE
        V = {4: V1, 3: V2, 2: V3, 1:V4}
    elif x == 'bin_car':
        V1 = ASC_CAR + BETA_CARTIME_RND * CARTIME + BETA_CARCOST * CARCOST + BETA_CARPSAFE * CARPSAFE
        V2 = 0
        V = {1: V1, 0: V2}
    elif x == 'bin_ebike':
        V1 = ASC_EBIKE + BETA_EBIKETIME * EBIKETIME + BETA_EBIKECOST * EBIKECOST + BETA_EBIKEPSAFE * EBIKEPSAFE
        V2 = 0
        V = {1: V1, 0: V2}
    elif x == 'bin_escoot':
        V1 = ASC_ESCOOT + BETA_ESCOOTIME * ESCOOTIME + BETA_ESCOOTCOST * ESCOOTCOST + BETA_ESCOOTPSAFE * ESCOOTPSAFE
        V2 = 0
        V = {1: V1, 0: V2}
    elif x == 'bin_walk':
        V1 = ASC_WALK + BETA_WALKTIME * WALKTIME + BETA_WALKPSAFE * WALKPSAFE
        V2 = 0
        V = {1: V1, 0: V2}    
    else: 
        V1 = 0
        V2 = 0
        V3 = 0
        V4 = 0
        V = {4: V1, 3: V2, 2: V3, 1:V4}
    
    return V

def avail(x):
    if x == 'MNL_1': av = {1:1, 2:1, 3:1, 4:1}
    elif x == 'bin_car': av = {0:1, 1:1}
    elif x == 'bin_ebike': av = {0:1, 1:1}
    elif x == 'bin_escoot': av = {0:1, 1:1}
    else: av = {1:1, 2:1, 3:1, 4:1}
    return av

def MNLest(df, V, av, cho, name): # !!!!!!!!!!!!!!!!!!!!!!! for packaging
    logprob = models.loglogit(V, av, cho) # import utilities in loglogit
    # logger = msg.bioMessage()
    # logger.setSilent() # not sure that this is working, but ok
    biogeme = bio.BIOGEME(df, logprob) # estimate biogeme based on the defined database
    biogeme.calculateNullLoglikelihood(av)
    biogeme.modelName = name
    results = biogeme.estimate()
    p = results.getEstimatedParameters()
    return p

# x = "MNL_1" # Multinomial logit of modes choice including all transport modes
CHOICE = dat_defin(typ, 'CHOICE',  intchoice, database)
# model0 = MNLest(database, set_utils(x), avail(x), CHOICE, "MNL_mode_choice")

x = "bin_car" # Binary logit including car only
CHOICE1 = dat_defin(typ, 'CHOICE1',  binchoice1, database)
# model1 = MNLest(database, set_utils(x), avail(x), CHOICE1, "Binary_logit_car")

# x = "bin_ebike" # Binary logit including car only
# CHOICE2 = dat_defin(typ, 'CHOICE2',  binchoice2, database)
# model2 = MNLest(database, set_utils(x), avail(x), CHOICE2, "Binary_logit_ebike")

# x = "bin_escoot" # Binary logit including car only
# CHOICE3 = dat_defin(typ, 'CHOICE3',  binchoice3, database)
# model3 = MNLest(database, set_utils(x), avail(x), CHOICE3, "Binary_logit_escoot")

# x = "bin_walk" # Binary logit including car only
# CHOICE4 = dat_defin(typ, 'CHOICE4',  binchoice4, database)
# model4 = MNLest(database, set_utils(x), avail(x), CHOICE4, "Binary_logit_walk")

x = "MNL_1"
obslogprob = models.loglogit(set_utils(x, True),  avail(x), CHOICE)
condprobIndiv = PanelLikelihoodTrajectory(obslogprob)
logprob = log(MonteCarlo(condprobIndiv))
logger = msg.bioMessage() 
logger.setDetailed()  
biogeme = bio.BIOGEME(database, logprob, numberOfDraws=5000)
biogeme.modelName = 'MNL_mode_choice'
results = biogeme.estimate()
print('Number of draws: 5000')
for c in results.columns:
    print(f'{c}:\t{results.loc[0,c]}')
    
pandasResults = results.getEstimatedParameters()
print(pandasResults)   

