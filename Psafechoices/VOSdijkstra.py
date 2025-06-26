"""
Tools to run VOS dijkstra to define the shortest, safest and flattest path

@author: ptzouras
National Technical University of Athens
"""

import pandas as pd
import os
import copy
# import random
import geopandas as gpd
import math
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import seaborn as sns
# from joblib import Parallel, delayed
# from tqdm import tqdm

from shapely.geometry import Point, LineString
import osmnx as ox
import networkx as nx

from mapAnalysis import plotPsafeLev
 
# root_dir = "/Users/panosgtzouras/Desktop/datasets"
# os.chdir(root_dir)
# out_dir = "/Users/panosgtzouras/Library/CloudStorage/OneDrive-UniversityofWestAttica/TZOURAS_paperz/paper61_VoS_navigation/results_May_2025"

# PRE-PROSSESING FUNS
def OSMnetwork(city, plot = True):
    G = ox.graph_from_place(city, network_type='drive')
    if plot: ox.plot_graph(G)
    
    nodes = ox.graph_to_gdfs(G, edges = False)
    med_lat = nodes.geometry.y.median()
    
    return G, med_lat

def meters_to_degrees(meters, latitude):
    """Convert meters to approximate degrees at a given latitude."""
    degrees_lat = meters / 111320  # latitude degrees
    degrees_lon = meters / (111320 * math.cos(math.radians(latitude)))  # longitude degrees
    return degrees_lat, degrees_lon

def nearestNodes(G, orig, dest, distAssignCheck=False):
    """
    This function finds the nearest network nodes in a graph for two geographical locations 
    (origin and destination) based on their latitude and longitude coordinates in WGS84
    
    Parameters:
    -----------
    G : networkx.MultiDiGraph
        A network graph (e.g., obtained via osmnx) containing nodes and edges representing the road network.
    orig : tuple
        A tuple of (latitude, longitude) representing the origin location.
    dest : tuple
        A tuple of (latitude, longitude) representing the destination location.
    
    distAssignCheck : bool, optional (default=False)
        If True, the function will PRINT the distance,
        If False, only the node IDs are returned.
    
    Returns:
    --------
    tuple
        A tuple containing the IDs of the nearest nodes for the origin and destination locations.    
    """
    orig_node = ox.nearest_nodes(G, X=orig[1], Y=orig[0], return_dist=distAssignCheck)
    dest_node = ox.nearest_nodes(G, X=dest[1], Y=dest[0], return_dist=distAssignCheck)

    # If distAssignCheck is True, we return the node ID, ignoring the distance
    if distAssignCheck:
        print(orig_node[1], dest_node[1])
        return orig_node[0], dest_node[0]
    else:
        return orig_node, dest_node

def osm_shp_match(G, links, latitude, tolerance = 15, mapCheck = False):
    
    """
    Match OSM network edges to preprocessed link geometries based on spatial proximity.

    This function performs a nearest-neighbor spatial join between the edges of a graph 
    (typically derived from OpenStreetMap) and a GeoDataFrame of processed link geometries.
    It checks whether each link can be matched to an edge within a specified distance threshold,
    and optionally visualizes the match results.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        The input street network graph, typically from OSMnx.
    links : GeoDataFrame
        A GeoDataFrame containing the fully processed links to be matched with the network edges.
    tolerance : float, optional (default=15)
        Maximum distance (in the units of the CRS) within which a link can be matched to an edge.
    mapCheck : bool, optional (default=False)
        If True, visualizes the original links and the matched edges colored by perceived safety levels.
        Assumes `plotPsafeLev()` is defined and takes a GeoDataFrame and mode string as input.
    
    Returns
    -------
    GeoDataFrame
        A new GeoDataFrame resulting from the spatial join, containing attributes from both `links` and `edges_gdf`.

    """
    
    nodes_gdf, edges_gdf = ox.graph_to_gdfs(G)
    edges_gdf = edges_gdf.reset_index() 
    
    # Links are less than the edges
    # so one link is matched to more than one edge
    
    tolerance_deg = max(meters_to_degrees(tolerance, latitude)) # BECAUSE OF WGS 84 COORDINATE SYSTEM
    match = gpd.sjoin_nearest(links, edges_gdf, max_distance = tolerance, how = 'left')
    
    unmatched_count = match['index_right'].isna().sum()
    
    if unmatched_count > 0:
        print(f"Number of unmatched edges: {unmatched_count} out of {len(edges_gdf)}")
        print("Increase the tolerance to ensure that all network edges are matched")
    else:
        print("All network edges matched successfully.")
    
    if mapCheck:
        modes = ['ca', 'eb', 'es', 'wa']
        for m in modes: plotPsafeLev(copy.deepcopy(links), m)
        for m in modes: plotPsafeLev(copy.deepcopy(match), m)

    return match

