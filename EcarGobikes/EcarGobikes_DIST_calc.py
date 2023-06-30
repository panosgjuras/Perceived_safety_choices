import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import math
import numpy as np
import pandas as pd

import os
import matplotlib.pyplot as plt

def slodist(df, typ = 'avgslo'): 
    # this function estimates the slope distance based on the slope
    # in percentage that is provided
    # typ = 'avgslo' -> based on the average slope
    # typ = 'maxslo' -> based on the maximum slope
    df["slodist"] = df.sdist

    for i in range(0, len(df)):
        run = df.loc[i, "sdist"]
        
        if typ == 'maxslo': slop = df.loc[i, "wavg_maxslope"]
        else: slop = df.loc[i, "wavg_avgslope"]
        
        rise = run * slop/100
        
        df.loc[i, 'slodist'] = math.sqrt(run**2 + rise**2)

    return df

def dfcor(x): # it correct the 999999 values with zero
    x = x.replace({999999: 0})
    return x

def psnegcheck(x, k = 0): # it updates the negative values
# considering the penalty
# to do so it considers the minimum value
# if it is negative, then it saves a constant 
# this constant is added in all the links
# it like changing the scale of the network
    if min(x) < 0:
        c = abs(min(x) + k)
    return c

def setdist(df, typ = 'hor', vos = 750, fun = 'linear', upd = 'no', k = 0):
    
    # options
    # typ = 'hor' -> based on the horizontal distance, calculate slope distance
    # typ = 'avgslo' -> based on the average slope, calculate slope distance
    # typ = 'maxslo' -> based on the maximum slope, calculate slope distance
    # typ = 'safe' -> extend or shorten the horizontal distance based on the safety score and vos
    # typ = 'combo' -> extend or shorten the slope distance based on the safety score and vos
    # fun = 'linear' -> the penalty is a linear function of psafe score per link
    # fun = 'exponential -> the penalty is an exponential function of psafe score per link
    # upd = 'no' -> no check for negative distances, due to the penalty
    # upd = 'min' -> negative distance are become positive based on the minimum value
    # k = 0 -> this means that the minimum distance is equalized with zero later in optimization
    
    if typ == 'hor': df['hordist'] = df["sdist"]

    if typ == 'avgslo': 
        df.wavg_avgslope = dfcor(df.wavg_avgslope)
        t = 'avgslodist'
        df[t] = slodist(df, typ).slodist
        
    if typ == 'maxslo':
        df.wavg_avgslope = dfcor(df.wavg_maxslope)
        t = 'maxslodist'
        df[t] = slodist(df, typ).slodist
    
    if typ == 'safe': 
        df.wavg_psafe = dfcor(df.wavg_psafe)
        if fun == 'linear': 
            t = 'safedist_lin_' + str(vos)
            df[t] = df.sdist - df.wavg_psafe * vos
        elif fun == 'exponential': 
            newvar = [math.exp(-x) * vos for x in df.wavg_psafe]
            t = 'safedist_exp_' + str(vos)
            df[t] = df.sdist + newvar
        else: 
            t = 'safedist_' + str(vos)
            df[t] = 0
    
    if typ == 'combo': 
        df.wavg_avgslope = dfcor(df.wavg_avgslope)
        df.wavg_psafe = dfcor(df.wavg_psafe)
        if fun == 'linear': 
            t = 'combodist_lin_' + str(vos)
            df[t] = df.avgslodist - df.wavg_psafe * vos
        elif fun == 'exponential': 
            newvar = [math.exp(-x) * vos for x in df.wavg_psafe]
            t = 'combodist_exp_' + str(vos)
            df[t] = df.avgslodist + newvar
        else: 
            t = 'combodist_' + str(vos)
            df[t] = 0
    
    if upd == 'min': 
        
        mask = df[t] != 0

        df.loc[mask, t + '_' + upd] = df.loc[mask, t] + psnegcheck(df[t])

        df[t + '_' + upd].fillna(value=0, inplace=True)
        
    else: df[t] = df[t]
    
    df = df.drop('slodist', axis=1)
    return df

