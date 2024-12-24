"""
Tools to update the links and build an xml for MATSim

@author: ptzouras
National Technical University of Athens
"""
import lxml.etree as ET
import pandas as pd

# def netcsv_cr(lin, path): # create a csv to be imported in GIS via join.
#     out=pd.DataFrame(lin, columns=['id','from1', 'to1', 'length', 'modes', 'car_psafe','ebike_psafe','escoot_psafe','walk_psafe',
#                               'car_psafe_l','ebike_psafe_l','escoot_psafe_l','walk_psafe_l'])
#    out.set_index('id').to_csv(path)

# set link values per attribute. 
# these values will be given from the shp file that will be converted into a dataframe
# build the tree of links for MATSim

def buildNetXML_old(lin, nod):
    network=ET.Element("network")
    nodes=ET.SubElement(network,"nodes")
    for i in range (0, len(nod)): 
        node=ET.SubElement(nodes,"node")
        node.set("id",str(nod.id.loc[i]))
        node.set("x", str(nod.x.iloc[i]))
        node.set("y", str(nod.y.iloc[i]))
        node.set("z", str(nod.z.iloc[i]))
    links=ET.SubElement(network, "links",attrib={'capperiod':"01:00:00"}) # define time these attribute values are valid
    for i in range(0,len(lin)): # links subelement, create fuction HERE
        link=ET.SubElement(links,"link")
        link.set("id", str(lin.id.iloc[i]))
        link.set("from", str(lin.from1.iloc[i]))
        link.set("to",str(lin.to1.iloc[i]))
        link.set("length", str(lin.length.iloc[i]))
        link.set("capacity", str(lin.capacity.iloc[i]))
        link.set("freespeed", str(lin.freespeed.iloc[i]))
        link.set("permlanes", str(lin.permlanes.iloc[i]))
        link.set("oneway", str(lin.oneway.iloc[i]))
        #link.set("modes", lin.modes.iloc[i])
        link.set("modes", str(lin.modes.iloc[i])) # car just to run the equil scenario
        link.set("origid","") # is it necessary ??

        attributes=ET.SubElement(link,"attributes") # additional attributes
        
        attribute=ET.SubElement(attributes,"attribute") #new attribute: pasafe for cars
        attribute.set("name","carpsafe")
        attribute.set("class", "java.lang.Integer")
        attribute.text=str(lin.car_psafe_l.iloc[i]) # psafe value that will be an integer.
        #attribute.text=str(lin.car_psafe.iloc[i]) # psafe value that will be an integer.
    
        attribute=ET.SubElement(attributes,"attribute") #new attribute: pasafe for ebike
        attribute.set("name","ebikepsafe")
        attribute.set("class", "java.lang.Integer")
        attribute.text=str(lin.ebike_psafe_l.iloc[i])
        #attribute.text=str(lin.ebike_psafe.iloc[i])
    
        attribute=ET.SubElement(attributes,"attribute") #new attribute: pasafe for escooter
        attribute.set("name","escootpsafe")
        attribute.set("class", "java.lang.Integer")
        attribute.text=str(lin.escoot_psafe_l.iloc[i])
        #attribute.text=str(lin.escoot_psafe.iloc[i])
    
        attribute=ET.SubElement(attributes,"attribute") #new attribute: pasafe for walk
        attribute.set("name","walkpsafe")
        attribute.set("class", "java.lang.Integer")
        attribute.text=str(lin.walk_psafe_l.iloc[i])
        #attribute.text=str(lin.walk_psafe.iloc[i])
    
        attribute=ET.SubElement(attributes,"attribute") #new attribute: pasafe for walk
        attribute.set("name","type")
        attribute.set("class", "java.lang.String")
        attribute.text="primary"
    
        attribute=ET.SubElement(attributes,"attribute") #new attribute: pasafe for walk
        attribute.set("name","bicycleInfrastructureSpeedFactor")
        attribute.set("class", "java.lang.Double")
        attribute.text="1.0"
    return network

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



# path = os.path.join(file_path, "berlin-v6.5-network.xml")

# attribute_names = ['carpsafe', 'ebikepsafe', 'escootpsafe']

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
    







