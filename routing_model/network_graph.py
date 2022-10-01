
import pandas as pd
import dijkstra as dij
import os

# current_dir = os.path.dirname(os.path.realpath(__file__)) 
os.chdir('C:/Users/panos/Desktop/github_tzouras/Perceived_safety_choices/network_analysis')
nodes = pd.read_csv("output_csv/experimental_field_athens_nod_coord.csv")
links = pd.read_csv("output_csv/experimental_field_athens_links_psafe.csv")
os.chdir('C:/Users/panos/Desktop/github_tzouras/Perceived_safety_choices/routing_model')
coeff = pd.read_csv("coeff_choice_model.csv").set_index('param')

def utils_cal(df, cf, dmax):
    df["car_utils"] = - ( cf.loc['btime', 'car'] * (df.length/(cf.loc['speed', 'car'] * 1000)) \
        + cf.loc['bcost', 'car'] * (cf.loc['consum', 'car']/1000) * cf.loc['ltcost', 'car'] * df.length \
        + cf.loc['bpsafe', 'car'] * (df.car_psafe_l - 4) * (df.length/dmax))
    
    df["ebike_utils"] = - (cf.loc['btime', 'ebike'] * (df.length/(cf.loc['speed', 'ebike'] * 1000)) \
        + cf.loc['bcost', 'ebike'] * (cf.loc['speed', 'ebike']/(cf.loc['speed', 'ebike'] * 1000)) * df.length \
        + cf.loc['bpsafe', 'ebike'] * (df.ebike_psafe_l - 4) * (df.length/dmax))
    
    df["escoot_utils"] = - (cf.loc['btime', 'escooter'] * (df.length/(cf.loc['speed', 'escooter'] * 1000)) \
        + cf.loc['bcost', 'escooter'] * (cf.loc['speed', 'escooter']/(cf.loc['speed', 'escooter'] * 1000)) * df.length \
        + cf.loc['bpsafe', 'escooter'] * (df.escoot_psafe_l - 4) * (df.length/dmax))
    
    df["walk_utils"] = - (cf.loc['btime', 'walk'] * (df.length/(cf.loc['speed', 'walk']  * 1000)) \
        + cf.loc['bpsafe', 'walk'] * (df.walk_psafe_l - 4) * (df.length/dmax))
    return df

def dij_graph(ln, tmode, minv, mth):
    graph = dij.Graph()
    
    for i in range(0, len(ln)):
        x = 0
        if tmode == 'car':
            psafe = ln.car_psafe_l.iloc[i]
            weight = ln.car_utils.iloc[i]
        elif tmode == 'ebike':
            psafe = ln.ebike_psafe_l.iloc[i]
            weight = ln.ebike_utils.iloc[i]
        elif tmode == 'escooter':
            psafe = ln.escoot_psafe_l.iloc[i]
            weight = ln.escoot_utils.iloc[i]          
        elif tmode == 'walk':
            psafe = ln.walk_psafe_l.iloc[i]
            weight = ln.walk_utils.iloc[i]
        else:
            x = 999
            print('no mode')
            break
        if mth == 'shortest': weight = ln.length.iloc[i]
        elif mth == 'best': weight = weight 
        else: 
            x = 999
            print('wrong method')
            break
        text = ln.modes.iloc[i]
        if tmode in text:
            if psafe>=minv: graph.add_edge(ln.from1.iloc[i], ln.to1.iloc[i], weight)    
    return graph, x

def dij_run(ln, nd, tmode, fr, to, mth, minv, dmax, coeff):
    
    ln = utils_cal(ln, coeff, dmax)
    
    graph = dij_graph(ln, tmode, minv, mth)[0]
    check = dij_graph(ln, tmode, minv, mth)[1]
    
    if check != 999:
        dijkstra = dij.DijkstraSPF(graph, fr)
        nod = list(nd.id)
        # print("%-5s %-5s" % ("label", "distance"))
        # for u in nod: 
        #    print(u, dijkstra.get_distance(u))
        print(dijkstra.get_path(to))
        x = dijkstra.get_path(to)
    return x 

def dij_dist_calc (path, ln):
    suml = 0
    for i in range (len(path) - 1):
        matchid = ln.index[(ln.from1 == path[i]) & (ln.to1 == path[i + 1])].tolist()
        add = ln.loc[(ln.from1 == path[i]) & (ln.to1 == path[i + 1]), 'length']
        suml = suml + add[matchid[0]]
    return suml

path = dij_run(links, nodes, 'car', 9000, 4000, 'shortest', 2, 10000, coeff)
path_length = dij_dist_calc (path, links)
print(path_length)
