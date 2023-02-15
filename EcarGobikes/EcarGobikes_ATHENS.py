import pandas as pd
import numpy as np
import os

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
from Psafechoices.routing_model import network_graph as dij
from Psafechoices.choice_model import opp_cost_calculator as opp

def read_points(path: str) -> pd.DataFrame:
    points = pd.read_csv(path)
    print(len(points))
    return points

path_points = 'G:/My Drive/PAPERS_TZOURAS/paper29_the_pre_battle/paper_christie'
points = read_points(os.path.join(path_points, 'depot_delpoints_ATHENS.csv'))

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
    sdf = pd.concat([df.rename(columns = {'depot':'from1', 'delpoint': 'to1'}), sdf])
    sdf['pid'] = np.arange(1, len(sdf) + 1, 1)
    sdf = sdf.set_index('pid')
    return(sdf)

net = logistnet_cre(points)

path_scenario = 'C:/Users/panos/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens'
nod = trfp.read_shapefile(os.path.join(path_scenario, 'shapefiles','experimental_field_athens_nodes.shp'))
lin = trfp.read_shapefile(os.path.join(path_scenario, 'shapefiles', 'experimental_field_athens_links.shp'))
lin = trfp.upd_links(lin, nod)
cf = pd.read_csv(os.path.join(path_scenario, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
lin = linpsafe.lin_psafe(lin, cf)

coeff = pd.read_csv(os.path.join(path_scenario, 'default_models', 'choice','coeff_choice_model.csv'),',')
speed = 20 # define mean speed of the selected mode
dcost = 7/speed
coeff = opp.opp_cost_calc(coeff, 'escooter', speed, dcost) # FIX FIX FIX here....

def logisticnet_sdist(df):
    for i in range(1, len(df) + 1):
        path = dij.dij_run(lin, nod, 'escooter', df.loc[i, 'from1'], df.loc[i, 'to1'] , 'shortest', 0, 1000, coeff)
        df['path'] = df['path'].astype('object')
        df.at[i, 'path'] = path
        df.loc[i, 'sdist'] = dij.dij_dist_calc(path, lin)
    return(df)

net = logisticnet_sdist(net)