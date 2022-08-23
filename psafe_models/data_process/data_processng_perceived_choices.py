"""
Data processing perceived safety rating data

@author: ptzouras
National Technical University of Athens
"""
import pandas as pd
import os
import numpy as np

####### GENERAL
current_dir = os.path.dirname(os.path.realpath(__file__)) 
os.chdir(current_dir)
x=100
b1 = pd.read_csv('raw_data/raw_data_perceived_choices_block1.csv', ',')
b1["pid"]=range(x,len(b1.index)+x)
x=200
b2 = pd.read_csv('raw_data/raw_data_perceived_choices_block2.csv', ',')
b2["pid"]=range(x,len(b2.index)+x) 
x=300
b3 = pd.read_csv('raw_data/raw_data_perceived_choices_block3.csv', ',') 
b3["pid"]=range(x,len(b3.index)+x) 
####### GENERAL


def sociodemo(df):
    # Rename sociodemo columns
    df=df.rename(columns={'Φύλο:':'gender','Ηλικία:':'age','Επίπεδο εκπαίδευσης:':'education','Κύρια απασχόληση:':'employment','Κύρια απασχόληση: ':'employment',
                    'Καθαρό μηνιαίο (ατομικό) εισόδημα:':'income',
                    'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Συμβατικό Αυτοκίνητο':'car',
                    'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Ηλεκτρικό Αυτοκίνητο':'ecar',
                    #'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Φορτηγό - Ημιφορτηγό (Βαν)':'truck', # PANOS: not necessary for our analysis drop it
                    'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Μηχανή':'motorcycle',
                    'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Ποδήλατο':'bike', # PANOS: here you set bike but after bicycle
                    'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Ηλεκτρικό Ποδήλατο':'ebike',
                    'Πόσα οχήματα έχετε στην οικογένεια (νοικοκυριό) σας;  - Ηλεκτρικό Πατίνι':'escoot'})
                    #'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Ποδήλατο':'bike_frequency', # no_replaces here, I will add code
                    #'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Ηλεκτρικό πατίνι':'escooter_frequency', # no_replaces here, I will add code
                    #'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Λεωφορείο, Τρόλεϊ κλπ.':'PT_frequency', # no_replaces here, I will add code
                    #'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Μετρό, Προαστιακός, Τραμ κλπ.':'metro_frequency'}) # no_replaces here, I will add code
    
    # replace gender
    df.gender = df.gender.replace({'Γυναίκα':0,'Άνδρας':1,'Δεν απαντώ':0, np.nan:0})
    # replace age
    df.age = df.age.replace({'Μικρότερος/η απο 18 ετών': 0,'18-30 ετών': 1, '31-40 ετών': 2, 
                       '41-50 ετών': 3,'51-65 ετών': 4,
                       'Μεγαλύτερος/η από 65 ετών': 5,'Δεν απαντώ':np.nan})
    
    df['young'] = np.where(df.age<=1, 1, 0)
    
    # replace education
    df.education=df.education.replace({'Πρωτοβάθμια Εκπαίδευση (δηλ. Νηπιαγωγείο, Δημοτικό )':1,
                                  'Δευτεροβάθμια Εκπαίδευση (δηλ. Γυμνάσιο, Γενικό ή Επαγγελματικό Λύκειο, κλπ)':2,
                                  'Τριτοβάθμια Εκπαίδευση (δηλ. Πανεπιστήμιο, ΤΕΙ)':3,
                                  'Μεταπτυχιακές ή Διδακτορικές Σπουδές':4,
                                  'Χωρίς Εκπαίδευση':0,
                                  'Δεν απαντώ':np.nan})
    # replace employment
    df.employment=df.employment.replace({'Οικιακά':0,'Μαθητής/τρια - Φοιτητής/τρια':1,'Άνεργος/η':2,
                                   'Ελεύθερος Επαγγελματίας - Επιχειρηματίας':3,
                                   'Δημόσιος - Ιδιωτικός Υπάλληλος':3,'Εργάτης - Τεχνίτης':3,
                                   'Αγρότης - Κτηνοτρόφος':3,'Συνταξιούχος':0,'Δεν απαντώ':np.nan,
                                   'Μαθητής/τρία - Φοιτητής/τρια':1})
    # replace income
    df.income=df.income.replace({'Δεν έχω εισόδημα':0,
                                'Λιγότερα από 750 ευρώ/μήνα':1,
                                '750-1500 ευρώ/μήνα':2,
                                '1500-2500 ευρώ/μήνα':3,
                        'Περισσότερα από 2500 ευρώ/μήνα':4,
                        'Δεν απαντώ':np.nan })
    # replace number of vehicles
    if df.dtypes['car']=='O': # if it is still an object and not an integer or float
       df.car= df.car.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0,' 3 ή περισσότερα':3}) 
    if df.dtypes['ecar']=='O': df.ecar=df.ecar.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0,' 3 ή περισσότερα':3})

       ##df.truck.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0}) 
    
    # vehicle ownership lines
    if df.dtypes['motorcycle']=='O': df.motorcycle = df.motorcycle.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0,' 3 ή περισσότερα':3})
    if df.dtypes['bike']=='O': df.bike = df.bike.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0,' 3 ή περισσότερα':3})
    if df.dtypes['ebike']=='O':df.ebike = df.ebike.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0,' 3 ή περισσότερα':3})
    if df.dtypes['escoot']=='O':df.escoot = df.escoot.replace({'Κανένα':0,'1':1,'2':2,'3 ή περισσότερα':3, np.nan:0,' 3 ή περισσότερα':3})
    
    df['car_own']=np.where((df.car>=1) | (df.ecar>=1), 1, 0) # car_own = 1, yes I own a car - dummy variable
    df['moto_own']=np.where(df.motorcycle>=1, 1, 0)
    df['cycle_own']=np.where((df.bike>=1) | (df.ebike>=1), 1, 0)
    df['ecar_own']=np.where(df.ecar>=1, 1, 0) 
    df['escoot_own']=np.where(df.escoot>=1, 1, 0)
    
    df=df.rename(columns={'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Ποδήλατο':'bike_frequency',
                          'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Ηλεκτρικό πατίνι':'escooter_frequency', 'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Ηλεκτρικό Πατίνι':'escooter_frequency',
                          'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Λεωφορείο, Τρόλεϊ κλπ.':'PT_frequency',
                          'Πόσο συχνά χρησιμοποιείτε τα ακόλουθα μέσα μετακίνησης;  - Μετρό, Προαστιακός, Τραμ κλπ.':'metro_frequency'})
    # mode frequency lines
    df.bike_frequency=df.bike_frequency.replace({'Σχεδόν ποτέ':0,'Μερικές φορές τον χρόνο':1,'Μερικές φορές την εβδομάδα':3,'Μερικές φορές το μήνα':2,'Μερικές φορές τον μήνα':2,'Καθημερινά':4})
    df.escooter_frequency=df.escooter_frequency.replace({'Σχεδόν ποτέ':0,'Μερικές φορές τον χρόνο':1,'Μερικές φορές την εβδομάδα':3,'Μερικές φορές το μήνα':2,'Μερικές φορές τον μήνα':2,'Καθημερινά':4})
    df.PT_frequency=df.PT_frequency.replace({'Σχεδόν ποτέ':0,'Μερικές φορές τον χρόνο':1,'Μερικές φορές την εβδομάδα':3,'Μερικές φορές το μήνα':2,'Μερικές φορές τον μήνα':2,'Καθημερινά':4})
    df.metro_frequency=df.metro_frequency.replace({'Σχεδόν ποτέ':0,'Μερικές φορές τον χρόνο':1,'Μερικές φορές την εβδομάδα':3,'Μερικές φορές το μήνα':2,'Μερικές φορές τον μήνα':2,'Καθημερινά':4})
    
    return df