def find_psafe_column(select_mode):
    """
    Return the name of the perceived safety column based on the selected transport mode.

    Parameters
    ----------
    select_mode : str
        The transport mode for which to retrieve the safety level column.
        Valid options: 'car', 'e-bike', 'e-scooter', 'walk'.

    Returns
    -------
    str
        The name of the column in the dataset that corresponds to the selected mode's perceived safety level.

    Raises
    ------
    ValueError
        If an invalid transport mode is provided.
    """
    mode_column_map = {
        'car': 'LevPsafeca',
        'e-bike': 'LevPsafeeb',
        'e-scooter': 'LevPsafeeb',
        'walk': 'LevPsafeeb'
    }

    try:
        return mode_column_map[select_mode.lower()]
    except KeyError:
        raise ValueError(f"Invalid transport mode: {select_mode}. "
                         "Choose from: 'car', 'e-bike', 'e-scooter', 'walk'.")

def upd_OSM_edge(G, mat, select_mode):
    """
    Update edges in a graph G with selected attributes from a matched GeoDataFrame.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        The street network graph whose edge attributes will be updated.
    
    mat : GeoDataFrame
        A GeoDataFrame resulting from matching processed links to the edges of G
        using spatial proximity (e.g., from osm_shp_match function).
    
    attrs_to_add : list of str
        The attribute names from `match` to copy over to the corresponding edges in G.

    Returns
    -------
    G : networkx.MultiDiGraph
        The updated graph with new attributes added to matched edges.
    """
    
    x = find_psafe_column(select_mode)
    
    mat = mat.rename(columns = {x: 'psafe'})
    
    attrs_to_add = ['inf', 'psafe'] # keep infrastructure type and psafe value
    
    for _, row in mat.iterrows():
        u, v, k = row['u'], row['v'], row['key']
        if G.has_edge(u, v, k):
            for attr in attrs_to_add:
                G[u][v][k][attr] = row[attr]
    
    return G

# VOS funs
def VOSweight(G, typ, VOS = 0, vcycle=20, vmixed=10, cpsafe = 7):
    """
    Assign a custom edge weight to a graph based on Value of Safety (VOS) and cycling infrastructure.

    This function computes a "VOSweight" for each edge in a graph `G`, which can be used 
    to define a custom cost function for routing algorithms. The weight is calculated 
    based on travel time and an added penalty proportional to safety perception (dpsafe),
    adjusted by cycling speed and infrastructure.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        The street network graph to update.
    typ : str
        Routing type: 'safest', 'flattest', 'combo', or 'shortest' (default).
    VOS : float
        Value of Safety — a coefficient that translates safety perception into distance penalty.
        Default is 20.
    vcycle : float, optional
        Average cycling speed in cycle highways (km/h). Default is 20.
    vmixed : float, optional
        Average cycling speed in mixed traffic (km/h). Default is 10.
    vlane : float, optional
        Average speed in bike lanes (km/h). Default is 15.
    cpsafe: int, optional
            The threshold level. The default is equal to 7

    Returns
    -------
    networkx.MultiDiGraph
        The graph `G`, with a new edge attribute `VOSweight` added.

    """
    
    vmixed_m_s = vmixed * 1000/3600
    vcycle_m_s = vcycle * 1000/3600

    
    v_speed = vmixed_m_s
        
    for u, v_, k, data in G.edges(keys=True, data=True):
        length = data.get("length", 0)  # in meters

        # Default values
        sl = 1
        dpsafe = 0
        inf = data.get('inf', 0)
        
        if inf in ['3: Urban road with cycle lane']: v_speed = vcycle_m_s

        if typ in ['safest', 'combo']:
            psafe = data.get('psafe', 0)
            dpsafe = psafe - cpsafe
        
        # print(dpsafe)
        # Placeholder: slope can be used in future
        if typ in ['flattest', 'combo']: sl = 1  # TODO: ADD SLOPE PENALTY IF AVAILABLE

        data["VOSweight"] = (1 / sl) * ((length / v_speed) + (VOS * dpsafe) / vcycle_m_s)

    return G

