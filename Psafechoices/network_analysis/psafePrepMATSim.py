"""
Tools to update the links and build an xml for MATSim

@author: ptzouras
National Technical University of Athens
"""
import lxml.etree as ET
import pandas as pd
import geopandas as gpd

def nod_match(links,nodes):
    """
    This function finds the id of staring and ending node per link

    Parameters
    ----------
    lin : gpd.DataFrame
        It is the geodataframe with all the links
    nod : gpd.DataFrame
        It is the geodataframe with all the nodes

    Returns
    -------
    links: gpd.DataFrame
        the updated links file
    """
    for i in range(0,len(links)): 
        fr1 = nodes.loc[(nodes.x==links.loc[i,'x_start']) & (nodes.y==links.loc[i,'y_start']),'id']
        fr2 = nodes.loc[(nodes.x==links.loc[i,'x_end']) & (nodes.y==links.loc[i,'y_end']),'id']
        if len(fr1)>0: # check if you found matches, if not 9999
           links.loc[i,'from1']=fr1.iloc[0] # select each time the first match
        else: links.loc[i,'from1'] = 999
        if len(fr2)>0:
           links.loc[i,'to1']=fr2.iloc[0]
        else: links.loc[i,'to1'] = 999
    return links

def twoway(df, no_resp_prior = 'walk'):
    """
    This function creates an extra link with the opposite direction, if road is twoway.
    Extra link is not created for oneways, unless the transport mode does not respect directions
    ----------
    df : gpd.DataFrame
       It is the geodataframe with all the links
    no_resp_prior : str, optional
        Modes that do not respect directions should be defined.
        The default is 'walk'.

    Returns
    -------
    df: gpd.DataFrame
        the updated links file
    """
    
    if no_resp_prior == 'walk':
        pedl = 'walk_links'
    elif no_resp_prior == 'escoot,walk':
        pedl = 'walk_escoot_links'
    elif no_resp_prior == 'ebike,escoot,walk':
        pedl = 'walk_ebike_escoot_links'
    else: pedl = 'no_walk_links'
    
    # the meaning of the walk links is to design opposite direction links in oneways for pedestrians only.
    
    x = len(df)
    dc = pd.DataFrame(columns = ['id','matchid','from1','to1'])
    text = 'walk'
    dl = pd.DataFrame(columns = ['id','matchid','from1','to1'])
    c = 0
    l = 0
    for i in range(0, x):
        if df.oneway.iloc[i]== 0:
                        
            dc = pd.concat([dc, pd.DataFrame({'id': 100000 + df.id.iloc[i], 'matchid': df.id.iloc[i], 
                                  'from1': df.to1.iloc[i], 'to1': df.from1.iloc[i]}, index=[0])], ignore_index=True)
            
            # dc = pd.concat({'id': 100000 + df.id.iloc[i], 'matchid': df.id.iloc[i], # it needs to start from 1, otherwise it requires upd
            #     'from1':df.to1.iloc[i], 'to1': df.from1.iloc[i]}, ignore_index = True)
            
            c = c + 1
            # print(c)
        
        if df.oneway.iloc[i]==1 and (text in df.modes.iloc[i]) and (pedl == 'walk_links' 
                                                                    or pedl == 'walk_escoot_links' or pedl == 'walk_ebike_escoot_links'):
            
            dl = pd.concat([dl, pd.DataFrame({'id': 100000 + df.id.iloc[i], 'matchid': df.id.iloc[i], 
                                  'from1': df.to1.iloc[i], 'to1': df.from1.iloc[i]}, index=[0])], ignore_index=True)
            
            
            # dl = dl.append({'id': 100000 + df.id.iloc[i], 'matchid': df.id.iloc[i], # it needs to start from 1, otherwise it requires upd
            #     'from1':df.to1.iloc[i], 'to1': df.from1.iloc[i]}, ignore_index = True)
            
            l = l + 1
            # print(l)
   
    dc = pd.merge(left=dc, right=df.drop(columns=['from1','to1']), how="inner", left_on='matchid', right_on='id').drop(columns=['id_y', 'matchid']).rename(columns={'id_x':'id'})
    df = pd.concat([df, dc], axis=0, ignore_index=True, sort=False).dropna()
    
    if pedl == 'walk_links': 
        dl = pd.merge(left = dl, right = df.drop(columns=['from1','to1']), how="inner", left_on='matchid', right_on='id').drop(columns=['id_y', 'matchid']).rename(columns={'id_x':'id'})
        dl["modes"] = 'walk'
        df = pd.concat([df, dl], axis=0, ignore_index=True, sort=False).dropna()
    
    if pedl == 'walk_escoot_links':
        dl = pd.merge(left = dl, right = df.drop(columns=['from1','to1']), how="inner", left_on='matchid', right_on='id').drop(columns=['id_y', 'matchid']).rename(columns={'id_x':'id'})
        dl["modes"] = 'escoot,walk'
        df = pd.concat([df, dl], axis=0, ignore_index=True, sort=False).dropna()
        
    if pedl == 'walk_ebike_escoot_links':
        dl = pd.merge(left = dl, right = df.drop(columns=['from1','to1']), how="inner", left_on='matchid', right_on='id').drop(columns=['id_y', 'matchid']).rename(columns={'id_x':'id'})
        dl["modes"] = 'ebike,escoot,walk'
        df = pd.concat([df, dl], axis=0, ignore_index=True, sort=False).dropna()
    
    df.oneway = df.oneway.replace({0:1})
    
    # print(c)
    # print(l)
    
    return df