socio=pd.DataFrame(sociodemo(b1), columns=['pid','gender','age','education','employment',
                   'income','car_own','moto_own','cycle_own','escoot_own','bike_frequency', 'escooter_frequency', 'PT_frequency',
                   'metro_frequency', 'young'])
socio = pd.concat([socio, pd.DataFrame(sociodemo(b2), columns=['pid','gender','age','education','employment',
                   'income','car_own','moto_own','cycle_own','escoot_own','bike_frequency', 'escooter_frequency', 'PT_frequency',
                   'metro_frequency','young'])], axis=0, ignore_index=True)
socio = pd.concat([socio, pd.DataFrame(sociodemo(b3), columns=['pid','gender','age','education','employment',
                   'income','car_own','moto_own','cycle_own','escoot_own','bike_frequency', 'escooter_frequency', 'PT_frequency',
                   'metro_frequency', 'young'])], axis=0, ignore_index=True)
socio.set_index('pid').to_csv('datasets/socio_dataset_perceived_choices.csv') # save dataset with sociodemographic characteristics

def sc_ren_rep(df,tmode,block): # PANOS: this function renames and replaces scenarios for each mode
    sc=list(df.columns) # save the columns of the dataframe (raw data) in a list
    if tmode=='car': i=18 # if car start i from 18, so 18th row in the list is the first evalution of car perceived safety
    elif tmode=='ebike': i=19 # so e-bike will be at 19th and goes on
    elif tmode=='escoot': i=20
    else: i=21
    # DOUBLE CHECK DOUBLE CHECK
    new_df=pd.DataFrame(df,columns=['pid',sc[i], sc[i+5], sc[i+10], sc[i+15],sc[i+20],
                                sc[i+25],sc[i+30], sc[i+35], sc[i+40], sc[i+45], sc[i+50], sc[i+55]]) # create a new dataframe with the evaluations only
    if block==3: # rename the columns, this is only for block 3, new lines of code for other blocks are required
        new_df=new_df.rename(columns={sc[i]:'scenario35', sc[i+5]:'scenario30', sc[i+10]: 'scenario12', sc[i+15]:'scenario31',sc[i+20]:'scenario01',
                                sc[i+25]:'scenario20',sc[i+30]:'scenario09', sc[i+35]:'scenario34', sc[i+40]:'scenario15',
                                sc[i+45]:'scenario14', sc[i+50]:'scenario17', sc[i+55]:'scenario04'}) # renames based on the list
    if block==2: 
        new_df=new_df.rename(columns={sc[i]:'scenario25', sc[i+5]:'scenario22', sc[i+10]: 'scenario03', sc[i+15]:'scenario28',sc[i+20]:'scenario08',
                                sc[i+25]:'scenario23',sc[i+30]:'scenario18', sc[i+35]:'scenario33', sc[i+40]:'scenario02',
                                sc[i+45]:'scenario36', sc[i+50]:'scenario05', sc[i+55]:'scenario19'}) # renames based on the list
    if block==1: 
        new_df=new_df.rename(columns={sc[i]:'scenario11', sc[i+5]:'scenario06', sc[i+10]: 'scenario24', sc[i+15]:'scenario07',sc[i+20]:'scenario13',
                                sc[i+25]:'scenario32',sc[i+30]:'scenario10', sc[i+35]:'scenario21', sc[i+40]:'scenario26',
                                sc[i+45]:'scenario27', sc[i+50]:'scenario16', sc[i+55]:'scenario29'}) # renames based on the list
    for item in list(new_df.columns): # change the evaluations
        if item!='pid' and new_df.dtypes[item]=='O':
            new_df[item]=new_df[item].replace({'1: Καθόλου ασφαλής':1,'2':2,'3':3,'4: Μέτρια Ασφαλής':4, '4:  Μέτρια ασφαλής':4, '4: Μέτρια ασφαλής ':4,
                                             '4: Μέτρια ασφαλής':4,'5':5,'6':6,'7: Πολύ ασφαλής':7, '7: Πόλυ ασφαλής':7})
    new_df['tmode']=tmode # save the mode in a new column
    return new_df # create a new dataframe

