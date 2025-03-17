"""
Tools to analyze MATSim outputs from the Scenario Athens

@author: ptzouras
National Technical University of Athens
"""

import pandas as pd
import gzip
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def gunzip(source_filepath, dest_filepath, block_size=65536):
    """
    Function to unzip giz files extracted from MATSim simulation run

    Parameters
    ----------
    source_filepath : str
        The path of the giz file
    dest_filepath : str
        The path where the unzipped file will be saved
    block_size : int, optional
        The block size. The default is 65536.

    Returns
    -------
    None.

    """
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)

def readtrips(outMATSim, outfold):
    """
    Function to read the trips of MATSim

    Parameters
    ----------
    outMATSim : str
        The path of the giz file
    outfold : str
        The path where the unzipped file will be saved

    Returns
    -------
    e : DataFrame
        the trips file. It is DataFrame
    """
    source_filepath = os.path.join(outMATSim, 'output_trips.csv.gz')
    dest_filepath = os.path.join(outfold, 'output_trips.csv')
    
    # source_filepath = os.path.join(root_dir, scenario, 'output_events.xml.gz')
    # dest_filepath = os.path.join(root_dir, outfold, scenario, 'output_events.xml')
    
    gunzip(source_filepath, dest_filepath)
    e = pd.read_csv(dest_filepath, sep = ';')
    # os.remove(dest_filepath) # if you do not want to save these large files
    return e


def readevents(root_dir, scenario, outfold):
    source_filepath = os.path.join(root_dir, outfold, scenario, 'output_events.xml.gz')
    dest_filepath = os.path.join(root_dir, outfold, scenario, 'output_events.xml')
    gunzip(source_filepath, dest_filepath)
    e = ET.parse(dest_filepath)
    e = e.getroot()
    os.remove(dest_filepath)
    return e

def readnetwork(root_dir, scenario, outfold):
    source_filepath = os.path.join(root_dir, outfold, scenario, 'output_network.xml.gz')
    dest_filepath = os.path.join(root_dir, outfold, scenario, 'output_network.xml')
    gunzip(source_filepath, dest_filepath)
    net = ET.parse(dest_filepath)
    net = net.getroot()
    os.remove(dest_filepath)
    return net

def flowmeasure(events, network):
    df = pd.DataFrame(columns = ['id', 'qcar', 'qebike', 'qescoot'])
    c = len(events)
    
    for x in range(0, len(network[2])):
        df.loc[x, 'id'] = network[2][x].attrib['id']
        car = 0
        ebike = 0
        escoot = 0
        for y in range(0, c):
            c1 = 0
            c2 = 0
            cebike = False
            cescoot = False
            ccar = False
            if events[y].attrib['type'] == "entered link":
                c1 = 1
                if events[y].attrib['link'] == df.loc[x, 'id']:
                    c2 = 1
                else: continue
                if 'ebike' in events[y].attrib['vehicle']: cebike = True
                elif 'escoot' in events[y].attrib['vehicle']: cescoot = True
                else: ccar = True
            else: continue
        
            if c1 == 1 and c2 == 1 and ccar == True: car = car + 1
            if c1 == 1 and c2 == 1 and cebike == True: ebike = ebike + 1
            if c1 == 1 and c2 == 1 and cescoot == True: escoot = escoot + 1
        
        df.loc[x, 'qcar'] = car
        df.loc[x, 'qebike'] = ebike
        df.loc[x, 'qescoot'] = escoot
        print(x)
    
    df.qcar = df.qcar.astype('int')
    df.qebike = df.qebike.astype('int')
    df.qescoot = df.qescoot.astype('int')
    df.id = df.id.astype(int)
    return df

def seqLinks(events, scenario, mode = ['ebike', 'escoot']):
    df = pd.DataFrame(columns=['link', 'vehicle', 'tmode'])

    for y, event in enumerate(events):
        if event.attrib.get('type') == "entered link":
            link = event.attrib.get('link')
            vehicle = event.attrib.get('vehicle')
            if link and vehicle:  # Check if link and vehicle are present
                tmode = 'car'
                if 'ebike' in vehicle:
                    tmode = 'ebike'
                elif 'escoot' in vehicle:
                    tmode = 'escoot'
                
                df = df.append({'link': link, 'vehicle': vehicle, 'tmode': tmode}, ignore_index=True)
    
    def clean_vehicle(vehicle):
        if '_escoot' in vehicle or '_ebike' in vehicle:
            return vehicle.split('_')[0]
        return vehicle

    df['vehicle'] = df['vehicle'].apply(clean_vehicle)

    df_grouped = df.groupby(['vehicle', 'tmode'])['link'].apply(list).reset_index()
    return df_grouped


