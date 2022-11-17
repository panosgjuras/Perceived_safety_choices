"""
A network router based on perceived safety
and Dijkstra algorithm

@author: ptzouras
National Technical University of Athens
Research project: SIM4MTRAN
"""

import pandas as pd
import dijkstra as dij
import os

def utils_cal(df, cf, dmin):
    # calclation of the utility based on an alternative utility function
    # Psafe impact is a function of dmin
    # It means that for links longer than dmin psafe has a significant weigth to utility function.....
    df["car_utils"] = - (cf.loc['btime', 'car'] * (df.length/(cf.loc['speed', 'car'] * 1000)) \
        + cf.loc['bcost', 'car'] * (cf.loc['speed', 'car']/(cf.loc['speed', 'car'] * 1000)) * df.length \
        + cf.loc['bpsafe', 'car'] * (df.car_psafe_l - 4) * (df.length/dmin))
    
    df["ebike_utils"] = - (cf.loc['btime', 'ebike'] * (df.length/(cf.loc['speed', 'ebike'] * 1000)) \
        + cf.loc['bcost', 'ebike'] * (cf.loc['speed', 'ebike']/(cf.loc['speed', 'ebike'] * 1000)) * df.length \
        + cf.loc['bpsafe', 'ebike'] * (df.ebike_psafe_l - 4) * (df.length/dmin))
    
    df["escoot_utils"] = - (cf.loc['btime', 'escooter'] * (df.length/(cf.loc['speed', 'escooter'] * 1000)) \
        + cf.loc['bcost', 'escooter'] * (cf.loc['speed', 'escooter']/(cf.loc['speed', 'escooter'] * 1000)) * df.length \
        + cf.loc['bpsafe', 'escooter'] * (df.escoot_psafe_l - 4) * (df.length/dmin))
    
    df["walk_utils"] = - (cf.loc['btime', 'walk'] * (df.length/(cf.loc['speed', 'walk']  * 1000)) \
        + cf.loc['bpsafe', 'walk'] * (df.walk_psafe_l - 4) * (df.length/dmin))
    return df

def dij_graph(ln, tmode, minv, mth):
    graph = dij.Graph()
    
    for i in range(0, len(ln)):
        x = 0
        if tmode == 'car':
            psafe = ln.car_psafe_l.iloc[i]
            weight = ln.car_utils.iloc[i]
        elif tmode == 'ebike':
            psafe = ln.ebike_psafe_l.iloc[i]
            weight = ln.ebike_utils.iloc[i] # give the weight based on the utility function
        elif tmode == 'escooter':
            psafe = ln.escoot_psafe_l.iloc[i]
            weight = ln.escoot_utils.iloc[i]          
        elif tmode == 'walk':
            psafe = ln.walk_psafe_l.iloc[i]
            weight = ln.walk_utils.iloc[i]
        else:
            x = 999
            print('no mode')
            break
        
        if mth == 'shortest': weight = ln.length.iloc[i] # if method shortest path, psafe is not necessary
        elif mth == 'best': weight = weight # otherwise we need to estimate the utils per mode
        else: 
            x = 999
            print('wrong method')
            break
        text = ln.modes.iloc[i]
        if tmode in text: # creates a network with only the links in which tmode can be used
            if psafe>=minv: graph.add_edge(ln.from1.iloc[i], ln.to1.iloc[i], weight)
            # the previous formula decrease the number of available network links
            # only these that are above the psafe level.
    return graph, x

def dij_run(ln, nd, tmode, fr, to, mth, minv, dmin, coeff):
    
    ln = utils_cal(ln, coeff, dmin)
    
    graph = dij_graph(ln, tmode, minv, mth)[0]
    check = dij_graph(ln, tmode, minv, mth)[1]
    
    if check != 999: # run Dijkstra shortest path
        dijkstra = dij.DijkstraSPF(graph, fr)
        nod = list(nd.id)
        # print("%-5s %-5s" % ("label", "distance"))
        # for u in nod: 
        #    print(u, dijkstra.get_distance(u))
        print(dijkstra.get_path(to))
        x = dijkstra.get_path(to)
    return x 

def dij_dist_calc (path, ln): # calculate the distance
    suml = 0
    for i in range (len(path) - 1):
        matchid = ln.index[(ln.from1 == path[i]) & (ln.to1 == path[i + 1])].tolist()
        add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'length']
        suml = suml + add[matchid[0]]
    return suml