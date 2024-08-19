import pandas as pd
import os
import geopandas as gpd
from pyproj import CRS
import ast
import warnings
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.colors as mcolors
import copy

from shapely.geometry import Point, LineString
from Psafechoices.network_analysis import traffic_params_upd as trfp

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)

def read_points(path: str) -> pd.DataFrame:
    points = pd.read_csv(path, delimiter=";")
    print(len(points))
    return points


root_dir = os.path.dirname(os.path.realpath(__file__))
path_points = os.path.join(root_dir, 'logistNet')
points = read_points(os.path.join(path_points, 'depot_delpoints_ATHENS.csv'))

scen_dir = '/Users/panosgtzouras/Desktop/github_tzouras/Perceived_safety_choices/scenario_athens'
scenario = 'scenario0'
nod_link = os.path.join(scen_dir, 'shapefiles', 'nodes',
                        'experimental_field_athens_nodes.shp')
nodes = trfp.read_shapefile(nod_link)


def DepotDelpointShp(points, nodes, tt, path=root_dir):
    # x = 'depot'
    df = pd.DataFrame(columns={'id', 'x_coord', 'y_coord'})
    df['x_coord'] = 0
    df['y_coord'] = 0
    df['id'] = points[tt].unique()
    for index, row in df.iterrows():
        node = nodes[nodes['id'] == row['id']]
        if not node.empty:
            df.at[index, 'x_coord'] = node['x'].values[0]
            df.at[index, 'y_coord'] = node['y'].values[0]

    # Print the updated dataframe
    # print(df)

    # Create a list of Point objects using x_coord and y_coord columns
    geometry = [Point(x, y) for x, y in zip(df['x_coord'], df['y_coord'])]

    # Create a GeoDataFrame using the geometry column
    gdf = gpd.GeoDataFrame(df, geometry=geometry,
                           crs=CRS.from_user_input('EPSG:2100'))

    # Save the GeoDataFrame as a shapefile
    file_name = tt + '.shp'
    gdf.to_file(os.path.join(path, 'shapefiles', file_name))


# DepotDelpointShp(points, nodes, 'depot')
# DepotDelpointShp(points, nodes, 'delpoint')

netdf = pd.read_csv(os.path.join(root_dir, 'NETfile', "net_file_ATHENS.csv"))
# netdf = netdf.loc[netdf.path != 'no path']

def newNetShp(netdf, nodes, pth=root_dir, typ = 'intermediate'):
    ldf = netdf.merge(nodes, left_on='from1', right_on='id')
    ldf = ldf.merge(nodes, left_on='to1', right_on='id',
                    suffixes=('_start', '_end'))
    ldf = ldf[ldf['from1'] != ldf['to1']]
    ldf = ldf.reset_index()
    
    geometry = []
    # print(len(ldf))
    for i in range(len(ldf)):
        pp = ast.literal_eval(ldf.loc[i, 'path'])
        pp = [int(value) if isinstance(value, float)
                  else value for value in pp]
        
        if typ == 'intermediate':
            path_points = [Point(nodes.loc[nodes.id == node_id, 'x'],
                                 nodes.loc[nodes.id == node_id, 'y']) for node_id in pp]
            geom = LineString(path_points)
            geometry.append(geom)
        else:
            path_points = [Point(nodes.loc[nodes.id == pp[0], 'x'],
                                nodes.loc[nodes.id == pp[0], 'y'],)]
            print(path_points)
            
            point1 = Point(nodes.loc[nodes.id == pp[0], 'x'],
                                nodes.loc[nodes.id == pp[0], 'y'])
                                
            point2 = Point(nodes.loc[nodes.id == pp[len(pp)-1], 'x'],
                                nodes.loc[nodes.id == pp[len(pp)-1], 'y'])
                                
            geom = LineString([point1, point2])
            geometry.append(geom)
        
    

    gdf = gpd.GeoDataFrame({'pid': ldf['pid'], 'from1': ldf.from1.astype(int), 'to1': ldf.to1.astype(int),
                            'geometry': geometry,
                            'wavg_psafe': ldf.wavg_psafe,
                            'sdist': ldf.sdist,
                            'sumlentype1': ldf.sumlentype1,
                            'sumlentype2': ldf.sumlentype2,
                            'sumlentype3': ldf.sumlentype3,
                            'sumlentype4': ldf.sumlentype4
                            },
                            crs=CRS.from_user_input('EPSG:2100'))

    gdf.to_file(os.path.join(pth, 'shapefiles', 'links.shp'))

    return gdf