def checkPlotDist(df, typ, vos = 750, fun = "linear", upd = 'no'):
    
    # plot scatter to check the contribution of the penalty
    # red dots correspond to negative penalty, means that we shorten the link more safe
    # blue dots correspond to positive penatly = bigger link
    
    # annotated dots correspond to negative distance (with penalty consideration)
    
    if upd == 'min': up = '_min'
    else: up = ''
    
    if fun == 'linear': 
        label = "Linear penalty"
        lal = "lin_"
    elif fun == 'exponential':
        label = "Exponential penalty"
        lal = "exp_"
    else:
        label = "LNo penalty"
        lal = ""
    
    c = df['sdist']
    ids = df['pid']
    x = df['avgslodist']
    y = df[ typ +  'dist_' + lal + str(vos) + up] - c
    colors = ['royalblue' if value >= 0 else 'tomato' for value in y]
    plt.figure(figsize = (8, 6))
    plt.style.use('default')
    plt.scatter(x, y, 5, c=colors)
    plt.xlabel('Slope distance in m')
    plt.ylabel('Penalty in m with VOS =' + str(vos))
    plt.title(label)
    
    for i, j, k, l in zip(ids, x, y, c):
        if k + l  < 0:
            plt.annotate(str(i), (j, k), textcoords="offset points", xytext=(0, 10), 
                         ha='center', fontsize = 9)
    trending_line_x = [x.min(), x.max()]
    trending_line_y = [y.mean(), y.mean()]
    plt.plot(trending_line_x, trending_line_y, color='black', linestyle='--', linewidth=3)
    
    slope, intercept = np.polyfit(x, y, 1)
    residuals = y - (slope * x + intercept)
    ss_residual = np.sum(residuals ** 2)
    ss_total = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - (ss_residual / ss_total)

    annotation_text = f'R-squared = {r_squared:.4f}'
    plt.annotate(annotation_text, (0.05, 0.9), xycoords='axes fraction', fontsize=12, weight = 'bold')
    
    plt.show()
    return plt

# RUN THIS THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
root_dir = os.path.dirname(os.path.realpath(__file__))
ttt = pd.read_csv(os.path.join(root_dir, 'NETfile ', "net_file_ATHENS.csv"))
ttt = ttt[ttt['from1'] != ttt['to1']]
ttt.reset_index(drop = True, inplace = True)

distance = setdist(ttt, 'avgslo') # creates a new column = avgslodist
# distance = setdist(ttt, 'maxslo') # creates a new column = maxslodist

distance = setdist(ttt, 'combo', vos = 600, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 600, fun = 'linear', upd = 'min')

distance = setdist(ttt, 'combo', vos = 1200, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 1200, fun = 'linear', upd = 'min')

distance = setdist(ttt, 'combo', vos = 1800, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 1800, fun = 'linear', upd = 'min')

distance = setdist(ttt, 'combo', vos = 2400, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 2400, fun = 'linear', upd = 'min')

distance = setdist(ttt, 'combo', vos = 3000, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 3000, fun = 'linear', upd = 'min')

distance = setdist(ttt, 'combo', vos = 3600, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 3600, fun = 'linear', upd = 'min')

distance = setdist(ttt, 'combo', vos = 4200, fun = 'linear', upd = 'min')
checkPlotDist(distance, 'combo', vos = 4200, fun = 'linear', upd = 'min')

# you will have a new set of columns...
# distance.columns
# Out[222]: 
# Index(['pid', 'from1', 'to1', 'path', 'sdist', 'sum_psafe', 'sum_avgslope',
#       'sum_maxslope', 'wavg_psafe', 'wavg_avgslope', 'wavg_maxslope',
#       'avgslodist', 'combodist_lin_600', 'combodist_lin_600_min',
#       'combodist_lin_1200', 'combodist_lin_1200_min', 'combodist_lin_1800',
#       'combodist_lin_1800_min', 'combodist_lin_2400',
#       'combodist_lin_2400_min', 'combodist_lin_3000',
#       'combodist_lin_3000_min', 'combodist_lin_3600',
#       'combodist_lin_3600_min', 'combodist_lin_4200',
#       'combodist_lin_4200_min'],
#      dtype='object')
#
# pid : the id of the link
# from1: from node i
# to1: to node j
# path: set of segments
# sdist: horizontal distance
# sum_psafe: total psafe - 4
# sum_avgslope: total slope, adding all the avg. slopes per link, positive negative
# sum_maxslope: total slope, adding all the max slopes per link, positive negative
# wavg_psafe: the weighted average of perceived safety, weigths = length of each segment
# wavg_avgslope: the weighted average of avg. slopes, weights = length of each segment
# wavg_maxslope: the weighted average of max slopes, weights = length of each segment
# avgslopdist: average slope distance in meters using the wavg_avgslope
# combodist_lin_600: combo distance (slope dist + penalty); penalty uses linear function, vos is equal to 600
# combodist_lin_600_min: the same but distances have been updated based on the min(x), + min(x)
# so no negative.

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