def accurate_path_length(G, path, weight='length'):
    total = 0
    for u, v in zip(path[:-1], path[1:]):
        # Get the attributes for all edges between u and v
        edges = G.get_edge_data(u, v)

        # Select the edge with the *minimum weight*
        min_weight = min(attr.get(weight, 0) for attr in edges.values())
        total += min_weight
    return total

def shortPath(G, orig, dest, w = 'length', mapCheck = False, distAssignCheck = False):
    
    """
        Compute the shortest path between two geographic coordinates in a graph.
        
        Parameters
        ----------
        G : networkx.MultiDiGraph
            The street network graph (typically from OSMnx).
        orig : tuple
            The origin node as id.
        dest : tuple
            The destination node as id.
        w : str, optional
            The edge attribute to minimize during routing (default is 'length').
        mapCheck : bool, optional
            If True, plots the route on the graph (default is False).
        
        Returns
        -------
        path : list
            A list of node IDs representing the shortest path.
        length : float
            The total geometric length (in meters) of the computed path, based on edge 'length' attributes.
        
        Notes
        -----
        This function uses Dijkstra’s algorithm via NetworkX’s `single_source_dijkstra` 
        and relies on OSMnx for node matching and visualization.
    """
    
    path = nx.shortest_path(G, source=orig, target=dest, weight=w)
    
    # length = sum(
    #     G[u][v][min(G[u][v])].get("length", 0)
    #     for u, v in zip(path[:-1], path[1:])
    # )
    
    length = accurate_path_length(G, path, weight = 'length')
    
    if mapCheck: 
        ox.plot_graph_route(G, path, 
                            route_linewidth=4, node_size=0, 
                            bgcolor='white')
    return path, length

def simulateVOS(mean, std_dev, n_samples=1000, seed=None):
    """
    Simulates strictly negative VOS values from a normal distribution
    by rejecting and resampling positive or zero values.

    Parameters
    ----------
    mean : float
        Mean of the normal distribution.
    std_dev : float
        Standard deviation of the normal distribution.
    n_samples : int, optional
        Number of negative samples to generate.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        Array of strictly negative VOS values.
    """
    if seed is not None:
        np.random.seed(seed)

    results = []
    while len(results) < n_samples:
        samples = np.random.normal(loc=mean, scale=std_dev, size=n_samples)
        negatives = samples[samples < 0]
        results.extend(negatives.tolist())
    
    return np.array(results[:n_samples])

# Analysis funs
def InfaBreakdown(G, path):
    """
    Computes the total length of each infrastructure type along a path.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        The graph with edge attributes including 'inf' and 'length'.
    path : list
        A list of node IDs representing the route.

    Returns
    -------
    dict
        A dictionary with infrastructure types as keys and total lengths (in meters) as values.
    """
    inf_lengths = defaultdict(float)

    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v)
        
        if edge_data is None:
            continue

        # Select the first edge if multiple exist (you can refine this as needed)
        edge = min(edge_data.values(), key=lambda x: x.get('length', 0))
        inf_type = edge.get('inf', 'unknown type')
        # print(inf_type)
        length = edge.get('length', 0)
        # print(length)
        inf_lengths[inf_type] += length

    return dict(inf_lengths)