def seqLinks(events, scenario, mode=['ebike', 'escoot']):
    """
    

    Parameters
    ----------
    events : TYPE
        DESCRIPTION.
    scenario : TYPE
        DESCRIPTION.
    mode : TYPE, optional
        DESCRIPTION. The default is ['ebike', 'escoot'].

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    df = pd.DataFrame(columns=['link', 'vehicle', 'tmode'])

    # Iterate through events
    for y, event in enumerate(events):
        if event.attrib.get('type') == "entered link":
            link = event.attrib.get('link')
            vehicle = event.attrib.get('vehicle')
            if link and vehicle:  # Check if link and vehicle are present
                tmode = 'car'  # Default mode
                # Check if vehicle matches any of the provided modes
                for m in mode:
                    if m in vehicle:
                        tmode = m
                        break  # Once a matching mode is found, stop checking further
                
                df = df.append({'link': link, 'vehicle': vehicle, 'tmode': tmode}, ignore_index=True)
    
    # Function to clean vehicle names by removing mode suffix (if any)
    def clean_vehicle(vehicle):
        for m in mode:  # Check against the provided modes
            if f'_{m}' in vehicle:
                return vehicle.split('_')[0]  # Remove the mode suffix
        return vehicle

    # Apply the clean_vehicle function to the 'vehicle' column
    df['vehicle'] = df['vehicle'].apply(clean_vehicle)

    # Group by vehicle and mode, and create a list of links
    df_grouped = df.groupby(['vehicle', 'tmode'])['link'].apply(list).reset_index()
    
    return df_grouped

def SimRouteMatrix(group, m, n = 20):
    num_group = len(group)
    siMatrix = pd.DataFrame(index=range(num_group), columns=range(num_group))
    if m == 'car': mc = "Car" 
    elif m == 'ebike': mc = 'E-bike'
    else: mc = 'E-scoot' 

    n = 50
    for i in range(num_group):
        for j in range(num_group):
            perc = simPerc2(group[j], m, seq000=group[i], n=n)
            siMatrix.loc[i,j] = 1 - perc[0]
            
    siMatrix = siMatrix.astype(float)

    plt.figure(figsize=(10, 10), dpi = 500)
    heatmap = sns.heatmap(siMatrix * 100, annot=True, cmap="viridis", fmt=".2f", annot_kws={"size": 10}, cbar=False)
    plt.title("Percentage (%) of similar paths - " + mc )
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks(ticks=range(len(group)), labels=scenario, rotation=90)
    plt.yticks(ticks=range(len(group)), labels=scenario, rotation=0)

    heatmap.set_yticks([i + 0.5 for i in range(len(scenario))])
    heatmap.set_yticklabels(scenario, va='center')
    
    heatmap.set_xticks([i + 0.5 for i in range(len(scenario))])
    heatmap.set_xticklabels(scenario)

    plt.show()


def accessTable(df):
    # Convert travel time to pandas timedelta
    df['trav_time'] = pd.to_timedelta(df['trav_time'])
    
    df['main_mode'] = df['main_mode'].astype(str)

    # Calculate the required statistics per person
    summary_df = df.groupby('person').agg({
        'trip_number': 'count',
        'euclidean_distance': 'sum',
        'traveled_distance': 'sum',
        'trav_time': lambda x: x.sum().total_seconds() / 60,
        'longest_distance_mode': 'first',
        'start_x': 'first',
        'start_y': 'first'
    }).rename(columns={
        'trip_number': 'Trips',
        'euclidean_distance': 'totEucliDist',
        'traveled_distance': 'totTravDist',
        'trav_time': 'totTravTime',
        'longest_distance_mode': 'mainMode',
    })
        
    summary_df = summary_df[summary_df['totEucliDist'] > 0]    
        

    return summary_df

def totalHist(df, t='totEucliDist', scenario='', thr = None, out = None, trend='no', step=2, dpi = 500):
    
    # df = df[df['relAccessDist'] < out]
    
    gdf = df.groupby('mainMode')[t].apply(list)

    scale = 1.5

    fig, ax1 = plt.subplots(figsize=(8 * scale, 6 * scale), dpi = dpi)

    colors = sns.color_palette("muted", len(gdf))

    sns.set_style("ticks")

    if t == 'relAccessTime':
        xt = 'Relative Access Time'
    elif t == 'relAccessDist':
        xt = 'Relative Access Distance'
    else:
        xt = t

    for i, (mode, data) in enumerate(gdf.items()):
        
        # Calculate mean and standard deviation
        mean = np.mean(data)
        std = np.std(data)
        if thr is not None: 
            data_filtered = [x for x in data if x < thr]
            perc = len(data_filtered) / len(data) * 100
        else: perc = 0
        
        if out is not None: data = [x for x in data if x < out]
        
        bins = np.arange(0, max(data) + step, step)
        sns.histplot(data, bins=bins, alpha=0.9, label=mode, color=colors[i], ax=ax1,
                     line_kws={"linewidth": 3}, edgecolor=".1")

        # ax1.legend()
        #ax1.legend([f"{mode} (Mean: {mean:.2f}, Std: {std:.2f})"])
        legend_label = f"{mode} (Mean: {mean:.2f}, Std: {std:.2f}, Pthr: {perc:.2f}%)"
        ax1.plot([], [], color=colors[i], label=legend_label)
        
        # Annotate mean and standard deviation in legend
        # legend_label = f"{mode} (Mean: {mean_value:.2f}, Std: {std_value:.2f})"
        # ax1.annotate("", xy=(0, 0), xytext=(0, 0), label=legend_label)
        
    ax1.set_xlabel(xt)
    ax1.set_ylabel('Frequency')
    ax1.set_title(scenario)
    ax1.legend(fontsize = 'large')

    if trend == 'yes':
        ax2 = ax1.twinx()

        for i, (mode, data) in enumerate(gdf.items()):
            
            if out is not None: data = [x for x in data if x < out]
            
            sns.kdeplot(data, linewidth=2, linestyle='--', color=colors[i], ax=ax2)

        ax2.set_ylabel('Density')

    return plt

def relAccess(df, fixSpeed = 30):
    df["relAccessDist"] = df.totTravDist/df.totEucliDist
    
    fixSpeed = 1000/60 * fixSpeed
    
    df["relAccessTime"] = df.totTravTime/(df.totEucliDist * (1/fixSpeed))

    return(df)


def GiniInd(df, t, c = 0):
    rel_access_dist = df[t].values + c
    # Sort the data in ascending order
    rel_access_dist_sorted = np.sort(rel_access_dist)
    # print(rel_access_dist_sorted)

    # Initialize an array to store the cumulative sums
    cumulative_sums = np.zeros_like(rel_access_dist_sorted)
    pop_step = np.zeros_like(rel_access_dist_sorted)

    # Calculate cumulative sums
    cumulative_sums[0] = rel_access_dist_sorted[0]
    pop_step[0] = 1
    
    
    for i in range(1, len(rel_access_dist_sorted)):
        cumulative_sums[i] = cumulative_sums[i - 1] + rel_access_dist_sorted[i]
        pop_step[i] = pop_step[i - 1] + 1
    
    
    sm = np.zeros_like(cumulative_sums)
    sm[0] = 0
    cumulative_perc = cumulative_sums/sum(rel_access_dist_sorted)
    pop_step_perc = pop_step/len(rel_access_dist_sorted)
    
    for i in range(1, len(cumulative_perc)):        
        sm[i] = (cumulative_perc[i] + cumulative_perc[i - 1]) * (pop_step_perc[i] - pop_step_perc[i - 1])
        
    gini = - sum(sm) + 1 
    print(gini)
    
    print(pop_step)
    
    # print(gini)
    
    return cumulative_sums, cumulative_perc, pop_step, pop_step_perc, gini


def cdfEquity(cumulative_sums, t, gini, scenario = 'Test Scenario', dpi = 400):
    
    sns.set_style("ticks")

    x = np.arange(len(cumulative_sums))

    scale = 1.2

    plt.figure(figsize=(8 * scale, 6 * scale), dpi = dpi) 

    # Plot the line
    plt.plot(x, cumulative_sums, 'r--', label='', linewidth=2.5)

    plt.plot([0, len(cumulative_sums)], [0, cumulative_sums[-1]], 'k--', label='Bottom Left to Top Right')

    # Plot the bars
    plt.bar(x, cumulative_sums, width=1, alpha=0.2,  color='red', label='Bars')
    
    # plt.fill_between(x, cumulative_sums, [0, cumulative_sums[-1]], where=(cumulative_sums >= [0, cumulative_sums[-1]]), alpha=0.2, color='red')

    # Add labels and title
    plt.xlabel('Agents')
    
    if t == 'relAccessTime': xt = 'Relative Access Time'
    elif t =='relAccessDist': xt = 'Relative Access Distance'
    else: xt = t

    plt.ylabel('Cummulative ' + xt + ' per agent')
    plt.title(scenario)
    
    plt.text(0.05, 0.95, f'Gini index: {gini:.4f}', transform=plt.gca().transAxes, ha='left', va='top', fontsize=15)

    plt.ylim(cumulative_sums[cumulative_sums != 0].min(), cumulative_sums.max())
    plt.xlim(0, len(cumulative_sums))

    # Add legend
    # plt.legend()

    # Display the plot
    # plt.show()
    return plt