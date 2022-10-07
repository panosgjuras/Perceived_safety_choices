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
from biogeme.expressions import Beta, DefineVariable, log


#current_dir = os.path.dirname(os.path.realpath(__file__))
# os.chdir('C:/Users/panos/Desktop/github_tzouras/Perceived_safety_choices')
# data = pd.read_csv('datasets/choice_dataset_perceived_choices.csv',',')
# data.describe()

# database = db.Database('Perceived&choices', data.drop(columns = ['scenario','choice']).dropna()) # create a dataset, whithout nan
# database.getSampleSize()

# globals().update(database.variables) # globalize database variables, still warnings!!

# EBIKETIME = DefineVariable('EBIKETIME', acttime, database) # new time variables based on the difference among modes
# ESCOOTIME = DefineVariable('ESCOOTTIME', (20/15) * acttime, database) # new time variables based on the difference among modes
# WALKTIME = DefineVariable('WALKTIME',  (20/5) * acttime, database) # new time variables based on the difference among modes

def sel_model(model_id):
    ASC_CAR = Beta('ASC_CAR', 0, None, None, 0)
    BETA_CARTIME = Beta('BETA_CARTIME', 0, None, None, 0)
    BETA_CARCOST = Beta('BETA_CARCOST', 0, None, None, 0)

    if model_id == 1:  # model test 1 - MNL
        # define beta variables and constants, set entry values
        ASC_WALK = Beta('ASC_WALK', 0, None, None, 0)
        ASC_EBIKE = Beta('ASC_EBIKE', 0, None, None, 0)
        ASC_ESCOOT = Beta('ASC_ESCOOT', 0, None, None, 0)
        # BETA_ACTTIME = Beta('Beta_acttime',0, None, None,0)
        BETA_ACTTIME_EBIKE = Beta('BETA_EBIKETIME', 0, None, None, 0)
        BETA_ACTTIME_ESCOOT = Beta('BETA_ESCOOTIME', 0, None, None, 0)
        BETA_ACTTIME_WALK = Beta('BETA_WALKTIME', 0, None, None, 0)
        BETA_EBIKECOST = Beta('BETA_EBIKECOST', 0, None, None, 0)
        BETA_ESCOOTCOST = Beta('BETA_ESCOOTCOST', 0, None, None, 0)
        BETA_CARPSAFE = Beta('BETA_CARPSAFE', 0, None, None, 0)
        BETA_EBIKEPSAFE = Beta('BETA_EBIKEPSAFE', 0, None, None, 0)
        BETA_ESCOOTPSAFE = Beta('BETA_ESCOOTPSAFE', 0, None, None, 0)
        BETA_WALKPSAFE = Beta('BETA_WALKPSAFE', 0, None, None, 0)
        # UTILITY FUNCTIONS
        V1 = BETA_CARTIME * cartime + BETA_CARCOST * carcost + BETA_CARPSAFE * CARPSAFE
        V2 = ASC_EBIKE + BETA_ACTTIME_EBIKE * EBIKETIME + \
            BETA_EBIKECOST * ebikecost + BETA_EBIKEPSAFE * EBIKEPSAFE
        V3 = ASC_ESCOOT + BETA_ACTTIME_ESCOOT * ESCOOTIME + \
            BETA_ESCOOTCOST * escootcost + BETA_ESCOOTPSAFE * ESCOOTPSAFE
        V4 = ASC_WALK + BETA_ACTTIME_WALK * WALKTIME + BETA_WALKPSAFE * WALKPSAFE
        # connect alternative choices with defined utility functions
        V = {4: V1, 3: V2, 2: V3, 1: V4}
        av = {1: 1, 2: 1, 3: 1, 4: 1}  # availability of modes
        cho = intchoice*1  # where is the choice set?

    elif model_id == 2:  # model test 2 - binary logit

        BETA_ACTTIME = Beta('Beta_acttime', 0, None, None, 0)

        BETA_ESCOOTPSAFE = Beta('Beta_escootpsafe', 0, None, None, 0)
        BETA_ESCOOTCOST = Beta('Beta_escootcost', 0, None, None, 0)
        ASC_ALL = Beta('ASC_ALL', 0, None, None, 0)
        BETA_WALKPSAFE = Beta('Beta_walkpsafe', 0, None, None, 0)

        V3 = BETA_ACTTIME * ESCOOTIME + BETA_ESCOOTCOST * \
            escootcost + BETA_ESCOOTPSAFE * escootpsafe
        V4 = 0
        cho = binchoice3*1
        V = {1: V3, 0: V4}
        av = {1: 1, 0: 1}

    elif model_id == 3:  # model test 3 - Same as 1, with gender controls
        ASC_WALK = Beta('ASC_WALK', 0, None, None, 0)
        ASC_EBIKE = Beta('ASC_EBIKE', 0, None, None, 0)
        ASC_ESCOOT = Beta('ASC_ESCOOT', 0, None, None, 0)
        BETA_ACTTIME_EBIKE = Beta('BETA_EBIKETIME', 0, None, None, 0)
        BETA_ACTTIME_ESCOOT = Beta('BETA_ESCOOTIME', 0, None, None, 0)
        BETA_ACTTIME_WALK = Beta('BETA_WALKTIME', 0, None, None, 0)
        BETA_EBIKECOST = Beta('BETA_EBIKECOST', 0, None, None, 0)
        BETA_ESCOOTCOST = Beta('BETA_ESCOOTCOST', 0, None, None, 0)
        BETA_CARPSAFE = Beta('BETA_CARPSAFE', 0, None, None, 0)
        BETA_EBIKEPSAFE = Beta('BETA_EBIKEPSAFE', 0, None, None, 0)
        BETA_ESCOOTPSAFE = Beta('BETA_ESCOOTPSAFE', 0, None, None, 0)
        BETA_WALKPSAFE = Beta('BETA_WALKPSAFE', 0, None, None, 0)
        BETA_EBIKEPSAFE_FEMALE = Beta(
            'BETA_EBIKEPSAFE_FEMALE', 0, None, None, 0)
        BETA_ESCOOTSAFE_FEMALE = Beta(
            'BETA_ESCOOTSAFE_FEMALE', 0, None, None, 0)
        BETA_CARPSAFE_FEMALE = Beta('BETA_CARPSAFE_FEMALE', 0, None, None, 0)
        BETA_WALKPSAFE_FEMALE = Beta('BETA_WALKPSAFE_FEMALE', 0, None, None, 0)
        # UTILITY FUNCTIONS
        V1 = BETA_CARTIME * cartime + BETA_CARCOST * carcost + BETA_CARPSAFE * CARPSAFE + \
            BETA_CARPSAFE_FEMALE * CARPSAFE * ISFEMALE
        V2 = ASC_EBIKE + BETA_ACTTIME_EBIKE * EBIKETIME + \
            BETA_EBIKECOST * ebikecost + BETA_EBIKEPSAFE * EBIKEPSAFE + \
            BETA_EBIKEPSAFE_FEMALE * EBIKEPSAFE * ISFEMALE
        V3 = ASC_ESCOOT + BETA_ACTTIME_ESCOOT * ESCOOTIME + \
            BETA_ESCOOTCOST * escootcost + BETA_ESCOOTPSAFE * ESCOOTPSAFE + \
            BETA_ESCOOTSAFE_FEMALE * ESCOOTPSAFE * ISFEMALE
        V4 = ASC_WALK + BETA_ACTTIME_WALK * WALKTIME + BETA_WALKPSAFE * WALKPSAFE + \
            BETA_WALKPSAFE_FEMALE * WALKPSAFE * ISFEMALE
        # connect alternative choices with defined utility functions
        V = {4: V1, 3: V2, 2: V3, 1: V4}
        av = {1: 1, 2: 1, 3: 1, 4: 1}  # availability of modes
        cho = intchoice*1  # where is the choice set?

    else:
        raise ValueError('Please provide a valid model ID.')

    return V, av, cho

