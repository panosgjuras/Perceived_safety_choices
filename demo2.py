#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: panosgtzouras
"""
# import pandas as pd
import os
import copy
# import random
import geopandas as gpd
# import math
# import matplotlib.pyplot as plt
# from collections import defaultdict
# import numpy as np
# import seaborn as sns
# from joblib import Parallel, delayed
# from tqdm import tqdm
# from collections import defaultdict
# from shapely.geometry import Point, LineString
# import osmnx as ox
# import networkx as nx
# import ast
# import matplotlib.cm as cm
# import numpy as np
# import scikit
# import sklearn
# from shapely.geometry import Point
# Keep this, do not download things from the package in order to be able to update it 
os.chdir("/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/Psafechoices") # TODO! import the package here
# from mapAnalysis import plotPsafeLev
# import Psafechoices.calc
from vosDijkstra import (OSMnetwork, osm_shp_match, upd_OSM_edge, VOSweight, 
                         shortPath, nearestNodes, simulateVOS, descrStats_stations, 
                         genHist, VOS_mean_max_double_plot, 
                         # stackInfrastructureMulti2,
                         bShareMapDiff, InfaBreakdown)

root_dir = "" # TODO! give the correct root_dir path
os.chdir(root_dir)
# out_dir = ""

# %% STEP 1. Select the city and download

G, latitude = OSMnetwork("Munich, Germany") # the latitude is median y in WGS 84
# %% STEP 2. Import the links shapefile with infrastructure type, 
# psafe and slope values as link attributes
links = gpd.read_file(os.path.join(root_dir, "")) # TODO! add the Munich network links in a cloud
links = links.to_crs(epsg = 4326)

# %% STEP 3. Select the transport mode and match link attributes with OSM edges

select_mode = 'e-bike' # options: car, e-bike, e-scooter, walk
tolerance = 5 # in meters, 

G = upd_OSM_edge(copy.deepcopy(G), 
                  osm_shp_match(G, links, latitude, tolerance = tolerance), 
                  select_mode)
# %% STEP 4. Test run
# Basic set the speed_config and see how the shortest path deviate

# must run first STEP 1, STEP 2 and STEP 3

orig_node, dest_node = nearestNodes(G, (48.137154, 11.576124), 
                                    (48.158822, 11.583137), distAssignCheck = True)

# it just estimates the shortest path
shortPath(G, orig_node, dest_node, mapCheck = True)[1]

# uniform distribution of travel speeds based on the road infrastructure type
speed_config = {
    "1: Urban road with sidewalk less than 1.5 m wide": {"min": 16, "max": 19},  # km/h
    "2: Urban road with sidewalk more than 1.5 m wide": {"min": 13.5, "max": 20.5},
    "3: Urban road with cycle lane": {"min": 18.5, "max": 26.6},
    "4: Shared space": {"min": 13.5, "max": 20.5}}

# estimates the weights of the netowrk based on the fastest path
G = VOSweight(G, 'fastest', var_v = True, dictSpeed = speed_config) 
# defines the fastest path between origin and destination points
shortPath(G, orig_node, dest_node, mapCheck = True, w = "VOSweight")[1]

# estimates the weights of the netowrk based on Value of Safety equal to 600 m
# each level of safety difference costs 600 m
G = VOSweight(G, 'safest', VOS = -600, var_v = True, dictSpeed = speed_config)
# defines the safest + fastest path between origin and destination points
shortPath(G, orig_node, dest_node, mapCheck = True, w = "VOSweight")[1] 