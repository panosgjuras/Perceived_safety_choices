#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: panosgtzouras
"""

import copy
import os

os.chdir("/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/Psafechoices") # TODO: Change it in the final notebook
from calc import processRowEst
from mapAnalysis import plotPsafeLev, PsafeHeatmaps
from mainFuns import modelPsafe_import, linksPsafe_import, score_diff, computeSignificantSafer

root_dir = "/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/data" # TODO: Change it in the final notebook

# %% Step 1: Import the links for which pereived safety score will be estimated

network_city = "Athens" # Select the network you want to estimate perceived safety
network_version = "_v1" # Select the network version

links = linksPsafe_import(os.path.join(root_dir, "scenario" + network_city, "baseNetwork" + network_version,
                                       "baseNetwork" + network_city + "Links" + network_version + ".shp"))

# %% Step 2: Import the perceived safety models

models_version = "_v1.1" # this one is with safety perceptions of Athens residents

cf1 = modelPsafe_import(os.path.join(root_dir, "models" + models_version, 
                                    "psafe", "psafe_models.csv"))

models_version = "_v1.2" # this one is with safety perceptions of Munich residents

cf2 = modelPsafe_import(os.path.join(root_dir, "models" + models_version, 
                                    "psafe", "psafe_models.csv"))

# %% Step 3: Esimtate perceived safety scores based on safety perception of Athens residents

modes = ['car', 'ebike', 'escoot', 'walk']

links_1 = links.copy()

for m in modes:
    latent_vars = []
    safety_levels = []
    
    for index, row in links.iterrows():        
        latent_vars.append(processRowEst(index, row, modes, cf1)[f'LatPsafe{m}'])
        safety_levels.append(processRowEst(index, row, modes, cf1)[f'LevPsafe{m}'])

    links_1[f'LatPsafe{m}'] = latent_vars
    links_1[f'LevPsafe{m}'] = safety_levels

# TODO: plotting functions are not working using the existing matplotlib version, check the requirements again
# for m in modes: plotPsafeLev(links_1, m, city = network_city) # If you want to plot the scores for each

# for m in modes: PsafeHeatmaps(links_1, m, city = network_city) # If you want to create a heatmap, showing the density of safe links per mode

# %% Step 4: Esimtate perceived safety scores based on safety perception of Munich residents

modes = ['car', 'ebike', 'escoot', 'walk']

links_2 = links.copy()

for m in modes:
    latent_vars = []
    safety_levels = []
    
    for index, row in links.iterrows():        
        latent_vars.append(processRowEst(index, row, modes, cf1)[f'LatPsafe{m}'])
        safety_levels.append(processRowEst(index, row, modes, cf1)[f'LevPsafe{m}'])

    links_2[f'LatPsafe{m}'] = latent_vars
    links_2[f'LevPsafe{m}'] = safety_levels

# for m in modes: plotPsafeLev(links_2, m, city = network_city) # If you want to plot the scores for each

# for m in modes: PsafeHeatmaps(links_2, m, city = network_city) # If you want to create a heatmap, showing the density of safe links per mode