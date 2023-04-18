import pandas as pd
import math
# import numpy as np

def mode_params(df, mode):
    df = df.set_index('Unnamed: 0')

    if mode == 'car':
        btime = df.loc["BETA_CARTIME", "Value"]
        bcost = df.loc["BETA_CARCOST", "Value"]
        bsafe = df.loc["BETA_CARPSAFE", "Value"]
    elif mode == 'ebike':
        btime = df.loc["BETA_EBIKETIME", "Value"]
        bcost = df.loc["BETA_EBIKECOST", "Value"]
        bsafe = df.loc["BETA_EBIKEPSAFE", "Value"]
    elif mode == 'escooter':
        btime = df.loc["BETA_ESCOOTIME", "Value"]
        bcost = df.loc["BETA_ESCOOTCOST", "Value"]
        bsafe = df.loc["BETA_ESCOOTPSAFE", "Value"]
    elif mode == 'walk':
        btime = df.loc["BETA_WALKTIME", "Value"]
        bcost = 0
        bsafe = df.loc["BETA_WALKPSAFE", "Value"]
    # print('Beta of travel time:', btime)
    return btime, bcost, bsafe

def prin_res(vot, vos1, vos2, mode):
    print('The value of travel time of', mode, ' is: ', vot,' euros/h')
    print('The value of safety of', mode, ' is: ', vos1, ' h/level')
    print('Or the value of safety of', mode, ' is: ', vos2, 'km/level') # fix fix fix here
    
def bin_model_coeff(vot, vos1, mode, speed, dcost):
    btime = -6.0
    if math.isinf(vot): bcost = 0
    else: bcost = vot/btime
    bpsafe = vos1 * btime
    d = {'param':['speed', 'dcost', 'btime', 'bcost', 'bpsafe'],
         mode : [speed, dcost, btime, bcost, bpsafe]}
    df = pd.DataFrame(data = d).set_index('param')
    return df

def opp_cost_calc(df, mode, speed, dcost):
    # mode = input("Select mode: car, ebike, escooter, walk?")
    vot = (mode_params(df, mode)[0]/mode_params(df, mode)[1])*60
    vos1 = (mode_params(df, mode)[2]/mode_params(df, mode)[0])/60
    vos2 = vos1 * speed
    prin_res(vot, vos1, vos2, mode)
    # preparation of parameters for the routing model
    rparam = bin_model_coeff(vot, vos1, mode, speed, dcost)
    return rparam