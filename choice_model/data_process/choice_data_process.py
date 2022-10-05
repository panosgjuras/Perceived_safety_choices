"""
Choice data processing

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
import os
import numpy as np

####### GENERAL
#current_dir = os.path.dirname(os.path.realpath(__file__)) 
#os.chdir(current_dir)

#x=100
#b1 = pd.read_csv('raw_data/raw_data_perceived_choices_block1.csv', ',')
#b1["pid"]=range(x,len(b1.index)+x)
#x=200
#b2 = pd.read_csv('raw_data/raw_data_perceived_choices_block2.csv', ',')
#b2["pid"]=range(x,len(b2.index)+x) 
#x=300
#b3 = pd.read_csv('raw_data/raw_data_perceived_choices_block3.csv', ',') 
#b3["pid"]=range(x,len(b3.index)+x)

#rate = pd.read_csv('ratings/rating_dataset_perceived_choices.csv', ',')
#socio = pd.read_csv('ratings/socio_dataset_perceived_choices.csv', ',')
####### GENERAL

def revese_fun(mat,x): # this function matches choice scenarios with rating scenarios
    match =  pd.read_csv(os.path.join(
        os.path.dirname(__file__), 'scenarios','SC_SCC.csv'
        ), sep=',')
    if x==1:
        mat = match.loc[match.sc == mat, 'scc'] # from rating scenarios to choice scenarios
        if len(mat)>0: new_mat = mat.iloc[0]
        else: new_mat = 'scenario999'
    elif x==2:
        mat = match.loc[match.scc == mat, 'sc'] # inverse function: from choice to ratings
        if len(mat)>0: new_mat = mat.iloc[0]
        else: new_mat = 'scenario999'
    else:
        new_mat = 'scenario 999'
    return new_mat

def sc_ch_rep(df,block): # PANOS: this function renames scenarios for each mode for choice experiment
    sc=list(df.columns) # save the columns of the dataframe (raw data) in a list
    i = 22
    # DOUBLE CHECK DOUBLE CHECK
    match =pd.read_csv(os.path.join(
        os.path.dirname(__file__), 'scenarios', 'SC_SCC.csv'
        ), sep=',') # not necessary, as there is a function, i should be fixed
    match = match.set_index('sc')
    new_df=pd.DataFrame(df,columns=['pid',sc[i], sc[i+5], sc[i+10], sc[i+15],sc[i+20],
                                sc[i+25],sc[i+30], sc[i+35], sc[i+40], sc[i+45], sc[i+50], sc[i+55]]) # create a new dataframe with the evaluations only
    if block==3: # rename the columns, this is only for block 3, new lines of code for other blocks are required
        new_df=new_df.rename(columns={sc[i]: match.loc['scenario35','scc'], sc[i+5]: match.loc['scenario30','scc'], sc[i+10]: match.loc['scenario12','scc'], 
                                      sc[i+15]: match.loc['scenario31','scc'],sc[i+20]: match.loc['scenario01','scc'], 
                                      sc[i+25]: match.loc['scenario20','scc'],sc[i+30]: match.loc['scenario09','scc'], sc[i+35]: match.loc['scenario34','scc'], 
                                      sc[i+40]: match.loc['scenario15','scc'], sc[i+45]: match.loc['scenario14','scc'], 
                                      sc[i+50]: match.loc['scenario17','scc'], sc[i+55]: match.loc['scenario04','scc']}) # renames based on the list
    if block==2:
        new_df=new_df.rename(columns={sc[i]:match.loc['scenario25','scc'], sc[i+5]: match.loc['scenario22','scc'], sc[i+10]: match.loc['scenario03','scc'], 
                                      sc[i+15]: match.loc['scenario28','scc'],sc[i+20]: match.loc['scenario08','scc'],
                                      sc[i+25]: match.loc['scenario23','scc'],sc[i+30]: match.loc['scenario18','scc'], 
                                      sc[i+35]: match.loc['scenario33','scc'], sc[i+40]: match.loc['scenario02','scc'],
                                      sc[i+45]:match.loc['scenario36','scc'], sc[i+50]: match.loc['scenario05','scc'], 
                                      sc[i+55]:match.loc['scenario19','scc']}) # renames based on the list
    if block==1: 
        new_df=new_df.rename(columns={sc[i]: match.loc['scenario11','scc'], sc[i+5]: match.loc['scenario06','scc'], 
                                      sc[i+10]: match.loc['scenario24','scc'], sc[i+15]: match.loc['scenario07','scc'],sc[i+20]: match.loc['scenario13','scc'],
                                      sc[i+25]: match.loc['scenario32','scc'], sc[i+30]: match.loc['scenario10','scc'], 
                                      sc[i+35]: match.loc['scenario21','scc'], sc[i+40]: match.loc['scenario26','scc'],
                                      sc[i+45]: match.loc['scenario27','scc'], sc[i+50]: match.loc['scenario16','scc'], sc[i+55]: match.loc['scenario29','scc']}) # renames based on the list 
    return new_df # create a new dataframe

def choice_repl(df):
    sc = list(df.columns)
    for i in range(0, len(df)):
        for j in range(1,13):
            if pd.isna(df[sc[j]].iloc[i]):
                wor = np.nan
                text = ' '
            else:
                text = df[sc[j]].iloc[i]

            if 'Αυτοκίνητο' in text : wor = 'car' # if this word is in the text, in wor keep car
            elif 'Κοινόχρηστο ηλεκτρικό ποδήλατο' in text: wor ='ebike'
            elif 'Κοινόχρηστο ηλεκτρικό πατίνι' in text: wor ='escoot'
            elif 'Περπάτημα' in text: wor = 'walk'
            else: wor = np.nan
            df[sc[j]].iloc[i] = wor # problem it says...slice df etc.
    
    return df

def choice_expl(): # it loads the choice explanatory dataset.
    expl=pd.read_csv(os.path.join(
        os.path.dirname(__file__), 'scenarios', 'choice_scenarios_perceived_choices.csv'
    ), sep=',') # import scenario table
    expl=expl.set_index('scenario') # set index, i.e. the scenario name
    expl.cartime=expl.cartime.replace({1:40,2:20,3:5}) # replace the leveles with real times, and costs
    expl.carcost=expl.carcost.replace({1:3.5,2:5,3:6.5})
    expl.acttime=expl.acttime.replace({1:25,2:15,3:5})
    expl.ebikecost=expl.ebikecost.replace({1:1.5,2:3,3:4.5})
    expl.escootcost=expl.escootcost.replace({1:0.5,2:2,3:3.5})
    return expl

def choice_dat(df): # transpose scenario choices from columns into rows, so 12 rows per respondent 
    new_df=pd.DataFrame(columns=('pid','scenario','choice')) 
    for item in list(df.columns):
        if item!='pid': # play only with scenario columns
            k=pd.DataFrame(columns=('pid','scenario','choice')) # change the format
            k['pid']=df["pid"] # keep pids as it is
            k['scenario']=item # save scenario number in a column, this column will be used for merge
            k['choice']=df[item] # add the evaluation per scenario
            new_df = pd.concat([new_df, k], axis=0, ignore_index=True).dropna() # next scenario, next iteration
    new_df = pd.merge(left=new_df, right=choice_expl(), how="inner", left_on='scenario', right_on='scenario') 
    # merge with the dataset of explanatory variables
    return new_df

def psafe_match(rdf, cdf): # function that matces choices with psafe ratings of each respondent for each mode
     for i in range(0, len(cdf)):
         fr1 = rdf.loc[(rdf.pid == cdf.pid.iloc[i]) & (rdf.scenario == revese_fun(cdf.scenario.iloc[i],2)) & (rdf.tmode == 'car'), 'psafe']
         fr2 = rdf.loc[(rdf.pid == cdf.pid.iloc[i]) & (rdf.scenario == revese_fun(cdf.scenario.iloc[i],2)) & (rdf.tmode == 'ebike'), 'psafe']
         fr3 = rdf.loc[(rdf.pid == cdf.pid.iloc[i]) & (rdf.scenario == revese_fun(cdf.scenario.iloc[i],2)) & (rdf.tmode == 'escoot'), 'psafe']
         fr4 = rdf.loc[(rdf.pid == cdf.pid.iloc[i]) & (rdf.scenario == revese_fun(cdf.scenario.iloc[i],2)) & (rdf.tmode == 'walk'), 'psafe']

         if len(fr1)>0: cdf.loc[i, 'carpsafe'] = fr1.iloc[0]
         else: cdf.loc[i, 'carpsafe'] = np.nan
        
         if len(fr2)>0: cdf.loc[i, 'ebikepsafe'] = fr2.iloc[0]
         else: cdf.loc[i, 'ebikepsafe'] = np.nan
        
         if len(fr3)>0: cdf.loc[i, 'escootpsafe'] = fr3.iloc[0]
         else: cdf.loc[i, 'escootpsafe'] = np.nan
        
         if len(fr4)>0: cdf.loc[i, 'walkpsafe'] = fr4.iloc[0]
         else: cdf.loc[i, 'walkpsafe'] = np.nan
     return cdf

def int_choice(df):
    df['intchoice']= df.choice.replace({'car':4, 'ebike':3, 'escoot':2, 'walk':1}) # BIOGEME does not use categories, it utilizes number for choice
    df['binchoice1'] = np.where(df.intchoice==4, 1, 0) # create a new choice variable for binary logit
    df['binchoice2'] = np.where(df.intchoice==3, 1, 0) 
    df['binchoice3'] = np.where(df.intchoice==2, 1, 0) 
    df['binchoice4'] = np.where(df.intchoice==1, 1, 0) 
    return df

def find_low(df1, df2, df3): # function that reduces sample size, so that same number of observations per block
    # through this function, correlations among x-variables are minimized
    sam = min(len(df1), len(df2), len(df3))
    diff1 = 0
    diff2 = 0
    diff3 = 0
    if len(df1)<=len(df2):
        if len(df1)<=len(df3):
            diff2 = len(df2) - sam
            diff3 = len(df3) - sam
        else:
            diff1 = len(df1) - sam
            diff2 = len(df2) - sam
    else:
        if len(df2)<=len(df3):
            diff1 = len(df1) - sam
            diff3 = len(df3) - sam
        else:
            diff1 = len(df1) - sam
            diff2 = len(df2) - sam
    return diff1, diff2, diff3

def drop_cor(df, diff1, diff2, diff3):
    for i in range(100, 100 + diff1): df = df.drop(index = i)
    for i in range(200, 200 + diff2): df = df.drop(index = i)
    for i in range(301, 301 + diff3): df = df.drop(index = i)
    return df

def drop_row(df):
    df = df[df['carpsafe'].notna()]
    df = df[df['ebikepsafe'].notna()]
    df = df[df['escootpsafe'].notna()]
    df = df[df['walkpsafe'].notna()]
    return df

def choice_dats(df1, df2, df3, rdf, sdf):
    choice = choice_dat(choice_repl(sc_ch_rep(df1,1)))
    choice = pd.concat([choice, choice_dat(choice_repl(sc_ch_rep(df2,2)))], axis=0, ignore_index=True)
    choice = pd.concat([choice, choice_dat(choice_repl(sc_ch_rep(df3,3)))], axis=0, ignore_index=True)
    choice =  pd.merge(left=choice, right=sdf, how="inner", left_on='pid', right_on='pid')
    choice = psafe_match(rdf, choice)
    choice = int_choice(choice)
    # choice = choice.set_index('pid')
    choice = drop_cor(choice, find_low(df1, df2, df3)[0], find_low(df1, df2, df3)[1], find_low(df1, df2, df3)[2]) # save the final choice dataset with no correlations
    choice = drop_row(choice)
    return choice