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
from Psafechoices.network_analysis import maphist as mph
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
from Psafechoices.network_analysis import shp_to_csv_xml_tool as convert

# from Psafechoices.routing_model import assess_analysis as ass

root_dir = os.path.dirname(os.path.realpath(__file__))

# To run the Psafechoices model, it requires two models as inputs
# Psafe model: ordinal logistic regression model with infrastructure parameters
# Choice model: BIOGEME discrete choice mode with time + cost + safety
scenario = 'scenario0'
nod_link = os.path.join(root_dir, 'shapefiles', 'nodes' ,'experimental_field_athens_nodes.shp')
lin_link = os.path.join(root_dir, 'shapefiles', scenario, 'experimental_field_athens_links.shp')

# nod_link = '/Users/panosgtzouras/Desktop/WEBSCENATHENS/shapefiles/nodes/experimental_field_athens_nodes.shp'
# lin_link = '/Users/panosgtzouras/Desktop/WEBSCENATHENS/shapefiles/scenario0/experimental_field_athens_links.shp'
# outpath = os.path.join(root_dir, 'outputs')
outpath = os.path.join(root_dir, 'Psafechoices_outputs', scenario)

# read the nodes from a shapefile
nod = trfp.read_shapefile(nod_link)
# read the links from a shapefile
# TEST HERE NEW SCENARIOS WITH INFRASTUCTURE UPDATES
lin = trfp.read_shapefile(lin_link)
# update traffic parameters and coordinates with nodes
lin = trfp.upd_links(lin, nod).reset_index()
# update perceived safety model parameters using the output model from Rchoice
# in this case, default perceived safety models are used. Use your own models...
cf = pd.read_csv(os.path.join(root_dir, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
# estimate perceived safety per link and per transport mode
lin = linpsafe.lin_psafe(lin, cf)
# create a csv file for mapping purposes

csv = 'psafest_'+ scenario + '.csv'
convert.netcsv_cr(lin, os.path.join(outpath, csv))
# create an XML for MATSim
convert.netxml_cr(lin, nod, os.path.join(outpath, 'psafest_'+ scenario + '.xml'))

# shppath = 'C:/Users/panos_000/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens/shapefiles'

mph.psafehist(lin, outpath, 'car', scenario)
mph.psafehist(lin, outpath, 'ebike', scenario)
mph.psafehist(lin, outpath, 'escooter', scenario)
mph.psafehist(lin, outpath, 'walk', scenario)

mph.psafemap(lin_link, nod_link, os.path.join(outpath, csv), outpath, scenario)