# Logit model
# logprob = models.loglogit(sel_model(1)[0], sel_model(1)[1], sel_model(1)[2]) # import utilities in loglogit
# logger = msg.bioMessage()
# logger.setSilent() # not sure that this is working, but ok
# biogeme = bio.BIOGEME(database,logprob) # estimate biogeme based on the defined database

# biogeme.modelName = "MNL_ex1" # how the file is gonna saved, it creates and HTML FILE
# results = biogeme.estimate()
# p=results.getEstimatedParameters()


def model_estimation(
        df: pd.DataFrame,
        typ: str = 'MNL',
        name: str = 'MNL_ex1',
        model_id: int = 1) -> pd.DataFrame:
    """
    Estimate a mode choice model with Biogeme

    :param df: The choice dataset
    :param typ: Type of model (ie MNL)
    :param name: The name of the model.
    :param model_id: Chooses one of the model formulations in the sel_model function.
    """

    database = db.Database('Perceived&choices', df.drop(columns=[
        'scenario', 'choice', 'age', 'education', 'employment', 'income',
        # 'car_own', 'moto_own', 'cycle_own', 'escoot_own',
        'bike_frequency', 'escooter_frequency', 'PT_frequency',
        'metro_frequency', 'young']).dropna())  # create a dataset, whithout nan
    database.getSampleSize()

    # globalize database variables, still warnings!!
    globals().update(database.variables)

    # new time variables based on the difference among modes
    EBIKETIME = database.DefineVariable('EBIKETIME', acttime)
    # new time variables based on the difference among modes
    ESCOOTIME = database.DefineVariable('ESCOOTIME', (20/15) * acttime)
    # new time variables based on the difference among modes
    WALKTIME = database.DefineVariable('WALKTIME',  (20/5) * acttime)
    CARPSAFE = database.DefineVariable('CARPSAFE',  carpsafe - 4)
    EBIKEPSAFE = database.DefineVariable('EBIKEPSAFE',  ebikepsafe - 4)
    ESCOOTPSAFE = database.DefineVariable('ESCOOTPSAFE',  escootpsafe - 4)
    WALKPSAFE = database.DefineVariable('WALKPSAFE',  walkpsafe - 4)
    ISFEMALE = database.DefineVariable('ISFEMALE',  gender == 0)

    # globalize database variables, still warnings!!
    globals().update(database.variables)

    if typ == 'MNL':
        V, av, cho = sel_model(model_id=model_id)
        logprob = models.loglogit(V, av, cho)  # import utilities in loglogit
        # logger = msg.bioMessage()
        # logger.setSilent() # not sure that this is working, but ok
        # estimate biogeme based on the defined database
        biogeme = bio.BIOGEME(database, logprob)
        biogeme.calculateNullLoglikelihood(av)
    else:
        raise ValueError(f'Model type {typ} is not supported.')

    biogeme.modelName = name
    results = biogeme.estimate()
    p = results.getEstimatedParameters()

    return p


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Activity synthesis')
    parser.add_argument('--mode_type', required=False,
                        default='MNL', help='Model type')
    parser.add_argument('--model_name', required=False,
                        default='MNL_ex1', help='Model name')
    parser.add_argument('--model_id', required=False,
                        default='1', help='Model ID')

    args = parser.parse_args()
    model_id = int(args.model_id)

    root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    data = pd.read_csv(os.path.join(root_dir, 'datasets',
                       'choice_dataset_perceived_choices.csv'), sep=',')
    model_estimation(data, typ='MNL', name='MNL_gender', model_id=model_id)