def stackInfrastructure(G, path1, path2, station_name_i=None, station_name_j=None):
    """
    Visualizes the infrastructure breakdown of two paths using a stacked bar plot.

    Parameters
    ----------
    G : networkx.Graph
        The graph representing the transportation network.

    path1 : list
        A list of node IDs representing the first path (typically the shortest path).

    path2 : list
        A list of node IDs representing the second path (typically the safest path).

    station_name_i : str, optional
        Name of the origin station. Used in the plot title.

    station_name_j : str, optional
        Name of the destination station. Used in the plot title.

    Returns
    -------
    None
        Displays a matplotlib plot comparing the lengths of different types of infrastructure
        used in both paths. Each infrastructure type is color-coded and annotated with its length.
    """
    # Infrastructure color mapping
    color_dict = {
        '1: Urban road with sidewalk less than 1.5 m wide': '#E31A1C',
        '2: Urban road with sidewalk more than 1.5 m wide': '#FF7F00',
        '3: Urban road with cycle lane': '#0000FF',
        '4: Shared space': '#1DD083',
        'unknown type': 'grey'
    }

    # Compute infrastructure breakdowns for both paths
    path1_infra = InfaBreakdown(G, path1)
    path2_infra = InfaBreakdown(G, path2)

    # Convert to DataFrames and merge
    df_path1 = pd.DataFrame.from_dict(path1_infra, orient='index', columns=['Shortest Path'])
    df_path2 = pd.DataFrame.from_dict(path2_infra, orient='index', columns=['Safest Path'])
    df = pd.merge(df_path1, df_path2, left_index=True, right_index=True, how='outer').fillna(0)
    df = df.T  # Transpose so rows are paths, columns are infrastructure types

    # Ensure column order matches color_dict
    df = df[[k for k in color_dict.keys() if k in df.columns]]

    # Plotting setup
    colors = [color_dict[col] for col in df.columns]
    fig, ax = plt.subplots(figsize=(10, 6), dpi=500)
    bottom = np.zeros(len(df))

    # Plot stacked bars with annotation
    for col in df.columns:
        values = df[col].values
        bars = ax.bar(df.index, values, bottom=bottom, color=color_dict[col], label=col)

        # Annotate each segment with bold white text
        for bar, value, btm in zip(bars, values, bottom):
            if value > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    btm + value / 2,
                    f"{value:.0f}",
                    ha='center',
                    va='center',
                    fontsize=8,
                    color='white',
                    fontweight='bold'
                )
        bottom += values

    # Axis formatting and labels
    ax.set_ylabel("Length (m)")
    ax.set_xlabel("")
    title = ""
    if station_name_i and station_name_j:
        title += f"from {station_name_i} to {station_name_j}"
    ax.set_title(title)
    ax.set_xticks(range(len(df.index)))
    ax.set_xticklabels(df.index, rotation=0)

    # Adjust layout for legend outside plot
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    ax.legend(title="Infrastructure Type", loc='center left', bbox_to_anchor=(1.0, 0.5))

    # Display the plot
    plt.show()

def descrStats_stations(df, normalize = False):
    """
    Computes descriptive statistics for the 'vos' and 'difference' columns, grouped by origin bike-sharing station ('from').

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns 'from', 'vos', 'difference', and optionally 'slength'. The 'from' column represents the origin station,
        and the 'difference' column represents the difference between the safest and shortest paths.
    
    normalize : bool, optional, default=False
        If True, the 'difference' will be normalized by dividing by the 'slength' column, creating a new 'rel_difference' column.
        If False, the 'difference' column will be used directly for the descriptive statistics.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the descriptive statistics (count, mean, std, min, 25%, 50%, 75%, max) for the 'difference' 
        (or 'rel_difference' if normalized) for each origin station ('from').
    """

    if normalize:
        x = "rel_difference"
        df[x] = df["difference"]/df["slength"]
        # Group by origin station ('from')
    else:
        x = "difference"
    
    grouped = df.groupby('from')
    stats = grouped[[x]].describe()
    
    return stats

def genHist(df, bins=100):
    """
    Plots a histogram for all the 'difference' values in the dataframe,
    adds a trend line and marks the mean.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with the 'difference' column.
    bins : int, optional
        Number of bins for the histogram (default is 100).
    """
    plt.figure(figsize=(10, 6), dpi=500)
    
    # Histogram
    sns.histplot(df['difference'], bins=bins, kde=True, 
                 color='red', edgecolor='black', alpha = 0.4)

    # Compute mean and draw vertical line
    mean_val = df['difference'].mean()
    plt.axvline(mean_val, color='black', linestyle='--', linewidth=1.5, label=f"Mean = {mean_val:.2f}")

    # Labels
    plt.xlabel('length difference in m (safest - fastest path)', fontsize=12)
    plt.ylabel('frequency', fontsize=12)
    # plt.title('Histogram with Density and Mean Line', fontsize=14)
    # plt.legend()

    plt.show()

