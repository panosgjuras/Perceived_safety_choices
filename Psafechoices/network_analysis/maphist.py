import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import geopandas as gpd
# from Psafechoices.network_analysis import traffic_params_upd as trfp
# import sys
import geopandas as gpd
import folium
import branca.colormap as cm
import os

def psafehist(lin, output_link, mode = 'walk', scenario = 'scenario0'):
    """
    @author: ptzouras
    it plots a histogramn per transport mode and scenario + a trend line
    it requires a dataframe with the estimated psafe levels
    it saves the hist in the output folder defined by the user
    """
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
    ax.set_ylim(0, 0.7)
    ax.set_yticks([])
    ax.set_title(title)
    ax.set_xticks(np.arange(1, 7+1, 1))
    ax.grid(False)
    plt.style.use("bmh")
    ax.tick_params(left = False, bottom = False)
    for ax, spine in ax.spines.items(): spine.set_visible(False)
    plt.show()
    fig.savefig(os.path.join(output_link, ("sim4mtran_psafehist_"+ mode + "_" + scenario + ".png")))
    
def join_shapefile_csv(shapefile_path, csv_path, id_field = "id"):
    """
    @author: chkarolemeas
    Perform a spatial join between a shapefile and a CSV file using a common attribute.

    Parameters
    ----------
    shapefile_path : str
        Path to the original shapefile (containg links)
    csv_path : str
        Path to the CSV file (the output of SIM4MTRAN)
    id_field : str
        Name of the common attribute field used to perform the join.

    Returns
    -------
    joined : geopandas.GeoDataFrame
        The resulting GeoDataFrame containing the joined data from both the shapefile (links) and the CSV file (output of SIM4MTRAN).
    """
    # Load the shapefile and the CSV into GeoDataFrames
    shapes = gpd.read_file(shapefile_path)
    csv = pd.read_csv(csv_path)

    # Perform the join on the common id_field
    joined = shapes.merge(csv, on=id_field)

    return joined

dcolor = cm.StepColormap(
    ['#CF3429', '#E3652C', '#C8A53E', '#94EA6B', '#73BFB1', '#4171CA', '#0110AD'],
    index=[0, 1, 2, 3, 4, 5, 6, 7],
    vmin=0,
    vmax=7) # default colors to illustrate perceived, DO NOT CHANGE

def highlight_function(feature, prop_name, shp2, colormap = dcolor):
    """
    @author: chkarolemeas
    """
    prop_value = feature['properties'][prop_name]
    color = colormap(prop_value)
    if prop_name == 'id' and shp2.equals(feature):
        # Return a different style for shp2
        return {
            'fillColor': '#000000',
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.7,
            'radius': 5,
            'type': 'circleMarker'
        }
    else:
        return {
            'fillColor': color,
            'color': color,
            'weight': 5,
            'fillOpacity': 1
        }

def style_function(feature, prop_name, shp2, colormap = dcolor):
    """
    @author: chkarolemeas
    """
    prop_value = feature['properties'][prop_name]
    color = colormap(prop_value)
    if prop_name == 'id' and shp2.equals(feature):
        # Return a different style for shp2
        return {
            'fillColor': '#000000',
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.7,
            'radius': 5,
            'type': 'circleMarker'
        }
    else:
        return {
            'fillColor': color,
            'color': color,
            'weight': 3,
            'fillOpacity': 0.7
        }

def create_layer_with_highlight_and_tooltip(shp, prefix, name, layer_type, m, shp2):
    """
    @author: chkarolemeas
    """
    show = (name == 'Car')  # Set the show parameter based on the name. Car is set as default value
    gj = folium.GeoJson(
        shp,
        style_function=lambda x: style_function(x, prefix, shp2),
        highlight_function=lambda x: highlight_function(x, prefix, shp2),
        tooltip=folium.GeoJsonTooltip(fields=["inf", "pav", "obst", "cross"],
                                      aliases=["Information", "Pavement Condition", "Obstacles", "Crossing Type"],
                                      sticky=True,
                                      localize=True) if layer_type == 'shp' else folium.GeoJsonTooltip(fields=["x", "y"],
                                      aliases=["X", "Y"],
                                      sticky=True,
                                      localize=True),
        name=name,
        show=show  # Set the show parameter
    )
    gj.add_to(m)
    if layer_type == "shp":
        m.fit_bounds(gj.get_bounds())
    
def psafemap(lin_link, nod_link, csv_link, output_link, scenario = 'scenario_0',
             location = [37.9756, 23.7347], colormap = dcolor):
    """
    @author: chkarolemeas
    
    provide the links, nodes and estimated csv with psafe
    to export an html map with psafe evaluations
    
    it save to the output directory defined by the user.
    
    """
    # Load the shapefiles
    # shp = gpd.read_file()
    shp = join_shapefile_csv(lin_link, csv_link)
    shp2 = gpd.read_file(nod_link)

    # shp = lin
    # shp = nod
    
    
    m = folium.Map(location = location,  tiles="cartodb positron") # Default location, but changes according to the shp

    # Define a dictionary to store the layer names and style function prefixes
    layers = {
        'Car': ('car_psafe_l', 'shp'),
        'Walking': ('walk_psafe_l', 'shp'),
        'E-Scooter': ('escoot_psafe_l', 'shp'),
        'E-bike': ('ebike_psafe_l', 'shp'),
        'Nodes': ('id', 'shp2')
    }

    # Use a for loop to create the GeoJson layers with tooltip functionality
    for name, (prefix, layer_type) in layers.items():
        create_layer_with_highlight_and_tooltip(shp if layer_type == 'shp' else shp2, prefix, name, layer_type, m, shp2)

    # Add a branca colormap to the map
    colormap.caption = 'Perceived Safety Level'

    # Modify the properties of the colormap
    colormap.width = 500
    colormap.caption_font_family = 'arial'
    colormap.fill_alpha = 1
    colormap.stroke_color = '#ffffff'
    colormap.stroke_width = 2

    colormap.add_to(m)

    folium.LayerControl(collapsed=False, autoZIndex=False).add_to(m)

    # Save the map as an HTML file
    m.save(os.path.join(output_link, ("sim4mtran_psafemap_"+ scenario + ".html")))    