routes = newNetShp(netdf, nodes)

def get_value2(value1):
    
    data1 = [30, 27, 29, 7, 5, 22, 21, 24]
    data2 = [116, 109, 114, 162, 159, 84, 76, 95]
    data3 = [33, 1, 32, 3, 26, 13, 4, 10, 9, 2]
    data4 = [127, 135, 254, 141, 229, 52, 150, 44, 41, 139]
    data5 = [23, 18, 19, 16, 20, 17, 15, 31]
    data6 = [217, 196, 197, 186, 204, 194, 184, 245]
    data7 = [28, 8, 11, 14]
    data8 = [239, 168, 172, 181]
    
    df1 = pd.DataFrame({'Value 1': data1, 'Value 2': data2})
    df2 = pd.DataFrame({'Value 1': data3, 'Value 2': data4})
    df3 = pd.DataFrame({'Value 1': data5, 'Value 2': data6})
    df4 = pd.DataFrame({'Value 1': data7, 'Value 2': data8})

    df = pd.concat([df1, df2, df3, df4], ignore_index=True)

    
    value2 = df.loc[df['Value 1'] == value1, 'Value 2'].values
    if len(value2) > 0:
        return value2[0]
    else:
        return None

def formSol(opt):
    sol = pd.DataFrame(columns=['depot', 'path1', 'path2', 'path3'])
    sol['depot'] = [80000, 20000, 30000, 60000]

    for i, paths in enumerate(opt):
        sol.loc[i, 'path1'] = str(paths[0])
        if len(paths) > 1:
            new_row = sol.loc[i].copy()
            new_row['path1'] = str(paths[1])
            sol = sol.append(new_row, ignore_index=True)
            # sol = pd.concat([sol, new_row], ignore_index= True)

    sol = sol.drop(['path2', 'path3'], axis=1)
    sol = sol.rename(columns={'path1': 'path'})  # Rename the 'path1' column to 'path'
    return sol


def OptRoutes(routes, sol):
    
    step = 50
    
    df_result = pd.DataFrame(columns=['from1', 'to1', 'depot', 'packages'])

    # Iterate over the rows in the 'sol' dataframe
    for index, row in sol.iterrows():
        path = ast.literal_eval(row['path'])  # Convert the path from string to list
    #   line_coords = []
         
        # Add the depot as the starting point of the sequence
        depot = row['depot']
        pckg = step * len(path)
    
        # print({'from1': depot, 'to1': path[0], 'depot': depot,
        #                                  'packages': pckg})
    
        df_result = df_result.append({'from1': depot, 'to1': path[0], 'depot': depot,
                                      'packages': pckg}, ignore_index=True)
       
        for i, node_id in enumerate(path):
            node_id = get_value2(node_id)
            
            # Get the node IDs before and after
            node_before = path[i] if i >= 0 else depot
            node_after = path[i+1] if i < len(path)-1 else depot
            
            pckg = pckg - step
        
            # print({'from1': node_before, 'to1': node_after, 
            #        'depot': depot, 'packages': pckg})
        
            # Add the node IDs to the dataframe
            df_result = df_result.append({'from1': node_before, 'to1': node_after, 
                                          'depot': depot, 'packages': pckg}, ignore_index=True)

    # print(df_result)
    df_result.from1 = df_result.from1.astype(int)
    df_result.to1 = df_result.to1.astype(int)
    df_result.depot = df_result.depot.astype(int)

    for i in range(0, len(df_result)):
        if df_result.loc[i, 'from1'] < 10000:
            df_result.loc[i, 'from1'] = get_value2(df_result.loc[i, 'from1'])
        if df_result.loc[i, 'to1'] < 10000:
            df_result.loc[i, 'to1'] = get_value2(df_result.loc[i, 'to1'])
            
    merged_df = pd.merge(df_result, routes, how='inner', left_on=['from1', 'to1'], right_on=['from1', 'to1'])

    filtered_routes = merged_df[['pid', 'from1', 'to1', 'depot', 'wavg_psafe', 'sdist','packages', 
                                 'sumlentype1', 'sumlentype2', 'sumlentype3', 'sumlentype4',
                                 'geometry']]

    # print(filtered_routes)

    ngdf = gpd.GeoDataFrame(filtered_routes,crs=CRS.from_user_input('EPSG:2100'))
    
    return ngdf