def VOS_mean_max_double_plot(df):
    """
    Creates a side-by-side plot showing the maximum and mean 'difference' for each unique 'vos' value.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with 'vos' and 'difference' columns.
    """
    # Group by VOS and compute mean and max difference
    grouped = df.groupby('vos')['difference'].agg(['mean', 'max']).reset_index()

    # Sort by VOS to ensure line continuity
    grouped = grouped.sort_values('vos')

    # Create subplots (two side-by-side)
    fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(15, 6), dpi=500)

    # Plot the max difference on the left plot
    ax1.plot(grouped['vos'], grouped['max'], label='Max Difference', color='red', linewidth=2)
    ax1.set_title('Maximum values', fontsize=14)
    ax1.set_xlabel('VOS in m', fontsize=12)
    ax1.set_ylabel('length difference in m (safest - shortest path)', fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Plot the mean difference on the right plot
    ax2.plot(grouped['vos'], grouped['mean'], label='Mean Difference', color='blue', linewidth=2)
    ax2.set_title('Mean values', fontsize=14)
    ax2.set_xlabel('VOS in m', fontsize=12)
    ax2.set_ylabel('length difference in m (safest - shortest path)', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.5)

    # Show legends
    # ax1.legend(loc='upper left')
    # ax2.legend(loc='upper left')

    # Show the plot
    plt.tight_layout()
    plt.show()

def bShareMapDiff(bShare, stats, links, legend_title="Mean Difference", size_factor=400):
    """
    Plots a map of Munich's bike sharing stations with circle sizes based on the mean difference value, 
    and overlays the network of links. It also adds CRS and grid information to the plot.

    Parameters
    ----------
    bShare : geopandas.GeoDataFrame
        GeoDataFrame containing bike sharing stations, with at least 'NAME' (station names) and geometry columns.
    
    stats : pandas.DataFrame
        DataFrame containing statistics, with 'mean' values indexed by station names.
    
    links : geopandas.GeoDataFrame
        GeoDataFrame containing the links between bike sharing stations (edges), with geometry information.
    
    legend_title : str, optional, default="Mean Difference"
        The title for the legend.
    
    size_factor : float, optional, default=400
        The factor by which the circle size is scaled based on the 'mean' column values.

    Returns
    -------
    None
        Displays the plot without returning any values.
    """
    # Merge bike sharing data with statistics
    merged = bShare.merge(stats[['mean']], left_on='NAME', right_index=True)

    # Define colormap and calculate sizes based on mean values
    cmap = 'plasma_r'
    merged["sizes"] = merged['mean'] * size_factor

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), dpi=500)

    # Plot bike sharing stations as circles based on 'mean' column
    merged.plot(ax=ax, column='mean', cmap=cmap, legend=True,
                legend_kwds={'label': legend_title, 'shrink': 0.7},
                markersize='sizes', edgecolor='black', zorder=2, alpha=0.6)

    # Plot links in the background
    links.plot(ax=ax, color='lightgrey', linewidth=0.8, alpha=0.7, zorder=1)

    # Show grid
    ax.axis('on')  # Keep axes visible for grid
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

    # CRS information (bottom-left)
    crs_info = merged.crs.to_string() if merged.crs else 'CRS information not available'
    plt.text(0.01, 0.01, f'CRS: {crs_info}', transform=ax.transAxes,
             fontsize=14, ha='left', va='bottom', bbox=dict(facecolor='white', alpha=0.7))

    # Set plot title
    ax.set_title("Munich bike sharing stations", fontsize=14)

    # Show the plot
    plt.show()

def path_to_shapefile(G, path, prefix, out_dir):
    
    """
    Save the nodes and edges of a path from a NetworkX graph to shapefiles.
    
    Parameters
    ----------
    G : networkx.Graph or networkx.MultiGraph
        A graph where nodes contain 'x' and 'y' coordinates, and edges may contain a 'geometry' attribute.
    
    path : list
        An ordered list of node IDs representing the path to be saved.
    
    prefix : str
        A prefix used to name the output shapefiles. Output files will be named as:
        - <prefix>_edges.shp
        - <prefix>_nodes.shp
    
    out_dir : str
        Directory path where the shapefiles will be saved.
    
    Notes
    -----
    - Nodes are saved as a Point geometry with an attribute 'node' for their ID.
    - Edges are saved as LineString geometries with 'from' and 'to' attributes.
    - If an edge does not have a 'geometry' attribute, a straight LineString is created from node coordinates.
    - Coordinate Reference System (CRS) is set to EPSG:4326 (WGS 84).
    """

    # Save edges
    edge_geoms = []
    edge_attrs = []

    for u, v in zip(path[:-1], path[1:]):
        data = G.get_edge_data(u, v)
        if data:
            edge = data[0]  # If MultiGraph, take first edge
            geom = edge.get('geometry', LineString([ (G.nodes[u]['x'], G.nodes[u]['y']), (G.nodes[v]['x'], G.nodes[v]['y']) ]))
            edge_geoms.append(geom)
            edge_attrs.append({'from': u, 'to': v})

    gdf_edges = gpd.GeoDataFrame(edge_attrs, geometry=edge_geoms, crs='EPSG:4326')
    gdf_edges.to_file(os.path.join(out_dir, f'{prefix}_edges.shp'))

    # Save nodes
    node_geoms = []
    node_attrs = []

    for node in path:
        x, y = G.nodes[node]['x'], G.nodes[node]['y']
        node_geoms.append(Point(x, y))
        node_attrs.append({'node': node})

    gdf_nodes = gpd.GeoDataFrame(node_attrs, geometry=node_geoms, crs='EPSG:4326')
    gdf_nodes.to_file(os.path.join(out_dir, f'{prefix}_nodes.shp'))

