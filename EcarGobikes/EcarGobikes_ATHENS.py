# install Psafechoices package version 0.2
# pip install git+https://github.com/lotentua/Perceived_safety_choices

# upgrade Psafechoices package # STILL UNDER DEVELOPMENT
# pip install --upgrade --force-reinstall git+https://github.com/lotentua/Perceived_safety_choices

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
# from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert
from Psafechoices.routing_model import network_graph as dij

def read_points(path: str) -> pd.DataFrame:
    points = pd.read_csv(path, delimiter = ",")
    print(len(points))
    return points

# G:\My Drive\PAPERS_TZOURAS\paper29_the_pre_battle\paper_christie 
path_points = '/Users/panosgtzouras/Library/CloudStorage/GoogleDrive-panosgjuras@gmail.com/My Drive/PAPERS_TZOURAS/paper29_the_pre_battle/paper_christie'
points = read_points(os.path.join(path_points, 'delpoints_ATHENS.csv'))

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


path_scenario = '/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens'
nod = trfp.read_shapefile(os.path.join(path_scenario, 'shapefiles','experimental_field_athens_nodes.shp'))
lin = trfp.read_shapefile(os.path.join(path_scenario, 'shapefiles', 'experimental_field_athens_links.shp'))
slopes = pd.read_csv(os.path.join(path_points,'new_slopes_Athens.csv'))
slopes = slopes.drop(columns = ["modes_y"])
lin = pd.merge(lin, slopes, left_on = 'id', right_on = 'id') # add slopes in the links dataframe
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
net.to_csv(os.path.join(path_points, 'net_file_ATHENS.csv'))

# df = net[(net.sdist!=999999) & (net.sdist!=0)]
# plt.scatter(df.sdist, df.sum_psafe)
# plt.scatter(df.sdist, df.sum_avgslope)
# plt.scatter(df.sdist, df.sum_maxslope)

# x = -2350
# plt.scatter(df.sdist, df.wavg_psafe * (x))
# plt.scatter(df.sdist, df.wavg_avgslope)
# plt.scatter(df.sdist, df.wavg_maxslope)
