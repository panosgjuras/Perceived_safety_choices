import pandas as pd
import dijkstra as dij
import os
import math

from Psafechoices.choice_model import opp_cost_calculator as opp

def simulate_params(lin, nod, fr, to, minv, dmin, mode, coeff, speed, dcost, scenario):
    coeff = opp.opp_cost_calc(coeff, mode, speed, dcost)
    mth = 'best'
    df = pd.DataFrame(columns =['dmin', 'minv', 'dist', 'seq', 'scenario'])
    for m in minv:
        for d in dmin: 
            path = dij.dij_run(lin, nod, mode, fr, to, mth, m, d, coeff)
            dist = dij.dij_dist_calc (path, lin)
            d = {'dmin':[d], 'minv':[m], 'dist':[dist], 'mode':[mode], 'seq': [path], 'scenario': [scenario]}
            df = df.append(pd.DataFrame(d), ignore_index=True)
    return df

def define_paths(sdf, mode):
    d = {'dist':sdf["dist"].unique(), 'path': range(1, 1 + len(sdf["dist"].unique()))}
    df = pd.DataFrame(d)
    df["path"] = df["path"] - 1
    df["path"] = mode + ' path ' + df["path"].astype(str)
    for i in range(0, len(df)):
        if df.dist.iloc[i] == 999999: df.path.iloc[i] = 'no path'
        sdf = pd.merge(left=sdf, right=df, how="inner", left_on='dist', right_on='dist')
        return sdf

def show_unique(df):
    ndf = df[["path", "dist", "scenario"]]
    ndf = ndf.sort_values(["path","dist", "scenario"]).drop_duplicates("path")
    return ndf
