import os
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from Psafechoices.routing_model import network_graph as dij

# from Psafechoices.routing_model import assess_analysis as ass

from Psafechoices.choice_model import opp_cost_calculator as opp

####################################################### SIMULATION BEST BEST PATHS

# import choice model to run routin
# in this case, default choice model is utilized

root_dir = os.path.dirname(os.path.realpath(__file__))

speed = 15 # define mean speed of the selected mode
dcost = 7/speed
# mode = 'walk' # select transport mode: car, ebike, escooter, walk
# coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice', 'coeff_route_model.csv'))
# coeff = opp.opp_cost_calc(coeff, mode, speed, dcost)
# coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice', 'coeff_route_model.csv') , sep=',').set_index('param')

# run routing algorithm in this network
fr = 9000 # select origin point
to = 4000 # select destination point

def simulate_params(lin, nod, fr, to, minv, dmin, mode, coeff, scenario):
    coeff = opp.opp_cost_calc(coeff, mode, speed, dcost)
    mth = 'best'
    df = pd.DataFrame(columns =['dmin', 'minv', 'dist', 'seq', 'scenario'])
    for m in minv:
        for d in dmin: 
            path = dij.dij_run(lin, nod, mode, fr, to, mth, m, d, coeff)
            dist = dij.dij_dist_calc (path, lin)
            d = {'dmin':[d], 'minv':[m], 'dist':[dist], 'mode':[mode], 'seq': [path], 'scenario': [scenario]}
            df = df.append(pd.DataFrame(d), ignore_index=True)
    return df

def define_paths(sdf, mode):
    d = {'dist':sdf["dist"].unique(), 'path': range(1, 1 + len(sdf["dist"].unique()))}
    df = pd.DataFrame(d)
    df["path"] = df["path"] - 1
    df["path"] = mode + ' path ' + df["path"].astype(str)
    for i in range(0, len(df)):
        if df.dist.iloc[i] == 999999: df.path.iloc[i] = 'no path'
        sdf = pd.merge(left=sdf, right=df, how="inner", left_on='dist', right_on='dist')
        return sdf

def show_unique(df):
    ndf = df[["path", "dist", "scenario"]]
    ndf = ndf.sort_values(["path","dist", "scenario"]).drop_duplicates("path")
    return ndf

step = 50

scenario = 'scenario0'
nod_link = os.path.join(root_dir, 'shapefiles', 'nodes' ,'experimental_field_athens_nodes.shp')
nod = os.path.join(root_dir, 'shapefiles', 'nodes' ,'experimental_field_athens_nodes.shp')

lin = pd.read_csv(os.path.join('Psafechoices_outputs', scenario, 'psafest_scenario0.csv'))

coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice', 'coeff_route_model.csv') , sep=',')
# coeff = coeff.rename(columns={'params': 'Unnamed: 0'})

cardf = simulate_params(lin, nod, fr, to, range(0,8), range(0, 10001, step), 'car', coeff, scenario)
escootdf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'escooter', coeff, scenario)
walkdf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'walk', coeff, scenario)

cardf = cardf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'car', coeff, 'scenario01'))
escootdf = escootdf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'escooter', coeff, 'scenario01'))
walkdf = walkdf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'walk', coeff, 'scenario01'))

cardf = define_paths(cardf, 'car') 
escootdf = define_paths(escootdf, 'escooter')
walkdf = define_paths(walkdf, 'walk')
savdf = cardf
savdf = savdf.append(escootdf)
savdf = savdf.append(walkdf)

outpath = os.path.join(root_dir, 'Dijkstra_outputs')
savdf.to_csv(root_dir, scenario + '_routing_results_step50.csv')