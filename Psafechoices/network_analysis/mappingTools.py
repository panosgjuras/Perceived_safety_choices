import copy
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap

import seaborn as sns
import geopandas as gpd
from shapely.geometry import LineString, Point

def infMapping(links, scen):
    
    """
    Useful function to understand the spatial variations of infrassture types

    Parameters
    ----------
    links : dataFrame
        The gpd dataFrame with all the links. The links must have 'inf' and 'pav'
    scen : str
        The scenario, this is used for the title of the figure

    Returns
    -------
    A map plot with the infrastructure types
    """
    
    
    # Color mappings for 'inf' and 'pav'
    inf_color_mapping = {
        '1: Urban road with sidewalk less than 1.5 m wide': '#BF1A23',  # Dark Red
        '2: Urban road with sidewalk more than 1.5 m wide': '#E3801A',  # Orange
        '3: Urban road with cycle lane': '#2A14BE',  # Blue
        '4: Shared space': '#55C896',  # Green
    }

    pav_color_mapping = {
        '0: bad condition': '#FF1493',  # Pink for bad condition
        '1: good condition': '#FFD700',  # Yellow for good condition
    }

    # Map the 'inf' and 'pav' columns to the corresponding colors
    links['inf_color'] = links['inf'].map(inf_color_mapping)
    links['pav_color'] = links['pav'].map(pav_color_mapping)

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 10), dpi=500)
        
    # Plot 'pav' layer first for transparency effect
    links.dropna(subset=['pav_color']).plot(ax=ax, facecolor="none",
                                            edgecolor=links['pav_color'], 
                                            linewidth=1.5,  # Thicker line for pav condition
        alpha=0.1,
        label = 'Infrastructure'# More transparent for background effect
    )

    links.dropna(subset=['inf_color']).plot(
        ax=ax,
        facecolor="none",
        edgecolor=links['inf_color'],
        linewidth=0.25,
        alpha = 1, # Thinner line for inf condition
        label = 'Pavement'
    )
    
    # cross.plot(ax=ax, edgecolor="blue", facecolor="lightblue", alpha=0.5, linewidth=10)

    # Add grid and labels
    ax.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.title(scen, fontsize=15)
    ax.set_xlabel('X-coordinate (m)')
    ax.set_ylabel('Y-coordinate (m)')
    
    ax.legend(title="Legend", loc='upper right')

    # Display plot
    plt.show()

def plotPsafeLev(gdf, mod, xy=2, city = 'Athens', font = 20):
    """
    This function create the maps with the perceived safety scores
    
    Parameters
    ----------
    gdf : dataframe, the shapefile with all the links
    mod : sting variable, the transport mode
    xy : integer variable to play with the size of the maps
        DESCRIPTION. The default is 2.

    Returns
    -------
    maps with the perceived safety scores per link

    """
    
    fixcolors = {"1.0": "#e31a1c", "2.0": "#f65d09", "3.0": "#d0a41d",
                 '4.0': "#73ee57", "5.0": "#53c3b1", "6.0": "#2d73d1",
                 "7.0": "#0000b7"} # this is the standard colorMap I used in the analysis
    text = "LevPsafe" + mod
    gdf[text] = gdf[text].astype(str) # I change to string, because it mess up the categories
    # It is a huge problem I have
    unique_levels = gdf['LevPsafe' + mod].unique()
    # Sort the levels
    sorted_levels = sorted(unique_levels.astype(str))
    # Create a colormap using fixed colors
    cmap = ListedColormap([fixcolors[category] for category in sorted_levels])

    plt.figure(figsize=(10 * xy, 6 * xy), dpi=500) # I maximized the dpi to 500, it can be smaller
    ax = plt.gca()  # Get current axis
    gdf.plot(column=text, cmap=cmap, legend=True, ax=ax, linewidth = 0.75)
    
    # Set plot title and axis labels
    ax.set_title('Psafe of ' + mod + ' in ' + city, fontsize = font)
    ax.set_xlabel('X-coordinate (m)', fontsize = font) # x-axis label
    ax.set_ylabel('Y-coordinate (m)', fontsize = font)
    
    ax.tick_params(axis='both', which='major', labelsize=font)

    # ax.legend()
    
    crs_info = gdf.crs.to_string() if gdf.crs else 'CRS information not available'
    plt.text(0.01, 0.01, f'CRS: {crs_info}', transform=ax.transAxes,
         fontsize=20, ha='left', va='bottom', bbox=dict(facecolor='white', alpha=0.7))
    
    plt.show()

def PsafeHeatmaps(gdf, mod, city = 'Athens', pmin = 4, xy = 2, font = 20):
    """
    It creates a planar heatmap with the concetration of high perceived safety scores

    Parameters
    ----------
    points : dataframe, with the mid points of each link
    mod : sting variable, the transport mode
    pmin : integer, it is the threshold, higher than this, the perceived safety level is acceptable
        DESCRIPTION. The default is 4.
    xy : integer variable to play with the size of the maps
         DESCRIPTION. The default is 2.

    Returns
    -------
    planar heatmaps per transport mode

    """
    
    def calculate_midpoint_coords(geometry):
        if isinstance(geometry, LineString):
            midpoint = geometry.interpolate(0.5, normalized=True)
            return midpoint.x, midpoint.y
        return None, None
    
    links = copy.deepcopy(gdf)
    
    gdf['xmid'], gdf['ymid'] = zip(*gdf['geometry'].apply(calculate_midpoint_coords))
    geometry = [Point(xy) for xy in zip(gdf['xmid'], gdf['ymid'])] # x-mid, y-mid refer to the mid point of each link
    points = gpd.GeoDataFrame(gdf, geometry=geometry)
    points.crs = gdf.crs # this is the CRS I used in the points tooo
    
    df = points.loc[points['LevPsafe' + mod] >= pmin] # this keeps only the points higher than the threshold
    # df = df.loc[df['modes'].str.contains(mod)] # this keep only the points associated with links that you can travel used the trasnport mode mod
    plt.figure(figsize=(20, 20), dpi = 500)
    axis = sns.kdeplot(x = df.xmid, y = df.ymid,
                fill=True, bw_adjust = 0.3, weights = points['LevPsafe' + mod], # the score the weight of each point, so level 7 more important
                cmap = "plasma")
    links.plot(ax = axis, facecolor = "none", edgecolor = "grey", linewidth = 0.75)
    plt.title('Psafe Hetmamp for ' + city + ' - ' + mod + ', level ' + str(copy.deepcopy(pmin)) + ' or greater',
              fontsize = font) # function for a crazy title
    plt.xlabel('X-coordinate (m)', fontsize = font)
    plt.ylabel('X-coordinate (m)', fontsize = font)
    # plt.tick_params(labelsize = font)
    
    crs_info = gdf.crs.to_string() if gdf.crs else 'CRS information not available'
    plt.text(0.01, 0.01, f'CRS: {crs_info}', transform=plt.gca().transAxes,
         fontsize=20, ha='left', va='bottom', bbox=dict(facecolor='white', alpha=0.7))
    
    plt.show()