def expl_rat():
    expl=pd.read_csv('scenarios/rating_scenarios_perceived_choices.csv', ',') # import scenario table
    expl=expl.set_index('scenario') # set index, i.e. the scenario name
    expl['type1']=np.where(expl.type==1, 1, 0) # PANOS: I developed dummy coding for infrastructure variables (non-linearities)
    # we will speak about it, it is a technique
    # DUMMY CODING ...
    # 0 is always the worst, so 0 is bad condition and 0 is obstacles
    expl['type2']=np.where(expl.type==2, 1, 0)
    expl['type3']=np.where(expl.type==3, 1, 0)
    expl['type4']=np.where(expl.type==4, 1, 0)
    expl['cross1']=np.where(expl.cross==1,1,0) 
    expl['cross2']=np.where(expl.cross==2, 1, 0)
    expl.veh=expl.veh.replace({1:100,2:60,3:20}) # replace the continuous x-variables
    expl.bike=expl.bike.replace({1:90, 2:50, 3:10})
    expl.ped=expl.ped.replace({1:25, 2:15, 3:5})
    return expl

def rate_dat(df,tmode): # transpose scenario ratings from columns into rows, so 12 rows per respondent 
    new_df=pd.DataFrame(columns=('pid','scenario','tmode','psafe')) 
    for item in list(df.columns):
        if item!='pid' and item!='mode': # play only with scenario columns
            k=pd.DataFrame(columns=('pid','scenario','tmode','psafe')) # change the format
            k['pid']=df["pid"] # keep pids as it is
            k['scenario']=item # save scenario number in a column, this column will be used for merge
            k['tmode']=tmode # mode as you gave it in the function inputs
            k['psafe']=df[item] # add the evaluation per scenario
            new_df = pd.concat([new_df, k], axis=0, ignore_index=True).dropna() # next scenario, next iteration
    new_df = pd.merge(left=new_df, right=expl_rat(), how="inner", left_on='scenario', right_on='scenario') 
    # merge with the dataset of explanatory variables
    return new_df

