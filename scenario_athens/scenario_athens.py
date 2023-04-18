# install Psafechoices package version 0.2
# pip install git+https://github.com/lotentua/Perceived_safety_choices

# upgrade Psafechoices package # STILL UNDER DEVELOPMENT
# pip install --upgrade --force-reinstall git+https://github.com/lotentua/Perceived_safety_choices

import os
import pandas as pd
import warnings
import numpy as np
import tempfile
import zipfile
warnings.simplefilter(action='ignore', category=FutureWarning)

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.network_analysis import maphist as mph
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert
from Psafechoices.routing_model import network_graph as dij
from Psafechoices.choice_model import opp_cost_calculator as opp

# NEW NEW NEW ... MODULES TO ESTIMATE INDICATORS
# they have been integrated in the setup file
from Psafechoices.microindianalysis import indicators as indi
from Psafechoices.microindianalysis import analysistools as ana

# from Psafechoices.routing_model import assess_analysis as ass

root_dir = os.path.dirname(os.path.realpath(__file__))

# To run the Psafechoices model, it requires two models as inputs
# Psafe model: ordinal logistic regression model with infrastructure parameters
# Choice model: BIOGEME discrete choice mode with time + cost + safety
scenario = 'scenario_0_ATHENS'
nod_link = os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_nodes.shp')
lin_link = os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links.shp')

# read the nodes from a shapefile
nod = trfp.read_shapefile(nod_link)
# read the links from a shapefile
# TEST HERE NEW SCENARIOS WITH INFRASTUCTURE UPDATES
lin = trfp.read_shapefile(lin_link)
# update traffic parameters and coordinates with nodes
lin = trfp.upd_links(lin, nod)
# update perceived safety model parameters using the output model from Rchoice
# in this case, default perceived safety models are used. Use your own models...
cf = pd.read_csv(os.path.join(root_dir, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
# estimate perceived safety per link and per transport mode
lin = linpsafe.lin_psafe(lin, cf)
# create a csv file for mapping purposes
outpath = os.path.join(root_dir, 'outputs')

csv = 'sim4mtran_psafest_'+ scenario + '.csv'
convert.netcsv_cr(lin, os.path.join(outpath, csv))
# create an XML for MATSim
convert.netxml_cr(lin, nod, os.path.join(outpath, 'sim4mtran_psafest_'+ scenario + '.xml'))

# shppath = 'C:/Users/panos_000/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens/shapefiles'

mph.psafehist(lin, outpath, 'car', scenario)
mph.psafehist(lin, outpath, 'ebike', scenario)
mph.psafehist(lin, outpath, 'escooter', scenario)
mph.psafehist(lin, outpath, 'walk', scenario)

mph.psafemap(lin_link, nod_link, os.path.join(outpath, csv), outpath, scenario)
# shp = gpd.read_file(os.path.join(shppath, 'experimental_field_athens_links.shp'))
# shp2 = gpd.read_file(os.path.join(shppath, 'experimental_field_athens_nodes.shp'))


####################################################### SIMULATION BEST BEST PATHS

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

# step = 50
# cardf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'car', coeff, 'scenario00')
      
# escootdf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'escooter', coeff, 'scenario00')

# walkdf = simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'walk', coeff, 'scenario00')

# lin = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links_scenario1.shp'))
# lin = trfp.upd_links(lin, nod)
# lin = linpsafe.lin_psafe(lin, cf)

# cardf = cardf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'car', coeff, 'scenario01'))
# escootdf = escootdf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'escooter', coeff, 'scenario01'))
# walkdf = walkdf.append(simulate_params(lin, nod, fr, to, range(0,8),range(0, 10001, step), 'walk', coeff, 'scenario01'))

# cardf = define_paths(cardf, 'car') 
# escootdf = define_paths(escootdf, 'escooter')
# walkdf = define_paths(walkdf, 'walk')
# savdf = cardf
# savdf = savdf.append(escootdf)
# savdf = savdf.append(walkdf)

# savdf.to_csv('G:/My Drive/research_papers/paper19_SIM4MTRAN_model/paper_SUSTAINABILITY/new_data_analysis/all_scenarios_routing_results_step50.csv')
#savdf.to_csv('')
# path_table = show_unique(savdf)


# NEW NEW NEW
# estimation of indicators based on the output txt files of MATSim
simoutlink = os.path.join(root_dir, 'simulation_Out', 'pkm_modestats.txt')
simout = pd.read_csv(simoutlink, sep="\t")

carOccupancy = 1.4
carVKM = simout['car'].to_numpy() * carOccupancy
escootVKM = simout['escoot'].to_numpy()
# iterNum = carVKM.shape[0] # not necessary...

carCO2 = indi.car_co2(carVKM)
carCOST = indi.car_cost(carVKM) 
carSAFETY = indi.car_safety(carVKM)

escootCO2 = indi.escoot_co2(escootVKM)
escootCOST = indi.escoot_cost(escootVKM)
escootSAFETY = indi.escoot_safety(escootVKM)

dfstat = ana.descrstat(carCO2, carCOST, carSAFETY, escootCO2, escootCOST, escootSAFETY)
temp1 = tempfile.NamedTemporaryFile(suffix='.xlsx')
dfstat.to_excel(temp1, index=False)

df_ba = ana.perchange(carVKM, escootVKM, carCO2, carCOST, carSAFETY, 
                      escootCO2, escootCOST, escootSAFETY)
temp2 = tempfile.NamedTemporaryFile(suffix='.xlsx')
df_ba.to_excel(temp2, index=False)

temp3 = ana.boxplot([carCO2], ['Car'], 'CO2 Emissions Cars', 'CO2 (kg)')
temp4 = ana.boxplot([escootCO2], ['E-scooter'], 'CO2 Emissions E-scooters', 'CO2 (kg)')

temp5 = ana.boxplot([carCOST, escootCOST], ['Car', 'E-scooter'], 'Cost of use per mode', 'Cost of use (€)')
temp6 = ana.boxplot([carSAFETY, escootSAFETY], ['Car', 'E-scooter'], 'Safety per mode', 'Safety (fatalities)')

ax = df_ba.plot.bar(x='Name', y='Diff %', rot=45, legend=False,
                        figsize=(8, 8), title='Indicators', 
                        xlabel='Name', ylabel = 'Diff %')
fig = ax.get_figure() 
temp7 = tempfile.NamedTemporaryFile(suffix='.xlsx')
fig.savefig(temp7, dpi=300)

## create a zip file... THIS THIS THE MAIN OUTPUT
zipFile = zipfile.ZipFile('indicators_'+ scenario + '.zip', 'w')

temps = [temp1, temp2, temp3, temp4, temp5, temp6, temp7]
fileNames = ['1 - Indicators Stats.xlsx', '2 - Changes.xlsx', '3 - CO2 Emissions Cars.png', 
             '4 - CO2 Emissions E-scooters.png', '5 - Cost of use per mode.png',
             '6 - Safety per mode.png', '7 - Changes.png']
for z, temp in enumerate(temps):
    zipFile.write(temp.name, fileNames[z], zipfile.ZIP_DEFLATED)
zipFile.close()