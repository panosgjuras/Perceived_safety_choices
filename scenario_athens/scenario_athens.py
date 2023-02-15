# install Psafechoices package version 0.2
# pip install git+https://github.com/lotentua/Perceived_safety_choices

# upgrade Psafechoices package # STILL UNDER DEVELOPMENT
# pip install --upgrade --force-reinstall git+https://github.com/lotentua/Perceived_safety_choices

import os
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert
from Psafechoices.routing_model import network_graph as dij

# from Psafechoices.routing_model import assess_analysis as ass

from Psafechoices.choice_model import opp_cost_calculator as opp

root_dir = os.path.dirname(os.path.realpath(__file__))

# To run the Psafechoices model, it requires two models as inputs
# Psafe model: ordinal logistic regression model with infrastructure parameters
# Choice model: BIOGEME discrete choice mode with time + cost + safety

# read the nodes from a shapefile
nod = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_nodes.shp'))
# read the links from a shapefile
# TEST HERE NEW SCENARIOS WITH INFRASTUCTURE UPDATES
lin = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links.shp'))
# update traffic parameters and coordinates with nodes
lin = trfp.upd_links(lin, nod)
# update perceived safety model parameters using the output model from Rchoice
# in this case, default perceived safety models are used. Use your own models...
cf = pd.read_csv(os.path.join(root_dir, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
# estimate perceived safety per link and per transport mode
lin = linpsafe.lin_psafe(lin, cf)
# create a csv file for mapping purposes
# convert.netcsv_cr(lin, os.path.join(root_dir, 'output_csv', 'experimental_field_athens_upd_links.csv'))
# create an XML for MATSim
# convert.netxml_cr(lin, nod, os.path.join(root_dir, 'output_xml', 'experimental_field_athens_upd_links.xml'))

# import choice model to run routin
# in this case, default choice model is utilized
speed = 15 # define mean speed of the selected mode
dcost = 7/speed
coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice','coeff_choice_model.csv'),',')
# mode = 'walk' # select transport mode: car, ebike, escooter, walk
# coeff = opp.opp_cost_calc(coeff, mode, speed, dcost)
# coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice', 'coeff_route_model.csv') , sep=',').set_index('param')

# run routing algorithm in this network
fr = 9000 # select origin point
to = 4000 # select destination point




## MODEL RESULTS ANALYSIS TO BE INTEGRATED IN THE PSAFECHOICES MODEL
# def simulate_params(lin, nod, fr, to, minv, dmin, mode, coeff, scenario):
#    coeff = opp.opp_cost_calc(coeff, mode, speed, dcost)
#    mth = 'best'
#    df = pd.DataFrame(columns =['dmin', 'minv', 'dist', 'seq', 'scenario'])
#    for m in minv:
#        for d in dmin: 
#            path = dij.dij_run(lin, nod, mode, fr, to, mth, m, d, coeff)
#            dist = dij.dij_dist_calc (path, lin)
#            d = {'dmin':[d], 'minv':[m], 'dist':[dist], 'mode':[mode], 'seq': [path], 'scenario': [scenario]}
#            df = df.append(pd.DataFrame(d), ignore_index=True)
#    return df

# def define_paths(sdf, mode):
#    d = {'dist':sdf["dist"].unique(), 'path': range(1, 1 + len(sdf["dist"].unique()))}
#    df = pd.DataFrame(d)
#    df["path"] = df["path"] - 1
#    df["path"] = mode + ' path ' + df["path"].astype(str)
#    for i in range(0, len(df)):
#        if df.dist.iloc[i] == 999999: df.path.iloc[i] = 'no path'
#        sdf = pd.merge(left=sdf, right=df, how="inner", left_on='dist', right_on='dist')
#        return sdf

# def show_unique(df):
#    ndf = df[["path", "dist", "scenario"]]
#    ndf = ndf.sort_values(["path","dist", "scenario"]).drop_duplicates("path")
#    return ndf

step = 50
cardf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'car', coeff, 'scenario00')
      
escootdf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'escooter', coeff, 'scenario00')

walkdf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'walk', coeff, 'scenario00')

lin = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links_scenario1.shp'))
lin = trfp.upd_links(lin, nod)
lin = linpsafe.lin_psafe(lin, cf)

cardf = cardf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'car', coeff, 'scenario01'))
escootdf = escootdf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'escooter', coeff, 'scenario01'))
walkdf = walkdf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'walk', coeff, 'scenario01'))

cardf = define_paths(cardf, 'car') 
escootdf = define_paths(escootdf, 'escooter')
walkdf = define_paths(walkdf, 'walk')
savdf = cardf
savdf = savdf.append(escootdf)
savdf = savdf.append(walkdf)

# savdf.to_csv('G:/My Drive/research_papers/paper19_SIM4MTRAN_model/paper_SUSTAINABILITY/new_data_analysis/all_scenarios_routing_results_step50.csv')
#savdf.to_csv('')
path_table = show_unique(savdf)