def rating_1(a,x): # create the rating dataset, for the first block, all modes in one dataset...
    rating = rate_dat(sc_ren_rep(a,'car',x),'car')
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'ebike',x),'ebike')], axis=0, ignore_index=True) 
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'escoot',x),'escoot')], axis=0, ignore_index=True)
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'walk',x),'walk')], axis=0, ignore_index=True)
    return rating

def rating_2(a,x,rating): # create the rating dataset, for the next blocks via pd.concat
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'car',x),'car')], axis=0, ignore_index=True)
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'ebike',x),'ebike')], axis=0, ignore_index=True) # add all modes in one dataset
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'escoot',x),'escoot')], axis=0, ignore_index=True)
    rating = pd.concat([rating, rate_dat(sc_ren_rep(a,'walk',x),'walk')], axis=0, ignore_index=True)
    return rating

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

rate = rating_1(b3,3)
rate = rating_2(b2,2, rate)
rate = rating_2(b1,1, rate)
# at the end, how many observations of psafe? number of respondents in raw data * 12 scenario * 4 modes 
rate =  pd.merge(left= rate, right=socio, how="inner", left_on='pid', right_on='pid') # merge socio with rate dataset

rate = rate.set_index('pid')
rate = drop_cor(rate, find_low(b1, b2, b3)[0], find_low(b1, b2, b3)[1], find_low(b1, b2, b3)[2])
rate.to_csv('datasets/rating_dataset_perceived_choices.csv') # save the final rating dataset with no correlations