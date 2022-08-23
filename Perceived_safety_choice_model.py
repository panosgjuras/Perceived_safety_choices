
"""
The PERCEIVED SAFETY CHOICE model

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
import os
import numpy as np
# In[00]: Inputs
current_dir = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(current_dir)
b1 = pd.read_csv('raw_data/raw_data_perceived_choices_block1.csv', ',')
b1["pid"]=range(100,len(b1.index)+100)
b2 = pd.read_csv('raw_data/raw_data_perceived_choices_block2.csv', ',')
b2["pid"]=range(200,len(b2.index)+200)
b3 = pd.read_csv('raw_data/raw_data_perceived_choices_block3.csv', ',') 
b3["pid"]=range(300,len(b3.index)+300)
# In[01]: Sociodmographic and rating data processing 