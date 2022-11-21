# install Psafechoices package version 0.2
# pip install git+https://github.com/panosgjuras/Perceived_safety_choices

# upgrade Psafechoices package # STILL UNDER DEVELOPMENT
# pip install --upgrade --force-reinstall git+https://github.com/panosgjuras/Perceived_safety_choices

import os
import pandas as pd

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert
from Psafechoices.routing_model import network_graph as dij
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
convert.netcsv_cr(lin, os.path.join(root_dir, 'output_csv', 'experimental_field_athens_upd_links.csv'))
# create an XML for MATSim
convert.netxml_cr(lin, nod, os.path.join(root_dir, 'output_xml', 'experimental_field_athens_upd_links.xml'))

# import choice model to run routin
# in this case, default choice model is utilized
tmode = 'escoοter' # select transport mode: car, ebike, escooter, walk
speed = 15 # define mean speed of the selected mode
dcost = 7/speed
coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice','coeff_choice_model.csv'),',')
coeff = opp.opp_cost_calc(coeff, tmode, speed, dcost)
# coeff = pd.read_csv(os.path.join(root_dir, 'default_models', 'choice', 'coeff_route_model.csv') , sep=',').set_index('param')

# run routing algorithm in this network
fr = 9000 # select origin point
to = 4000 # select destination point

mth = 'best' # select method, it can be 'shortest' or 'best' path
minv = 1 # miniumum ACCEPTABLE perceived safety level
dmin = 100 # in meters minimum distance so that psafe really matters
path = dij.dij_run(lin, nod, tmode, fr, to, mth, minv, dmin, coeff) # estimate the path
print(dij.dij_dist_calc (path, lin)) # estimate the path distance

psmodel.psafe_coeff_upd(cf)
