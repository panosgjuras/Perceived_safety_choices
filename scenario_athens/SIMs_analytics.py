import os
import pandas as pd
import numpy as np
from Psafechoices.network_analysis import traffic_params_upd as trfp
from Psafechoices.network_analysis import lin_psafe_calc as linpsafe
from Psafechoices.psafe_model import psafe_coeff_upd as psmodel
import statistics as stat

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

root_dir = os.path.dirname(os.path.realpath(__file__))
lin = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links.shp'))
nod = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_nodes.shp'))
lin = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links.shp'))
lin = trfp.upd_links(lin, nod)
cf = pd.read_csv(os.path.join(root_dir, 'default_models', 'psafe','simple_psafe_models.csv'), ',')
cf = psmodel.psafe_coeff_upd(cf)
lin = linpsafe.lin_psafe(lin, cf)


def psafehist(lin, mode = 'walk'):
    bin_edges = np.arange(0.5, 7.5+1, 1)
    if mode == 'car':
        var = lin.car_psafe_l
        color = 'grey'
        title = 'Car'
    elif mode =='ebike':
        var = lin.ebike_psafe_l
        color = 'green'
        title = 'E-bike'
    elif mode == 'escooter':
        var = lin.escoot_psafe_l
        color = 'red'
        title = 'E-scooter'
    else:
        var = lin.walk_psafe_l
        color = 'blue'
        title = 'Walk'

    fig, ax = plt.subplots(figsize = (7.5,6.5))
    var.plot(kind = "hist", density = True, bins = bin_edges, rwidth = 0.7, alpha=0.5,facecolor=color)
    var.plot(kind ='density', bw_method=1)
    ax.set_xlabel('Perceived Safety Level')
    ax.set_ylabel('Frequency')
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_title(title)
    ax.set_xticks(np.arange(1, 7+1, 1))
    ax.grid(False)
    plt.style.use("bmh")
    ax.tick_params(left = False, bottom = False)
    for ax, spine in ax.spines.items(): spine.set_visible(False)
    plt.show()

psafehist(lin, 'car')
psafehist(lin, 'ebike')
psafehist(lin, 'escooter')
psafehist(lin, 'walk')

lin2 = trfp.read_shapefile(os.path.join(root_dir, 'shapefiles', 'experimental_field_athens_links_scenario1.shp'))
lin2 = trfp.upd_links(lin2, nod)
lin2 = linpsafe.lin_psafe(lin2, cf)
psafehist(lin2, 'car')
psafehist(lin2, 'ebike')
psafehist(lin2, 'escooter')
psafehist(lin2, 'walk')
