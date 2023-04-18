import pandas as pd
import dijkstra as dij
import os
import math

def utils_cal(df, cf, dmin, mode):
    # calclation of the utility based on an alternative utility function
    # Psafe impact is a function of dmin
    # It means that for links longer than dmin psafe has a significant weigth to utility function.....
    if mode == 'car':
        df["car_utils"] = cf.loc['btime', 'car'] * (df.length/(cf.loc['speed', 'car'] * 1000) \
                          + cf.loc['bcost', 'car'] * (cf.loc['dcost', 'car']/1000) * df.length \
                          + cf.loc['bpsafe', 'car'] * (df.car_psafe_l - 4) * (df.length/dmin))
    elif mode =='ebike':
        df["ebike_utils"] = cf.loc['btime', 'ebike'] * (df.length/(cf.loc['speed', 'ebike'] * 1000)\
                            + cf.loc['bcost', 'ebike'] * (cf.loc['dcost', 'ebike']/1000) * df.length \
                            + cf.loc['bpsafe', 'ebike'] * (df.ebike_psafe_l - 4) * (df.length/dmin))
    elif mode == 'escooter':
        df["escoot_utils"] = cf.loc['btime', 'escooter'] * (df.length/(cf.loc['speed', 'escooter'] * 1000)\
                             + cf.loc['bcost', 'escooter'] * (cf.loc['dcost', 'escooter']/1000) * df.length \
                             + cf.loc['bpsafe', 'escooter'] * (df.escoot_psafe_l - 4) * (df.length/dmin))
    elif mode == 'walk':
        df["walk_utils"] = cf.loc['btime', 'walk'] * (df.length/(cf.loc['speed', 'walk']  * 1000)\
                           + cf.loc['bcost', 'walk'] * (cf.loc['dcost', 'walk']/1000) * df.length \
                           + cf.loc['bpsafe', 'walk'] * (df.walk_psafe_l - 4) * (df.length/dmin))
    else: df["utils"] = 99999
    return df

# def mode_psafe_checker(tmode, ln, i):
#    if(tmode == 'car' or tmode == 'ebike' or tmode == 'escooter' or tmode == 'walk'): x = 'yes'
#        if tmode == 'car': psafe = ln.car_psafe_l.iloc[i]
#        elif tmode == 'ebike': psafe = ln.ebike_psafe_l.iloc[i]
#        elif tmode == 'escooter': psafe = ln.escoot_psafe_l.iloc[i]
#        elif tmode == 'walk': psafe = ln.walk_psafe_l.iloc[i]
#    else: x = 'no'
#    return x

def dij_graph(ln, tmode, minv, mth):
    graph = dij.Graph()
    
    for i in range(0, len(ln)):
        x = 0
        if tmode == 'car': psafe = ln.car_psafe_l.iloc[i]
        elif tmode == 'ebike': psafe = ln.ebike_psafe_l.iloc[i]
        elif tmode == 'escooter': psafe = ln.escoot_psafe_l.iloc[i]
        elif tmode == 'walk': psafe = ln.walk_psafe_l.iloc[i]
        else:
           x = 999
           print('no mode')
           break 
       
        if mth == 'best':
            # give the weight based on the utility function
            if tmode == 'car': weight = ln.car_utils.iloc[i]
            elif tmode == 'ebike': weight = ln.ebike_utils.iloc[i] 
            elif tmode == 'escooter': weight = ln.escoot_utils.iloc[i]          
            elif tmode == 'walk': weight = ln.walk_utils.iloc[i]
        elif mth == 'shortest': weight = ln.length.iloc[i] # if method shortest path, psafe is not necessary
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

def dij_run(ln, nd, tmode, fr, to, mth = "shortest" , minv = 1, dmin = 10000, coeff = 0):
    if mth != 'shortest': ln = utils_cal(ln, coeff, dmin, tmode)
    
    graph = dij_graph(ln, tmode, minv, mth)[0]
    check = dij_graph(ln, tmode, minv, mth)[1]
    
    if check != 999: # run Dijkstra shortest path
        dijkstra = dij.DijkstraSPF(graph, fr)
        # print(dijkstra)
        # nod = list(nd.id)
        # print("%-5s %-5s" % ("label", "distance"))
        # for u in nod: 
        #    print(u, dijkstra.get_distance(u))
        if math.isinf(dijkstra.get_distance(to)): # it estimates distance based on weigths
            x = 'no path'
            print(x)
        else: 
            x = dijkstra.get_path(to)
            print(x)
    return x 

# UPDATE HERE TO CREATE MATRICES FROM ONE PATH TO THE OTHER

# UPDATE HERE TO ESTIMATE TIME FROM TO
def dij_dist_calc(path, ln, var = 'sdist', tmode = 'walk'): # calculate the distance
    
    if tmode == 'car': psafe = 'car_psafe_l'
    elif tmode == 'ebike': psafe = 'ebike_psafe_l'
    elif tmode == 'escooter': psafe = 'escoot_psafe_l'
    else: psafe = 'walk_psafe_l'


    if path!= 'no path':
        suml = 0
        for i in range (len(path) - 1):
            matchid = ln.index[(ln.from1 == path[i]) & (ln.to1 == path[i + 1])].tolist()               
            if var == 'sumavgslope':
                add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'avgslope'] 
            elif var == 'summaxslope':
                add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'maxslope']
            elif var == 'sumpsafe':
                add = (ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), psafe] - 4) # + if psafe > 4, - if psafe < 4.
            elif var == 'weight_sumavgslope':
                add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'avgslope'] * ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'length']
            elif var == 'weight_summaxslope':
                add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'maxslope'] * ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'length']
            elif var == 'weight_sumpsafe':
                add = (ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), psafe] - 4) * ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'length']
            else: add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'length']
            suml = suml + add[matchid[0]]
    else: suml = 999999
    
    return suml