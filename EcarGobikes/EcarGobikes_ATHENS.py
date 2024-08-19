# install Psafechoices package version 0.2
# pip install git+https://github.com/lotentua/Perceived_safety_choices

# upgrade Psafechoices package # STILL UNDER DEVELOPMENT
# pip install --upgrade --force-reinstall git+https://github.com/lotentua/Perceived_safety_choices

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import ast

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
# from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert
from Psafechoices.routing_model import network_graph as dij

def read_points(path: str) -> pd.DataFrame:
    points = pd.read_csv(path, delimiter = ";")
    print(len(points))
    return points

root_dir = os.path.dirname(os.path.realpath(__file__))
path_points = os.path.join(root_dir, 'logistNet')
points = read_points(os.path.join(path_points, 'depot_delpoints_ATHENS.csv')) # Depots and delivery points

# points.to_csv(os.path.join(path_points, 'delpoints_ATHENS.csv'))

def logistnet_cre(df):
    sdf = pd.DataFrame(columns =['from1', 'to1'])
    for item1 in df.delpoint:
       ndf = pd.DataFrame()
       i = 0
       for item2 in df.delpoint:
           ndf.loc[i, 'from1'] = item1
           ndf.loc[i, 'to1'] = item2
           i = i + 1
       sdf = pd.concat([sdf, ndf])
    # sdf = pd.concat([df.rename(columns = {'depot':'from1', 'delpoint': 'to1'}), sdf])
    sdf['pid'] = np.arange(1, len(sdf) + 1, 1)
    sdf = sdf.set_index('pid')
    return(sdf)

net = logistnet_cre(points)

path_scenario = '/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens' # Add the path of the scenario Athens



nod = trfp.read_shapefile(os.path.join(path_scenario, 'shapefiles','nodes/experimental_field_athens_nodes.shp'))



# '/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens/shapefiles/scenario0/experimental_field_athens_links.shp'

lin = trfp.read_shapefile(os.path.join(path_scenario, 'shapefiles', 'scenario0/experimental_field_athens_links.shp'))



slopes = pd.read_csv(os.path.join(path_points,'new_slopes_Athens.csv')) # ADD the DTM model
slopes = slopes.drop(columns = ["modes_y"])
lin = pd.merge(lin, slopes, left_on = 'id', right_on = 'id') # add slopes in the links dataframe, CHECK IF ALL CAN BE MATCHED
cf = pd.read_csv(os.path.join(path_scenario, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
lin = linpsafe.lin_psafe(lin, cf)

lin = trfp.upd_links(lin, nod)

lin['modes'] = 'ebike' # assumption ebike can travel in all links

lin = lin.rename(columns = {'Avg_Slope':'avgslope', 'Max_Slope':'maxslope'})

def fixslope(lin, nod):
    lin["zfrom"] = pd.merge(lin, nod, left_on = 'from1', right_on = 'id').z 
    lin["zto"] = pd.merge(lin, nod, left_on = 'to1', right_on = 'id').z
    #lin["slope"] = ((lin.zto - lin.zfrom)/lin.length)*100
    lin.avgslope = np.where(lin.zfrom > lin.zto, 0 - lin.avgslope, lin.avgslope)
    lin.maxslope = np.where(lin.zfrom > lin.zto, 0 - lin.maxslope, lin.maxslope)
    lin = lin.drop(columns=["zfrom", "zto"])
    return(lin)

lin = fixslope(lin, nod)

# coeff = pd.read_csv(os.path.join(path_scenario, 'default_models', 'choice','coeff_choice_model.csv'),',')
# speed = 20 # define mean speed of the selected mode
# dcost = 7/speed
# coeff = opp.opp_cost_calc(coeff, 'ebike', speed, dcost) # FIX FIX FIX here....

def logisticnet_sdist(df, lin, nod):
    df["path"] = 0
    for i in range(1, len(df) + 1):
        path = dij.dij_run(lin, nod, 'ebike', df.loc[i, 'from1'], df.loc[i, 'to1'])
        
        df['path'] = df['path'].astype('object')
        df.at[i, 'path'] = path
        
        df.loc[i, 'sdist'] = dij.dij_dist_calc(path, lin)
        
        df.loc[i, 'sum_psafe'] = dij.dij_dist_calc(path, lin, 'sumpsafe', 'ebike')
        df.loc[i, 'sum_avgslope'] = dij.dij_dist_calc(path, lin, 'sumavgslope', 'ebike')
        df.loc[i, 'sum_maxslope'] = dij.dij_dist_calc(path, lin, 'summaxslope', 'ebike')
        
        df.loc[i, 'wavg_psafe'] = dij.dij_dist_calc(path, lin, 'weight_sumpsafe', 'ebike')
        
        df.loc[i, 'wavg_avgslope'] = dij.dij_dist_calc(path, lin, 'weight_sumavgslope', 'ebike')
        
        df.loc[i, 'wavg_maxslope'] = dij.dij_dist_calc(path, lin, 'weight_summaxslope', 'ebike')

    df.wavg_psafe = np.where((df.sdist!=0) & (df.sdist!=999999), df.wavg_psafe/df.sdist, 999999)
    df.wavg_avgslope = np.where((df.sdist!=0) & (df.sdist!=999999), df.wavg_avgslope/df.sdist, 999999)
    df.wavg_maxslope = np.where((df.sdist!=0) & (df.sdist!=999999), df.wavg_maxslope/df.sdist, 999999)
    
    return(df)

net = logisticnet_sdist(net, lin, nod)

def netInfAna(df, lin):
    # df['path'] = df['path'].apply(ast.literal_eval)
    xt = ['type1', 'type2', 'type3', 'type4']
    types = ['1: Urban road with sidewalk less than 1.5 m wide', 
             '2: Urban road with sidewalk more than 1.5 m wide',
             '3: Urban road with cycle lane',
             '4: Shared space']
    
    df['path'] = df['path'].apply(ast.literal_eval)

    for x in xt: df['sumlen' + x] = 0

    # Iterate over the rows of the dataframe
    for idx in df.index:
        path = df.at[idx, 'path']
        print(path)
        # print(path)  
        for x in range(len(types)):
            
            suml = 0
            
            for j in range(len(path) - 1):
                from_node = int(path[j])
                to_node = int(path[j + 1])
                condition = (lin.from1 == from_node) & (lin.to1 == to_node)
                # print('point1 =' + path[j])
                if (lin.loc[condition, 'inf'] == types[x]).any():
                    # print("heloo")
                    add = lin.loc[condition, 'length'].values[0] if not lin.loc[condition, 'length'].empty else 0
                    suml += add
            # print("hello2")        
            df.at[idx, 'sumlen' + xt[x]] = suml
    return df


net2 = pd.read_csv("/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/EcarGobikes/NETfile/net_file_ATHENS.csv")
net2 = netInfAna(net2, lin)

net2.to_csv(os.path.join(root_dir, 'NETfile', 'net_file_ATHENS.csv'))




df = net2
df['path'] = df['path'].apply(ast.literal_eval)