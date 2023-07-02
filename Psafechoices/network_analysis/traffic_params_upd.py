"""
Shapefiles reader and traffic parameters updater

@author: ptzouras
National Technical University of Athens
"""

# packages
import pandas as pd


def read_shapefile(shp_path): # function which translates shapefiles to dataframes!

	import shapefile # it needs pyshp package

	#read file, parse out the records and shapes
	sf = shapefile.Reader(shp_path)
	fields = [x[0] for x in sf.fields][1:]
	records = sf.records()
	shps = [s.points for s in sf.shapes()]

	#write into a dataframe
	df = pd.DataFrame(columns=fields, data=records)
	df = df.assign(coords=shps)

	return df



# current_dir = os.path.dirname(os.path.realpath(__file__))
# os.chdir(current_dir)
# lin = read_shapefile('networks_shp/new_equil/simple_network_links.shp')
# nod = read_shapefile('networks_shp/new_equil/simple_network_nodes.shp')

# check stability, 
# lin.loc[5,'x_start']=88 # if, we have coordinates that do not match with a node in the link data
# nod.loc[14,'x']=0 # if we have more than on nodes in the same location - same coordinates
# nod.loc[14,'x']=0

def nod_match(links,nodes):
    for i in range(0,len(links)): 
        fr1 = nodes.loc[(nodes.x==links.loc[i,'x_start']) & (nodes.y==links.loc[i,'y_start']),'id']
        fr2 = nodes.loc[(nodes.x==links.loc[i,'x_end']) & (nodes.y==links.loc[i,'y_end']),'id']
        if len(fr1)>0: # check if you found matches, if not 9999
           links.loc[i,'from1']=fr1.iloc[0] # select each time the first match
        else: links.loc[i,'from1'] = 999
        if len(fr2)>0:
           links.loc[i,'to1']=fr2.iloc[0]
        else: links.loc[i,'to1'] = 999
    return links.from1, links.to1

def twoway(df, no_resp_prior = ''):
    
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
    
    print(c)
    print(l)
    
    return df

def speed(df, cr = 1, delr = 1):
    
    # cr = is the compliance, where 1 means freespeed = speedlimit.
    # delr = the ration between the actual speed and the freeflow speed.
    # 1 means no congestion, but also means no delay due to interactions.
    
    df.freespeed = delr * (cr * df.freespeed*1000/3600)
    return df

def capacity(df, dwn = 1, simp = 'simple',  w = 13.5, kjam = 125):
    
    # dwn is the level of the downscale you do at the end. 
    # w the wave speed that the cells propagate backwards
    # kjam is the jam density, change them only if simp == 'kinematic_waves'
    
    # df.freespeed = df.freespeed * 3600/1000
    
    freespeed = df.freespeed * 3600/1000
    
    for i in range(0,len(df)):
        if simp == 'simple': 
            df.loc[i, 'capacity'] = dwn * (df.permlanes.iloc[i]*1200) # very simplistic approach.
        elif simp == 'kinematic_waves':
            df.loc[i, 'capacity']= dwn * (df.permlanes.iloc[i] * kjam * freespeed.iloc[i] * w)/(freespeed.iloc[i] + w)
        else: df.capacity.iloc[i] = 9999 # here a new extension will be written based on speed compliance rate and speed limit
    return df

# DELETE DELETE NOT NECESSARY
def upd_links(lin, nod):
    # macth nodes id with links, starting - ending point
    lin['from1']=999 # node id = 999 id, if unmatched - set from the beginning
    lin['to1']=999
    [lin.from1,lin.to1]=nod_match(lin, nod) # determine from / to nodes id based on x,y coordinates of starting ana ending points
    # lin=lin.drop(columns=['x_start','y_start','x_end','y_end'])
    # create uni-directional links, by making a new one
    lin = twoway(lin).replace({0:1})
    # update the capacity of the links
    lin = speed(lin)
    lin = capacity(lin, 'yes')
    # lin.modes = lin.modes.replace({'car,bicycle':'bicycle,car'})
    return lin