def lighten_color(color, amount=0.3):
    """
    Lighten the given color by multiplying the RGB values by the specified amount.
    """
    color = mcolors.to_rgb(color)
    lighter_color = [min(c + (1 - c) * amount, 1) for c in color]
    return lighter_color

def totalStackBar(dataframes, column_names = ['scenario', 'depot'], 
                  scale = 1, palette='coolwarm', dpi = 400):
    sns.set_theme(style="ticks")
    combined_df = pd.concat(dataframes)
    
    # Group the data by scenario and depot, and calculate the sum of the specified column for each group
    grouped_df = combined_df.groupby(column_names)['sdist'].sum().reset_index()

    # Get unique scenarios and depots
    scenarios = grouped_df[column_names[0]].unique()
    depots = grouped_df[column_names[1]].unique()

    # Set the figure size
    figsizes = (12 * scale, 8 * scale)
    plt.figure(figsize= figsizes, dpi = dpi)
    
    fontsize = 9 * (figsizes[0] / 10)
    
    plt.rcParams.update({'font.size': fontsize})

    # Define the original color palette
    # original_colors = ["#33A02C", "#011FFF", "#E31A1C", "#FF01C8"]
    
    original_colors = ["#011FFF", "#E31A1C", "#FF01C8", "#33A02C"]

    # Generate a lighter version of each color
    colors = [lighten_color(color, amount=0.7) for color in original_colors]
    
    # Plot the stacked bar chart
    x = np.arange(len(scenarios))  # x-axis values
    width = 0.8  # width of the bars
    bottom = np.zeros(len(scenarios))  # bottom values for the bars

    # Loop through each depot and create a stacked bar for each scenario
    for i, depot in enumerate(depots):
        values = grouped_df[grouped_df[column_names[1]] == depot]['sdist'].tolist()

        plt.bar(x, values, width, bottom=bottom, label=depot, alpha = 1, color=colors[i], edgecolor=".1")

        # Annotate the values on each bar
        for j, value in enumerate(values):
            plt.annotate(f'{value:.2f}', (x[j], bottom[j] + value / 2), ha='center', va='center')

        # Update the bottom values for the next depot
        bottom += values

    # Set the x-axis tick labels
    # plt.xticks(x, scenarios)
    
    xl = ["0", "600", "1200", "1800", "2400", "3000", "3600", "4200"]
    plt.xticks(range(len(xl)), xl)

    # Set the labels and title
    plt.xlabel('Value of Safety in meters')
    plt.ylabel('Total network distance in meters')
    # plt.title('Stacked Bar Chart - Sum Distance per {}'.format(column_names[0]))

    # Set the legend
    plt.legend()

    # Show the plot
    plt.show()
    
    return plt

