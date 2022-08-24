"""
The PERCEIVED SAFETY CHOICE model

@author: ptzouras
National Technical University of Athens
Research project: SIM4MTRAN
"""
import pandas as pd
import os
# import numpy as np

# In[00]: Inputs
current_dir = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(current_dir)
b1 = pd.read_csv('raw_data/raw_data_perceived_choices_block1.csv', ',') # data, as it were downloaded from QuestionPro
b1["pid"]=range(100,len(b1.index)+100)
b2 = pd.read_csv('raw_data/raw_data_perceived_choices_block2.csv', ',')
b2["pid"]=range(200,len(b2.index)+200)
b3 = pd.read_csv('raw_data/raw_data_perceived_choices_block3.csv', ',') 
b3["pid"]=range(300,len(b3.index)+300)

# In[01]: Sociodmographic and rating data processing
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('psafe_models/data_process')
from data_process_psafe import socio_dats
socio = socio_dats(b1, b2, b3)

from data_process_psafe import rate_dats
rate = rate_dats(b1, b2, b3, socio)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
socio.set_index('pid').to_csv('datasets/socio_dataset_perceived_choices.csv')
rate.set_index('pid').to_csv('datasets/rating_dataset_perceived_choices.csv') # save the final rating dataset with no correlations

# In[02]: Choice data processing
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('choice_model/data_process')

from choice_data_process import choice_dats
choice = choice_dats(b1, b2, b3, rate, socio)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
choice.set_index('pid').to_csv('datasets/choice_dataset_perceived_choices.csv')

# In[03]: Development of psafe models
os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.chdir('psafe_models')

from psafe_coeff_update import coeff_upd
coeff = coeff_upd()

# In[04]: Network analysis