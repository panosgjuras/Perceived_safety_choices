"""
The PERCEIVED SAFETY CHOICE model

@author: ptzouras
National Technical University of Athens
Research project: SIM4MTRAN
"""
import pandas as pd
import os
from psafe_models.data_process.data_process_psafe import socio_dats, rate_dats
from choice_model.data_process.choice_data_process import choice_dats
from choice_model.opp_cost_calculator import opp_cost_calc
from psafe_models.psafe_coeff_update import coeff_upd
from network_analysis.traffic_params_upd import read_shapefile, upd_links
from network_analysis.lin_psafe_calc import lin_psafe
from network_analysis.shp_to_csv_xml_tool import netcsv_cr, netxml_cr

root_dir = os.path.dirname(os.path.realpath(__file__))

# In[00]: Inputs
b1 = pd.read_csv(
    os.path.join(root_dir, 'raw_data', 'raw_data_perceived_choices_block1.csv'), ',')  # data, as it were downloaded from QuestionPro
b1["pid"] = range(100, len(b1.index)+100)
b2 = pd.read_csv(os.path.join(root_dir, 'raw_data',
                 'raw_data_perceived_choices_block2.csv'), sep=',')
b2["pid"] = range(200, len(b2.index)+200)
b3 = pd.read_csv(os.path.join(root_dir, 'raw_data',
                 'raw_data_perceived_choices_block3.csv'), sep=',')
b3["pid"] = range(300, len(b3.index)+300)

# In[01]: Sociodmographic and rating data processing
socio = socio_dats(b1, b2, b3)
rate = rate_dats(b1, b2, b3, socio)

# save the outputs of data processing
socio.set_index('pid').to_csv(os.path.join(
    root_dir, 'datasets', 'socio_dataset_perceived_choices.csv'))
# save the final perceived safety rating dataset
rate.set_index('pid').to_csv(os.path.join(
    root_dir, 'datasets', 'rating_dataset_perceived_choices.csv'))

# In[02]: Choice data processing
choice = choice_dats(b1, b2, b3, rate, socio)

# save the outputs of choice data processing
choice.set_index('pid').to_csv(os.path.join(
    root_dir, 'datasets', 'choice_dataset_perceived_choices.csv'))

# In[03]: Development of psafe models
coeff = coeff_upd()

# In[04]: Network analysis
nod = read_shapefile(
    os.path.join(root_dir, 'network_analysis', 'networks_shp',
                 'experimental', 'experimental_field_athens_nodes.shp')
)  # import links shapefile, it needs a specific format
lin = read_shapefile(
    os.path.join(root_dir, 'network_analysis',
                 'networks_shp', 'experimental', 'experimental_field_athens_links_scenario1.shp')
)  # import nodes shapefile, it needs a specific format

# update link traffic parameters ("physical supply")
lin = upd_links(lin, nod)
nod.set_index('id').to_csv(
    os.path.join(root_dir, 'network_analysis', 'output_csv',
                 'experimental_field_athens_nod_coord.csv')
)
lin = lin_psafe(lin, coeff)

netcsv_cr(lin, os.path.join(root_dir, 'network_analysis',
                            'output_csv', 'experimental_field_athens_links_psafe_scenario1.csv'))
netxml_cr(lin, nod, os.path.join(root_dir, 'network_analysis', 'output_xml',
                                 'experimental_field_athens_network_scenario1.xml'))

# In[05]: Choice modeling
path_choice_model = os.path.join(
    root_dir, 'choice_model', 'coeff_choice_model.csv')
opp_cost_calc(pd.read_csv(path_choice_model,
              sep=',').set_index('Unnamed: 0'), 'car')
opp_cost_calc(pd.read_csv(path_choice_model,
              sep=',').set_index('Unnamed: 0'), 'ebike')
opp_cost_calc(pd.read_csv(path_choice_model, sep=',').set_index(
    'Unnamed: 0'), 'escooter')
opp_cost_calc(pd.read_csv(path_choice_model,
              sep=',').set_index('Unnamed: 0'), 'walk')
