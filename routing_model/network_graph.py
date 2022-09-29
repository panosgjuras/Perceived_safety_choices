# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:31:59 2022

@author: kkoli
"""

import pandas as pd
import dijkstra as dij
import os

# current_dir = os.path.dirname(os.path.realpath(__file__)) 
os.chdir('C:/Users/panos_000/Desktop/github_tzouras/Perceived_safety_choices/network_analysis')
nodes = pd.read_csv("output_csv/experimental_field_athens_nod_coord.csv")
links = pd.read_csv("output_csv/experimental_field_athens_links_psafe.csv")

links["car_utils"] = + 6.0 * (links.length/(40*1000)) + 0.73822 * links.length - 0.90838 * (links.car_psafe_l-4) * (links.length/1000)
links["ebike_utils"] = + 6.0 * (links.length/(20*1000)) + 1.10523 * (8/(20*1000)) * links.length - 1.41532 * (links.ebike_psafe_l - 4) * (links.length/1000)
links["escoot_utils"] = + 6.0 * (links.length/(15*1000)) + 1.05452 * (7/(15*1000)) * links.length - 1.27399 * (links.escoot_psafe_l - 4) * (links.length/1000)
links["walk_utils"] = + 6.0 * (links.length/(5*1000)) + 0.86911 * (links.walk_psafe_l - 4) * (links.length/1000)
links["ps"] =  - links.escoot_psafe_l * (links.length/4917.710000000001)
nod = list(nodes.id)
graph = dij.Graph()



for i in range(0, len(links)):
    graph.add_edge(links.from1.iloc[i], links.to1.iloc[i], links.walk_utils.iloc[i])

dijkstra = dij.DijkstraSPF(graph, 9000)

print("%-5s %-5s" % ("label", "distance"))
for u in nod:
    print(u, dijkstra.get_distance(u))
    # print("%-5s %8d" % (u, dijkstra.get_distance(u)))

print(dijkstra.get_path(4000))
# In[00]: Inputs

from .graph import Graph, generate_random_graph
from .dijkstra import DijkstraSPF

__version__ = "0.2.1"
__author__ = "Jukka Aho <ahojukka5@gmail.com>"
__all__ = [Graph, DijkstraSPF, generate_random_graph]
# graph = dij.Graph()
# graph.add_edge(S, A, 4)
# graph.add_edge(S, B, 3)
# graph.add_edge(S, D, 7)
# graph.add_edge(A, C, 1)
# graph.add_edge(B, S, 3)
# graph.add_edge(B, D, 4)
# graph.add_edge(C, E, 1)
# graph.add_edge(C, D, 3)
# graph.add_edge(D, E, 1)
# graph.add_edge(D, T, 3)
# graph.add_edge(D, F, 5)
# graph.add_edge(E, G, 2)
# graph.add_edge(G, E, 2)
# graph.add_edge(G, T, 3)
# graph.add_edge(T, F, 5)

# dijkstra = dij.DijkstraSPF(graph, S)

# print("%-5s %-5s" % ("label", "distance"))
# for u in nod:
#    print("%-5s %8d" % (u, dijkstra.get_distance(u)))
# print(" -> ".join(dijkstra.get_path(T)))

# network=pd.read_csv("C:/Users/kkoli/Desktop/NTUA/SIM4MTRAN/Perceived_safety_choices-main/Perceived_safety_choices-main/network_analysis/output_csv/new_equil_lin_coord.csv")
    
# mynetwork=network[['from1','to1','length']]

#######################################################################################
#G =nx.Graph()
# G=nx.from_pandas_edgelist(network,'from1','to1',edge_attr='length')

# from matplotlib.pyplot import figure
# figure(figsize=(10, 8))
# nx.draw_shell(G, with_labels=True)

# dijkstra = DijkstraSPF(G, 11)
####################################################################################