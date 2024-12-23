"""
Tools to fuse spatial data in order to define road infrastructure types

Road infrastructure types are later utilized to estimate perceived safety rates

@author: ptzouras
National Technical University of Athens
"""
import geopandas as gpd
import matplotlib.pyplot as plt

def InfTypeCheck(df):

    # This function should go to Perceived Safety Choice Repo
    # It has been developed first time for Munich Analysis
    
    """
    Parameters
    ----------
    df : dataFrame
        df with the links, it must contain: 'inf', 'explInf'
    Returns
    -------
    A bar plot with frequencies per infrastructure type met in the link dataFrame
    It is only for checking
    """
    group = df.groupby(['inf', 'explInf']).size().unstack(fill_value = 0)
    plt.figure(figsize = (10, 10))
    group.plot(kind='bar', stacked=True)
    plt.xlabel('Infrastructure Type')
    plt.ylabel('Frequency')
    # plt.title('')
    plt.show()


def fusionWalkableCity(gdf, wlink, var, text = "variable1", tolerance = 10):
        
    """
    The function fuse link data with sidewalk data. It is a data processing function.
    It creates buffer in the link data and check for mean width of sidewalks in both sides

    Parameters
    ----------
    gdf : dataFrame
        The gpd dataFrame with all the links. The links must have 'inf' column
    wlink : dataFrame
        The gpd dataframe with the sidewalk width
    var : str
        indicates which column the of wlink dataFrame the sidewalk width is given
    text : str, optional
        how the variable will be named in the gdf. The default is "variable1".
    tolerance : int, optional
        the tolerance based on overlaps will be checked, it creates a buffer. The default is 10.

    Returns
    -------
    gdf : dataFrame
        the new links gpd dataframe, with the extra attribute associated with the sidewalk width

    """
    # the tolerance is 10 meters, so we create a buffer with radius 10 meters
    wlink = wlink.rename(columns={var:'x_variable'}) # raname the variable you will play with
    gdf_buffered = gdf.copy() # create the buffered gdf
    gdf_buffered['geometry'] = gdf_buffered.geometry.buffer(tolerance) # buffer the road links, not the sidewalks
    wlink_buffered = wlink.copy() # this contains sidewalks, so both sides
    # it creates a joined files, based on intersection, it is a spatial analysis
    joined = gpd.sjoin(gdf_buffered, wlink_buffered, how="inner", op="intersects")
    
    gdf[text] = "no Walkable Data" # set the variable you will do fusion
    
    dominant_category = (
        joined.groupby('linkId')['x_variable']
        .agg(lambda x: x.value_counts().idxmax())
        .reset_index()
        .rename(columns={'x_variable': text})
    )
    
    gdf = gdf.merge(dominant_category, on='linkId', how='left')
    
    # print(joined)
    # for uid in joined["linkId"].unique(): # check all the unique id of our links
    # one link of our file can be joined with multiple links from Walkable
    # so we run only the unique ids
        # print(uid)
    #    gff = joined.loc[joined["linkId"]==uid].groupby("x_variable").size()
    #    if not gff.empty:
    #        ff = gff.idxmax() # we check which category is the dominant one
    #        gdf.loc[gdf["linkId"] == uid, text] = ff # we add this new input
    return gdf