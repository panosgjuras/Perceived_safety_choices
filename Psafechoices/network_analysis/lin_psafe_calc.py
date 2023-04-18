"""
Perceived safety estimation

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def inf_match(s_inf): # functions that codes infrastructure, 
    # it may need modification if dummy coding to describe non-linearities among categories
    inf=999 # 999, if not matched
    if s_inf=='1: Urban road with sidewalk less than 1.5 m wide': inf=1 
    # standarized categories given to the user in drop-down menu in GIS
    elif s_inf=='2: Urban road with sidewalk more than 1.5 m wide': inf=2
    elif s_inf=='3: Urban road with cycle lane': inf=3
    elif s_inf=='4: Shared space': inf=4
    return inf

def pav_match(s_pav): # functions that codes pavement variable 
    pav=999
    if s_pav=='0: bad condition': pav=0
    # standarized coding - binary variable so one beta parameter
    elif s_pav=='1: good condition': pav=1
    return pav

def obst_match(s_obst): # function that codes obstacles
    obst=999
    if s_obst=='0: yes obstacles': obst=0
    # standarized coding - binary variable so one beta parameter
    elif s_obst=='1: no obstacles': obst=1
    return obst

def cross_match(s_cross): # function that codes pedestrian crossing
    cross = 999
    # it may need modification if dummy coding to describe non-linearities among categories
    if s_cross=='0: without pedestrian crossings': cross = 0
    elif s_cross=='1: with pedestrian crossings not controlled by traffic lights': cross = 1
    elif s_cross=='2: with pedestrian crossing controlled by traffic lights': cross = 2
    return cross

def fun_psafe(links, mode, cf):
    # beta parameters that are valid for one mode only
    # a different approach is to give these parameters from a csv
    # but maybe it is not necessary, if the user cannot provide these parameters
    # so here we have default parameters
    k0 = cf.loc['kappa.0', mode]
    k1 = cf.loc['kappa.1', mode]
    k2 = cf.loc['kappa.2', mode]
    k3 = cf.loc['kappa.3', mode]
    k4 = cf.loc['kappa.4', mode]
    k5 = cf.loc['kappa.5', mode]
    
    b_inf1 = cf.loc['type1', mode]
    b_inf2 = cf.loc['type2', mode]
    b_inf4 = cf.loc['type4', mode]
    
    b_cross1 = cf.loc['cross1', mode]
    b_cross2 = cf.loc['cross2', mode]
    
    b_pav = cf.loc['pav', mode]
    b_obst = cf.loc['obst', mode]
    
    psafe=pd.Series(999, index=np.arange(len(links))) # 999, if mode and x are unmatched
    psafe_l=pd.Series(999, index=np.arange(len(links))) # 999, if mode and x are unmatched 
    
    for i in range(0,len(links)):
        # coding categorical variables based on the developed functions
        inf = inf_match(links.inf.iloc[i])
        inf1 = np.where(inf==1, 1, 0)
        inf2 = np.where(inf==2, 1, 0)
        # inf3 = np.where(inf==3, 1, 0)
        inf4 = np.where(inf==4, 1, 0)
        pav = pav_match(links.pav.iloc[i])
        obst = obst_match(links.obst.iloc[i])
        cross =cross_match(links.cross.iloc[i])
        cross1 = np.where(cross==1, 1, 0)
        cross2 = np.where(cross==2, 1, 0)       
        
        if inf!=999 and pav!=999 and obst!=999 and cross!=999:
            psafe.iloc[i]=b_inf1 * inf1 + b_inf2 * inf2 + b_inf4 * inf4 + b_pav*pav + b_cross1 * cross1 + b_cross2*cross2 + b_obst*obst
            
            if psafe.iloc[i]!=999:
              # estime perceived safety level based on the estimated latent variable
              if psafe.iloc[i]<=k0:
                 psafe_l.iloc[i]=1
              elif psafe.iloc[i]<=k1:
                 psafe_l.iloc[i]=2
              elif psafe.iloc[i]<=k2:
                 psafe_l.iloc[i]=3
              elif psafe.iloc[i]<=k3:
                 psafe_l.iloc[i]=4
              elif psafe.iloc[i]<=k4:
                 psafe_l.iloc[i]=5
              elif psafe.iloc[i]<=k5:
                 psafe_l.iloc[i]=6
              else:
                psafe_l.iloc[i]=7
           
    return psafe, psafe_l

def lin_psafe(lin, cf):
    [lin['car_psafe'], lin['car_psafe_l']] = fun_psafe(lin, 'car', cf)
    [lin['ebike_psafe'], lin['ebike_psafe_l']] = fun_psafe(lin,'ebike', cf)
    [lin['escoot_psafe'], lin['escoot_psafe_l']]=fun_psafe(lin,'escoot', cf)
    [lin['walk_psafe'], lin['walk_psafe_l']]=fun_psafe(lin,'walk', cf)
    return lin