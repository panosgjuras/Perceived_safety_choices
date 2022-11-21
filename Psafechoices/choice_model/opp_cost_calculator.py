import pandas as pd
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
    print('The value of travel time of ', mode, ' is: ', vot,' euros/h')
    print('The value of safety of ', mode, ' is: ', vos1, ' h/level')
    print('Or the value of safety of ', mode, ' is: ', vos2, 'km/level') # fix fix fix here
    
def bin_model_coeff(vot, vos1, mode, speed, dcost):
    btime = -6.0
    bcost = vot/btime
    bpsafe = btime/vos1
    d = {'param':['speed', 'dcost', 'btime', 'bcost', 'bpsafe'],
         mode : [speed, dcost, btime, bcost, bpsafe]}
    df = pd.DataFrame(data = d).set_index('param')
    return df

def opp_cost_calc(df, mode, speed, dcost):
    # mode = input("Select mode: car, ebike, escooter, walk?")
    if mode == 'car':
        # speed = input("Define mean speed of private car in km/h")
        # dcost = input("Define trip cost of private car in euros/km")
        vot = (mode_params(df, mode)[0]/mode_params(df, mode)[1])*60
        vos1 = (mode_params(df, mode)[2]/mode_params(df, mode)[0])/60
        vos2 = mode_params(df, mode)[2]/(dcost * mode_params(df, mode)[1])
        prin_res(vot, vos1, vos2, mode)
    elif mode =='ebike' or mode == 'escooter':
        # speed = input("Define mean speed of the selected mode in km/h")
        # hcost = input("Define trip cost of the micromobility service in euros/h")
        vot = (mode_params(df, mode)[0]/mode_params(df, mode)[1])*60 
        vos1 = (mode_params(df, mode)[2]/mode_params(df, mode)[0])/60
        vos2 = mode_params(df, mode)[2]/(dcost * mode_params(df, mode)[1])
        prin_res(vot, vos1, vos2, mode)
    elif mode == 'walk':
        vot = 0
        vos1 = (mode_params(df, mode)[2]/mode_params(df, mode)[0])/60
        vos2 = 0
        prin_res(vot, vos1, vos2, mode)   
    else: print('false')
    # preparation of parameters for the routing model
    rparam = bin_model_coeff(vot, vos1, mode, speed, dcost)
    return rparam