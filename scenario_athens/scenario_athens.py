
import os
import pandas as pd

from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel

# pip install --upgrade --force-reinstall git+https://github.com/panosgjuras/Perceived_safety_choices

root_dir = os.path.dirname(os.path.realpath(__file__))
# read the nodes from a shapefile
nod = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_nodes.shp'))
# read the links from a shapefile
lin = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links.shp'))
# update traffic parameters and coordinates with nodes
lin = trfp.upd_links(lin, nod)
# estimate perceived safety model parameters using the output dataset
cf = psmodel.psafe_coeff_upd('simple')

lin = linpsafe.lin_psafe(lin, cf)