def wavgPckgLine(dataframes, column_names = ['scenario', 'depot'], 
                 scale = 1.5, dpi = 400):
    sns.set_theme(style="ticks")
    combined_df = pd.concat(dataframes)
    combined_df['pckgDist'] = combined_df['sdist'] * combined_df['packages']

    sum_pckgDist_per_depot = combined_df.groupby(column_names)['pckgDist'].sum()
    max_pckgDist_per_depot = combined_df.groupby(column_names)['packages'].max()
    wavg_pckgDist_per_depot = sum_pckgDist_per_depot/max_pckgDist_per_depot
    print(wavg_pckgDist_per_depot)

    plt.figure(figsize=(10 * scale, 6 * scale), dpi = dpi)

    # Plot a line for each depot with different colors
    depots = combined_df['depot'].unique()
    original_colors = ["#33A02C", "#011FFF", "#E31A1C", "#FF01C8"]
    
    colors = original_colors
    
    for i, depot in enumerate(depots):
        depot_data = wavg_pckgDist_per_depot.loc[:, depot]
        plt.plot(depot_data.index, depot_data.values, marker='o', linestyle='dashed', linewidth=3.0, label=depot, color=colors[i])
        
        # Annotate the value at each point with two digits precision
        for x, y in zip(depot_data.index, depot_data.values):
            plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # Set the x-axis tick labels as scenarios
    # plt.xticks(range(len(depot_data.index)), depot_data.index)
    
    xl = ["0", "600", "1200", "1800", "2400", "3000", "3600", "4200"]
    plt.xticks(range(len(xl)), xl)
    

    # Set the labels and title
    plt.xlabel('Value of Safety in meters')
    plt.ylabel('Average distance per package in meters')
    # plt.title('Sensitivity anal')

    # Set the legend
    plt.legend()

    # Show the plot
    plt.show()
    return plt