def speed(df, cr = 1, delr = 1):
    """
    It updates the free flow speed based on the speed limit, compliance rate and delays at intersections

    Parameters
    ----------
    df : gpd.DataFrame
       It is the geodataframe with all the links
    cr : float, optional
        The compliance rate of drivers. The default is 1.
    delr : float, optional
        The ratio between the actual speed and the freeflow speed. The default is 1.
        1 means no congestion, but also means no delay due to interactions.

    Returns
    -------
    df: gpd.DataFrame
        the updated links file

    """

    df.freespeed = delr * (cr * df.freespeed*1000/3600)
    return df

def capacity(df, dwn = 1, simp = 'simple',  w = 13.5, kjam = 125):
    """
    It updates the capacity of links based on multimple parameters

    Parameters
    ----------
    df : gpd.DataFrame
       It is the geodataframe with all the links
    dwn : float, optional
        It is the level of capacity downscale you do at the end. The default is 1.
    simp : str, optional
        if "simple", the capacity is equal to the number of lanes multiplied by 1200. 
        if "kinematic_waves": the capacity is calculated based on the kinematic waves function
        The default is 'simple'.
    w : float, optional
        It is the wave speed. The default is 13.5.
    kjam : float, optional
        The jam density. The default is 125.

    Returns
    -------
    df: gpd.DataFrame
        the updated links file
    """
    
    freespeed = df.freespeed * 3600/1000
    
    for i in range(0,len(df)):
        if simp == 'simple': 
            df.loc[i, 'capacity'] = dwn * (df.permlanes.iloc[i]*1200) # very simplistic approach.
        elif simp == 'kinematic_waves':
            df.loc[i, 'capacity']= dwn * (df.permlanes.iloc[i] * kjam * freespeed.iloc[i] * w)/(freespeed.iloc[i] + w)
        else: df.capacity.iloc[i] = 9999 # here a new extension will be written based on speed compliance rate and speed limit
    return df

def netxml_cr(network, path):
    """
    It saves the xml file for using in MATSim

    Parameters
    ----------
    network : etree.ElementTree.Element
        the updated network file for analysis
    path : str
        The path where the xml file will be saved

    Returns
    -------
    None

    """
    
    new_xml = ET.tostring(network, encoding='utf-8', pretty_print=True , xml_declaration=True,
              doctype='<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">') # encoding utf-8 and pretty print
    # provide doctype, it is necessary for MATSim
    with open(path,'wb') as f: f.write(new_xml) # export the new xml file

