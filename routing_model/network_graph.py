# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:31:59 2022

@author: kkoli
"""


import pandas as pd
import networkx as nx 
import dijkstra

network=pd.read_csv("C:/Users/kkoli/Desktop/NTUA/SIM4MTRAN/Perceived_safety_choices-main/Perceived_safety_choices-main/network_analysis/output_csv/new_equil_lin_coord.csv")
    
mynetwork=network[['from1','to1','length']]


#######################################################################################
G=nx.Graph()
G=nx.from_pandas_edgelist(network,'from1','to1',edge_attr='length')

from matplotlib.pyplot import figure
figure(figsize=(10, 8))
nx.draw_shell(G, with_labels=True)

dijkstra = DijkstraSPF(G, 11)
####################################################################################