def outputShpOpt(scen, routes = routes, root_dir = root_dir):
    if scen == 'sdist':
        opt = [[[21, 27, 29, 22], [30, 7, 5, 24]],[[1, 32, 26, 33, 2], [13, 3, 4, 9, 10]],[[23, 20, 18, 19], [15, 16, 17, 31]],[[28, 8, 11, 14]]]
        # opt = 0
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'avgslodist':
        opt = [[[]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_600':
        opt = [[[7, 5, 27, 29], [21, 30, 22, 24]],[[33, 26, 32, 1], [13, 10, 4, 2, 3, 9]],[[23, 20, 19, 18], [16, 17, 31, 15]] ,[[8, 28, 11, 14]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_1200':
        opt = [[[21, 30, 22, 24], [5, 7, 27, 29]],[[3, 9, 13, 10, 4], [1, 33, 26, 32, 2]],[[19, 23, 20, 18], [16, 17, 31, 15]],[[8, 28, 11, 14]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_1800':
        opt = [[[5, 27, 29, 24], [21, 30, 7, 22]],[[2, 9, 13, 10, 4], [1, 33, 26, 32, 3]],[[18, 23, 20, 19], [16, 17, 31, 15]],[[8, 28, 11, 14]]]			
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_2400':
        opt = [[[5, 27, 29, 24], [21, 7, 30, 22]],[[2, 9, 13, 10, 4], [1, 33, 26, 32, 3]],[[16, 17, 31, 15], [18, 23, 20, 19]],[[8, 28, 11, 14]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_3000':
        opt = [[[24, 21, 30, 22], [5, 29, 7, 27]],[[2, 9, 13, 10, 4], [1, 33, 26, 32, 3]],[[16, 17, 31, 15], [18, 23, 20, 19]] ,[[8, 28, 11, 14]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_3600':
        opt = [[[24, 21, 30, 22], [5, 29, 7, 27]],[[1, 9, 13, 10, 4], [3, 33, 26, 32, 2]],[[16, 17, 31, 15], [18, 23, 20, 19]] ,[[8, 28, 11, 14]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    elif scen == 'combo_min_4200':
        opt = [[[24, 21, 30, 22], [5, 29, 7, 27]],[[9, 13, 10, 4, 3], [33, 26, 32, 1, 2]],[[16, 17, 31, 15], [18, 23, 20, 19]],[[8, 28, 11, 14]]]
        sol = formSol(opt)
        ngdf = OptRoutes(routes, sol)
        ngdf.to_file(os.path.join(root_dir, 'shapefiles', scen +'_routes.shp'))
        sdistance = sum(ngdf.sdist)
    
    else: print('wrong scenario')
    
    return ngdf,sdistance

ngdf1 = outputShpOpt('sdist')[0]
ngdf2 = outputShpOpt('combo_min_600')[0]
ngdf3 = outputShpOpt('combo_min_1200')[0]
ngdf4 = outputShpOpt('combo_min_1800')[0]
ngdf5 = outputShpOpt('combo_min_2400')[0]
ngdf6 = outputShpOpt('combo_min_3000')[0]
ngdf7 = outputShpOpt('combo_min_3600')[0]
ngdf8 = outputShpOpt('combo_min_4200')[0]

ngdf1['scenario'] = '0: sdist'
ngdf2['scenario'] = '2: combo_min_600'
ngdf3['scenario'] = '3: combo_min_1200'
ngdf4['scenario'] = '4: combo_min_1800'
ngdf5['scenario'] = '5: combo_min_2400'
ngdf6['scenario'] = '6: combo_min_3000'
ngdf7['scenario'] = '7: combo_min_3600'
ngdf8['scenario'] = '7: combo_min_4200'

# xl = ["VoS = 0", "VoS = 600 m", "VoS = 1200 m", "VoS = 1800 m", "VoS = 2400 m", 
#      "VoS = 3000 m", "VoS = 3600 m", "VoS = 4200 m"]

# ngdf1['scenario'] = xl[0]
# ngdf2['scenario'] = xl[1]
# ngdf3['scenario'] = xl[2]
# ngdf4['scenario'] = xl[3]
# ngdf5['scenario'] = xl[4]
# ngdf6['scenario'] = xl[5]
# ngdf7['scenario'] = xl[6]
# ngdf8['scenario'] = xl[7]


dataframes = [ngdf1, ngdf2, ngdf3, ngdf4, ngdf5, ngdf6, ngdf7, ngdf8]
totalStackBar(dataframes, scale = 1.5)
wavgPckgLine(dataframes)



sum(ngdf1.sdist)
sum(ngdf2.sdist)
sum(ngdf3.sdist)
sum(ngdf4.sdist)
sum(ngdf5.sdist)
sum(ngdf6.sdist)
sum(ngdf7.sdist)
sum(ngdf8.sdist)





dfs = [ngdf1, ngdf2, ngdf3, ngdf4, ngdf5, ngdf6, ngdf7, ngdf8]
vos = [0, 600, 1200, 1800, 2400, 3000, 3600, 4200, 4800]

# List to hold individual grouped DataFrames
grouped_dfs = []

# Group and sum each DataFrame by depot, and add a column indicating the original DataFrame and VoS
for i, df in enumerate(dfs, start=1):
    
    grouped_df = df.groupby('depot').agg({
    'sumlentype1': 'sum',
    'sumlentype2': 'sum',
    'sumlentype3': 'sum',
    'sumlentype4': 'sum',
    'wavg_psafe': 'mean'}).reset_index()
    
    grouped_df['VOS'] = vos[i-1]  # Add VoS value corresponding to the DataFrame
    grouped_df['DF'] = f'DF{i}'  # Add a column indicating the DataFrame source
    grouped_dfs.append(grouped_df)

# Concatenate all grouped DataFrames into a single DataFrame
cdf = pd.concat(grouped_dfs).reset_index()

def stackRoadInv2(cdf, depot, ax1, ymax = 6000):
    cdf = cdf.loc[cdf.depot == depot]
    
    # fig, ax1 = plt.subplots(figsize=(10 * scale, 6 * scale), dpi=dpi)
    
    # Plot bars on the primary y-axis (left axis)
    ax1.bar(cdf.DF, cdf.sumlentype1, color='#E31A1C', label='1: Urban road with sidewalk less than 1.5 m wide')
    ax1.bar(cdf.DF, cdf.sumlentype2, color='#FF7F00', bottom=cdf.sumlentype1, 
            label='2: Urban road with sidewalk more than 1.5 m wide')
    ax1.bar(cdf.DF, cdf.sumlentype3, color='#0000FF', bottom=cdf.sumlentype1 + cdf.sumlentype2,
            label='3: Urban road with cycle lane')
    ax1.bar(cdf.DF, cdf.sumlentype4, color='#1DD083', bottom=cdf.sumlentype1 + cdf.sumlentype2 + cdf.sumlentype3,
            label='4: Shared space')

    ax1.set_xlabel('Value of Safety in meters')  # X-axis label
    ax1.set_ylabel('Total network length in m', color='black')  # Left y-axis label
    ax1.set_title('Depot ' + str(depot))  # Plot title
    
    # Custom x-axis ticks
    custom_labels = ['0', '600', '1200', '1800', '2400', '3000', '3600', '4200']
    ax1.set_xticks(cdf.DF)
    ax1.set_xticklabels(custom_labels)
    ax1.set_ylim([0, 14000])
    
    ax1.legend(loc='upper left')  # Legend for bar plots
    
    # Create a secondary y-axis (right axis) for wavg_psafe
    ax2 = ax1.twinx()
    ax2.plot(cdf.DF, 4 + cdf.wavg_psafe, color='black', marker='o', linestyle='-', linewidth=2, label='wavg_psafe')
    ax2.set_ylabel('Mean perceived safety level (max 7)', color='black')  # Right y-axis label
    ax2.set_ylim([2, 4])
    
    # ax2.set_ylim([1, 7])
    
    # ax2.legend(loc='upper right')  # Legend for line plot

fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10 * 1.2, 8 * 1.2), dpi=400)

# Flatten the 2D array of subplots to iterate over them
axs = axs.flatten()

# Iterate over unique depots and plot on each subplot
unique_depots = cdf.depot.unique()
for i, depot in enumerate(unique_depots):
    stackRoadInv2(copy.deepcopy(cdf), depot, axs[i])

# Adjust layout to prevent overlapping labels
plt.tight_layout()

plt.show()

for depot in cdf.depot.unique(): stackRoadInv2(copy.deepcopy(cdf), 
                                              depot)

def stackRoadInv3(cdf, depot, scale=1.5, dpi=400):
    cdf = cdf.loc[cdf.depot == depot]
    
    # Calculate total sum for each DF category
    totals = cdf[['sumlentype1', 'sumlentype2', 'sumlentype3', 'sumlentype4']].sum(axis=1)
    
    # Normalize each column by dividing by totals
    normalized_df = cdf[['sumlentype1', 'sumlentype2', 'sumlentype3', 'sumlentype4']].div(totals, axis=0) * 100
    
    fig, ax1 = plt.subplots(figsize=(10 * scale, 8 * scale), dpi=dpi)
    
    # Plot 100% stacked bars on the primary y-axis (left axis)
    ax1.bar(cdf.DF, normalized_df['sumlentype1'], color='#E31A1C', label='1: Urban road with sidewalk less than 1.5 m wide')
    ax1.bar(cdf.DF, normalized_df['sumlentype2'], color='#FF7F00', bottom=normalized_df['sumlentype1'], 
            label='2: Urban road with sidewalk more than 1.5 m wide')
    ax1.bar(cdf.DF, normalized_df['sumlentype3'], color='#0000FF', bottom=normalized_df['sumlentype1'] + normalized_df['sumlentype2'],
            label='3: Urban road with cycle lane')
    ax1.bar(cdf.DF, normalized_df['sumlentype4'], color='#1DD083', bottom=normalized_df['sumlentype1'] + normalized_df['sumlentype2'] + normalized_df['sumlentype3'],
            label='4: Shared space')

    ax1.set_xlabel('Value of Safety in meters')  # X-axis label
    ax1.set_ylabel('Percentage of Network Length (%)', color='black')  # Left y-axis label
    ax1.set_title('Depot ' + str(depot))  # Plot title
    
    # Custom x-axis ticks
    custom_labels = ['0', '600', '1200', '1800', '2400', '3000', '3600', '4200']
    ax1.set_xticks(cdf.DF)
    ax1.set_xticklabels(custom_labels)
    
    # ax1.legend(loc=' left')  # Legend for bar plots
    
    # Create a secondary y-axis (right axis) for wavg_psafe (optional)
    ax2 = ax1.twinx()
    ax2.plot(cdf.DF, 4 + cdf.wavg_psafe, color='black', marker='o', linestyle='-', linewidth=2, label='wavg_psafe')
    ax2.set_ylabel('Weighted Average of Safety', color='black')  # Right y-axis label
    
    # ax2.legend(loc='upper right')  # Legend for line plot
    
    plt.show()

# for depot in cdf.depot.unique(): stackRoadInv3(copy.deepcopy(cdf), 
#                                              depot)