def buildNetXML(lin, nod, modes, path):
    """
    It updates an existing network xml file for MATSim.
    the new xml file contains the perceived safety rates as additional attribute.

    Parameters
    ----------
    lin : gpd.DataFrame
        It is the geodataframe with all the links
    nod : gpd.DataFrame
        It is the geodataframe with all the nodes
    modes : list
        the list with all the transport modes
    path : str
        The path where the xml file will be saved

    Returns
    -------
    network : etree.ElementTree.Element
        the updated network file for analysis
    """
    
    
    # Create the root network element
    network = ET.Element("network")
    
    # Create nodes subelement
    nodes = ET.SubElement(network, "nodes")
    
    # Add nodes to the XML structure
    for _, node in nod.iterrows():
        node_elem = ET.SubElement(nodes, "node")
        node_elem.set("id", str(node.id))
        node_elem.set("x", str(node.x))
        node_elem.set("y", str(node.y))
        node_elem.set("z", str(node.z))
    
    # Create links subelement
    links = ET.SubElement(network, "links", attrib={'capperiod': "01:00:00"})
    
    # Add links to the XML structure
    for _, link in lin.iterrows():
        link_elem = ET.SubElement(links, "link")
        link_elem.set("id", str(link.id))
        link_elem.set("from", str(link.from1))
        link_elem.set("to", str(link.to1))
        link_elem.set("length", str(link.length))
        link_elem.set("capacity", str(link.capacity))
        link_elem.set("freespeed", str(link.freespeed))
        link_elem.set("permlanes", str(link.permlanes))
        link_elem.set("oneway", str(link.oneway))
        link_elem.set("modes", str(link.modes)) 
        link_elem.set("origid", "")  # Consider if this is necessary

        # Add attributes subelement to the link
        attributes = ET.SubElement(link_elem, "attributes")

        # Dynamically create attributes for each transport mode
        for mode in modes:
            attribute = ET.SubElement(attributes, "attribute")
            attribute.set("name", f"{mode}psafe")
            attribute.set("class", "java.lang.Integer")
            attribute.text = str(link[f"{mode}_psafe_l"])
    
    netxml_cr(network, path)
    
    return network

def updNetXML(hierarchy, gdf_results, modes, path):
    """
    It updates an existing network xml file for MATSim.
    the new xml file contains the perceived safety rates as additional attribute.

    Parameters
    ----------
    hierarchy : etree.ElementTree.Element
        The startig network xml file. This means that does exist
    gdf_results : gpd.DataFrame
        It is the geodataframe with all the links
    modes : list
        the list with all the transport modes
    path : str
        The path where the xml file will be saved
        
    Returns
    -------
    hierarchy : etree.ElementTree.Element
        the updated network file for analysis

    """
    
    total_links = len(hierarchy[2])
    attribute_names = [mode + 'psafe' for mode in modes]
    for idx, link in enumerate(hierarchy[2]):
        attributes = ET.SubElement(link, "attributes")  # Create additional attributes

        # Check if the link ID exists in gdf_results
        if link.attrib["id"] in gdf_results["id"].values:
            # Extract the values for each mode, converting to string
            values = [str(gdf_results.loc[gdf_results["id"] == link.attrib["id"], mode].values[0]) for mode in modes]
        else:
            # Default values if the ID does not exist
            values = [str(7)] * len(modes)

        # Create attributes using a loop
        for attribute_name, value in zip(attribute_names, values):
            attribute = ET.SubElement(attributes, "attribute")  # New attribute
            attribute.set("name", attribute_name)
            attribute.set("class", "java.lang.Integer")
            attribute.text = value

        # Calculate and print the processing percentage
        processed_percentage = (idx + 1) / total_links * 100
        print(f"Processed {idx + 1} out of {total_links} links ({processed_percentage:.2f}%)")
        

    netxml_cr(hierarchy, path)
    
    return hierarchy
    