def top5pairs(df, normalize=False, top_n=5):
    """
    Finds the top N station pairs (by 'id') with the highest maximum 'difference' or 'rel_difference' across VOS values.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with repeated rows per 'id', containing columns 'id', 'from', 'to', 'vos', 'difference', 'slength', and optionally 'rel_difference'.
    
    normalize : bool, default=False
        If True, compute 'rel_difference' as difference / slength before ranking.

    top_n : int, default=5
        Number of top 'id's to return based on the highest maximum score.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the top N rows (one per 'id'), including all original columns, ranked by the selected metric.
    """
    df = df.copy()

    if normalize:
        df["rel_difference"] = df["difference"] / df["slength"]
        metric = "rel_difference"
    else:
        metric = "difference"

    # Compute variance per id
    var_df = df.groupby('id').agg(
        variance=(metric, 'var'),
        from_station=('from', 'first'),
        to_station=('to', 'first')
    ).reset_index()

    # Get top N by variance
    top_var = var_df.sort_values(by='variance', ascending=False).head(top_n)

    return top_var

def stackInfrastructureMulti2(G, paths, labels=None, station_name_i=None, station_name_j=None):
    """
    Visualizes the infrastructure breakdown for multiple paths as a 100% stacked bar plot.

    Parameters
    ----------
    G : networkx.Graph
        The graph representing the transportation network.

    paths : list of lists
        A list of paths, where each path is a list of node IDs.

    labels : list of str, optional
        A list of labels for each path (e.g., 'Shortest Path', 'Safest Path').
        If not provided, generic labels like 'Path 1', 'Path 2', ... will be used.

    station_name_i : str, optional
        Name of the origin station. Used in the plot title.

    station_name_j : str, optional
        Name of the destination station. Used in the plot title.

    Returns
    -------
    None
        Displays a matplotlib 100% stacked bar plot comparing the proportion of infrastructure
        types used in each path.
    """
    # Color dictionary
    color_dict = {
        '1: Urban road with sidewalk less than 1.5 m wide': '#E31A1C',
        '2: Urban road with sidewalk more than 1.5 m wide': '#FF7F00',
        '3: Urban road with cycle lane': '#0000FF',
        '4: Shared space': '#1DD083',
        'unknown type': 'grey'
    }

    # Generate labels if needed
    if labels is None:
        labels = [f'Path {i+1}' for i in range(len(paths))]

    # Build path breakdown DataFrame
    df_list = []
    for path, label in zip(paths, labels):
        breakdown = InfaBreakdown(G, path)
        df = pd.DataFrame.from_dict(breakdown, orient='index', columns=[label])
        df_list.append(df)

    df = pd.concat(df_list, axis=1).fillna(0).T

    # Normalize each row to 100%
    df_pct = df.div(df.sum(axis=1), axis=0) * 100

    # Keep color order
    df_pct = df_pct[[k for k in color_dict if k in df_pct.columns]]
    colors = [color_dict[col] for col in df_pct.columns]

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6), dpi=500)
    bottom = np.zeros(len(df_pct))

    for col in df_pct.columns:
        values = df_pct[col].values
        bars = ax.bar(df_pct.index, values, bottom=bottom, color=color_dict[col], label=col)
        for bar, value, btm in zip(bars, values, bottom):
            if value > 3:  # Only label if it's a big enough slice
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    btm + value / 2,
                    f"{value:.0f}%",
                    ha='center',
                    va='center',
                    fontsize=8,
                    color='white',
                    fontweight='bold'
                )
        bottom += values

    # Title
    title = ""
    if station_name_i and station_name_j:
        title = f"100% Infrastructure Composition: {station_name_i} → {station_name_j}"
    ax.set_title(title)
    ax.set_ylabel("Percentage of Path (%)")
    ax.set_xticks(range(len(df_pct.index)))
    ax.set_xticklabels(df_pct.index, rotation=90)

    # Legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    ax.legend(title="Infrastructure Type", loc='center left', bbox_to_anchor=(1.0, 0.5))

    plt.show()