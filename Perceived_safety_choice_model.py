"""
The PERCEIVED SAFETY CHOICE model

@author: ptzouras
National Technical University of Athens
Research project: SIM4MTRAN
"""
import pandas as pd
import os
# import numpy as np

def gen_path():
    current_dir = os.path.dirname(os.path.realpath(__file__)) 
    os.chdir(current_dir)
# In[00]: Inputs
gen_path()

b1 = pd.read_csv('raw_data/raw_data_perceived_choices_block1.csv', ',') # data, as it were downloaded from QuestionPro
b1["pid"]=range(100,len(b1.index)+100)
b2 = pd.read_csv('raw_data/raw_data_perceived_choices_block2.csv', ',')
b2["pid"]=range(200,len(b2.index)+200)
b3 = pd.read_csv('raw_data/raw_data_perceived_choices_block3.csv', ',') 
b3["pid"]=range(300,len(b3.index)+300)
# In[01]: Sociodmographic and rating data processing
gen_path()
os.chdir('psafe_models/data_process')

from data_process_psafe import socio_dats
socio = socio_dats(b1, b2, b3)

from data_process_psafe import rate_dats
rate = rate_dats(b1, b2, b3, socio)

gen_path()
# save the outputs of data processing
socio.set_index('pid').to_csv('datasets/socio_dataset_perceived_choices.csv')
rate.set_index('pid').to_csv('datasets/rating_dataset_perceived_choices.csv') # save the final perceived safety rating dataset

# In[02]: Choice data processing
gen_path()
os.chdir('choice_model/data_process')

from choice_data_process import choice_dats
choice = choice_dats(b1, b2, b3, rate, socio)

gen_path()
# save the outputs of choice data processing
choice.set_index('pid').to_csv('datasets/choice_dataset_perceived_choices.csv')

# In[03]: Development of psafe models
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('psafe_models')

from psafe_coeff_update import coeff_upd
coeff = coeff_upd()

# In[04]: Network analysis
gen_path()
os.chdir('network_analysis')

from traffic_params_upd import read_shapefile # function to read shapefile
lin = read_shapefile('networks_shp/new_equil/simple_network_links.shp') # import links shapefile, it needs a specific format
nod = read_shapefile('networks_shp/new_equil/simple_network_nodes.shp') # import nodes shapefile, it needs a specific format

from traffic_params_upd import upd_links # function to update link traffic parameters ("physical supply")
lin = upd_links(lin, nod)

from lin_psafe_calc import lin_psafe
lin = lin_psafe(lin, coeff)

from shp_to_csv_xml_tool import netcsv_cr
netcsv_cr(lin, 'output_csv/new_equil_psafe.csv')

from shp_to_csv_xml_tool import netxml_cr
netxml_cr(lin, nod, 'output_xml/new_equil_network.xml')

# In[05]: Choice modeling
gen_path()
os.chdir('choice_model')

from BIOGEME_models_perceived_choices import model_estimation
p = model_estimation(choice.set_index('pid'), 'MNL', 'mode_choice_model')

gen_path()
p.to_csv('choice_model/coeff_choice_model.csv')