import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import os
# import numpy as np
import biogeme.messaging as msg
from biogeme import models
from biogeme.expressions import Beta, DefineVariable, log

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)
data = pd.read_csv('datasets/choice_dataset_perceived_choices.csv',',')
#data.describe()

#def int_choice(df):
#    df['intchoice']= df.choice.replace({'car':4, 'ebike':3, 'escoot':2, 'walk':1}) # BIOGEME does not use categories, it utilizes number for choice
#    df['binchoice1'] = np.where(df.intchoice==4, 1, 0) # create a new choice variable for binary logit
#    df['binchoice2'] = np.where(df.intchoice==3, 1, 0) 
#    df['binchoice3'] = np.where(df.intchoice==2, 1, 0) 
#    df['binchoice4'] = np.where(df.intchoice==1, 1, 0) 
#    return df

database = db.Database('Perceived&choices', data.drop(columns = ['scenario','choice']).dropna()) # create a dataset, whithout nan
database.getSampleSize()

globals().update(database.variables) # globalize database variables, still warnings!!

EBIKETIME = DefineVariable('EBIKETIME', acttime, database) # new time variables based on the difference among modes
ESCOOTIME = DefineVariable('ESCOOTTIME', (20/15) * acttime, database) # new time variables based on the difference among modes
WALKTIME = DefineVariable('WALKTIME',  (20/5) * acttime, database) # new time variables based on the difference among modes

def sel_model(x):
    ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
    BETA_CARTIME = Beta('Beta_cartime',0, None, None,0)
    BETA_CARCOST = Beta('Beta_carcost',0, None, None,0)
    
    if x == 1: # model test 1 - MNL
        # define beta variables and constants, set entry values
        ASC_WALK = Beta('ASC_WALK', 0, None, None, 0)
        BETA_ACTTIME = Beta('Beta_acttime',0, None, None,0)
        BETA_ACTTIME_EBIKE = Beta('Beta_acttime_ebike',0, None, None,0)
        BETA_ACTTIME_ESCOOT = Beta('Beta_acttime_escoot',0, None, None,0)
        BETA_ACTTIME_WALK = Beta('Beta_acttime_walk',0, None, None,0)
        BETA_EBIKECOST = Beta('Beta_ebikecost',0, None, None,0)
        BETA_ESCOOTCOST = Beta('Beta_escootcost',0, None, None,0)
        BETA_CARPSAFE = Beta('Beta_carpsafe',0, None, None,0)
        BETA_EBIKEPSAFE = Beta('Beta_ebikepsafe',0, None, None,0)
        BETA_ESCOOTPSAFE = Beta('Beta_escootpsafe',0, None, None,0)
        BETA_WALKPSAFE = Beta('Beta_walkpsafe',0, None, None,0)
        # UTILITY FUNCTIONS
        V1 = ASC_CAR + BETA_CARTIME * cartime + BETA_CARCOST * carcost + BETA_CARPSAFE * carpsafe
        V2 = BETA_ACTTIME_EBIKE * EBIKETIME + BETA_EBIKECOST * ebikecost + BETA_EBIKEPSAFE * ebikepsafe
        V3 = BETA_ACTTIME_ESCOOT * ESCOOTIME + BETA_ESCOOTCOST * escootcost + BETA_ESCOOTPSAFE * escootpsafe
        V4 = BETA_ACTTIME_WALK * WALKTIME + BETA_WALKPSAFE * walkpsafe
        V = {4: V1, 3: V2, 2: V3, 1:V4} # connect alternative choices with defined utility functions
        av = {1:1, 2:1, 3:1, 4:1} # availability of modes
        cho = intchoice*1 # where is the choice set?
    if x == 2: # model test 2 - binary logit
        
        BETA_ACTTIME = Beta('Beta_acttime',0, None, None,0)
        
        BETA_ESCOOTPSAFE = Beta('Beta_escootpsafe',0, None, None,0)
        BETA_ESCOOTCOST = Beta('Beta_escootcost',0, None, None,0)
        ASC_ALL = Beta('ASC_ALL', 0, None, None, 0)
        BETA_WALKPSAFE = Beta('Beta_walkpsafe',0, None, None,0)

        V3 = BETA_ACTTIME * ESCOOTIME + BETA_ESCOOTCOST * escootcost + BETA_ESCOOTPSAFE * escootpsafe
        V4 = 0
        cho = binchoice3*1
        V = {1: V3, 0: V4} 
        av = {1:1, 0:1}
    
    return V, av, cho

# Logit model        
logprob = models.loglogit(sel_model(1)[0], sel_model(1)[1], sel_model(1)[2]) # import utilities in loglogit
logger = msg.bioMessage()
logger.setSilent() # not sure that this is working, but ok
biogeme = bio.BIOGEME(database,logprob) # estimate biogeme based on the defined database

biogeme.modelName = "MNL_ex1" # how the file is gonna saved, it creates and HTML FILE
results=biogeme.estimate()
p=results.getEstimatedParameters()




