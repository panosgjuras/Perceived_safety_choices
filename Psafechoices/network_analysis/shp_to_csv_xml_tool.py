"""
Network psafe csv and xml creation

@author: ptzouras
National Technical University of Athens
"""
import lxml.etree as ET
import pandas as pd

def netcsv_cr(lin, path): # create a csv to be imported in GIS via join.
    out=pd.DataFrame(lin, columns=['id','from1', 'to1', 'length', 'modes', 'car_psafe','ebike_psafe','escoot_psafe','walk_psafe',
                               'car_psafe_l','ebike_psafe_l','escoot_psafe_l','walk_psafe_l'])
    out.set_index('id').to_csv(path)

# set link values per attribute. 
# these values will be given from the shp file that will be converted into a dataframe
# build the tree of links for MATSim

def netxml_bld(lin, nod):
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

def netxml_cr(lin, nod, path):
    new_xml = ET.tostring(netxml_bld(lin, nod), encoding='utf-8', pretty_print=True , xml_declaration=True,
              doctype='<!DOCTYPE network SYSTEM "http://www.matsim.org/files/dtd/network_v2.dtd">') # encoding utf-8 and pretty print
    # provide doctype, it is necessary for MATSim
    with open(path,'wb') as f: f.write(new_xml) # export the new xml file
