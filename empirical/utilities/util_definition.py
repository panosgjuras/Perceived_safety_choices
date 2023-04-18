import pandas as pd
import biogeme.database as db

def dat_defin(x, NAME, expr, database):
    if x == 1:
        var = DefineVariable(NAME, expr, database)
    if x == 2:
        var = database.DefineVariable(NAME, expr)
    return var

class database:
    def __init__(self, link, typ):
        self.link = link
        self.typ = typ
        self.set_dbase(link, typ)
    
    def set_dbase(self, link, typ):
        df = pd.read_csv(link,',')
        df = df.drop(columns = ['scenario','choice', 'gender', 'age', 'education', 'employment',
                    'income', 'car_own', 'moto_own', 'cycle_own', 'escoot_own',
                    'bike_frequency', 'escooter_frequency', 'PT_frequency',
                    'metro_frequency', 'young'])
        
        dbs = db.Database('Perceived&choices', df.dropna())
        dbs.panel('pid')
        
        globals().update(dbs.variables)
        CARTIME = dat_defin(typ,'CARTIME', cartime, dbs)
        CARCOST = dat_defin(typ,'CARCOST', carcost, dbs)
        CARPSAFE = dat_defin(typ,'CARPSAFE',carpsafe - 4, dbs)

        EBIKETIME = dat_defin(typ,'EBIKETIME',acttime, dbs) # new time variables based on the difference among modes
        EBIKECOST = dat_defin(typ,'EBIKECOST',ebikecost, dbs)
        EBIKEPSAFE = dat_defin(typ,'EBIKEPSAFE',ebikepsafe - 4, dbs)
                 
        ESCOOTIME = dat_defin(typ,'ESCOOTIME', (20/15) * acttime, dbs) # new time variables based on the difference among modes
        ESCOOTCOST = dat_defin(typ,'ESCOOTCOST', escootcost, dbs) # new time variables based on the difference among modes
        ESCOOTPSAFE = dat_defin(typ,'ESCOOTPSAFE', escootpsafe - 4, dbs)
        
        WALKTIME = dat_defin(typ,'WALKTIME',  (20/5) * acttime, dbs) # new time variables based on the difference among modes
        WALKPSAFE = dat_defin(typ,'WALKPSAFE',walkpsafe - 4, dbs)
        
        self.__dbase = dbs
     
    def get_dbase(self):
        return self.__dbase


class utils:
    
    def __init__(self, dbs, b, rnds = 0, exp = 'mode_choice', typ = 1):        
        self.set_MNLVs(dbs, b)
        self.set_MLVs(dbs, b, rnds)
        self.set_Bincar_RND(dbs, b, rnds)
        self.set_Binebike_RND(dbs, b, rnds)
        self.set_Binesoot_RND(dbs, b, rnds)
        self.set_Binwalk_RND(dbs, b, rnds)
        self.set_modecho_av(exp)
        self.set_cho(dbs, exp, typ)

    def set_MNLVs(self, dbs, b):
        globals().update(dbs.variables)
        V1 = b.CARTIME * CARTIME + b.CARCOST * CARCOST + b.CARPSAFE * CARPSAFE
        V2 = b.ASC_EBIKE + b.EBIKETIME * EBIKETIME + b.EBIKECOST * EBIKECOST + b.EBIKEPSAFE * EBIKEPSAFE
        V3 = b.ASC_ESCOOT + b.ESCOOTIME * ESCOOTIME + b.ESCOOTCOST * ESCOOTCOST + b.ESCOOTPSAFE * ESCOOTPSAFE
        V4 = b.ASC_WALK + b.WALKTIME * WALKTIME + b.WALKPSAFE * WALKPSAFE
        V = {4: V1, 3: V2, 2: V3, 1:V4}
        self.__MNLVs = V
    
    def get_MNLVs(self):
        return self.__MNLVs

    def set_MLVs(self, dbs, b, rnds):
        globals().update(dbs.variables)
        V1 = b.CARTIME * CARTIME + b.CARCOST * CARCOST + rnds.CARPSAFE * CARPSAFE
        V2 = rnds.ASC_EBIKE + b.EBIKETIME * EBIKETIME + b.EBIKECOST * EBIKECOST + rnds.EBIKEPSAFE * EBIKEPSAFE
        V3 = rnds.ASC_ESCOOT + b.ESCOOTIME * ESCOOTIME + b.ESCOOTCOST * ESCOOTCOST + rnds.ESCOOTPSAFE * ESCOOTPSAFE
        V4 = rnds.ASC_WALK + b.WALKTIME * WALKTIME + rnds.WALKPSAFE * WALKPSAFE
        V = {4: V1, 3: V2, 2: V3, 1:V4}
        self.__MLVs = V

    def get_MLVs(self):
        return self.__MLVs
    
    def set_Bincar_RND(self, dbs, b, rnds):
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_CAR + rnds.CARTIME * CARTIME + rnds.CARCOST * CARCOST + rnds.CARPSAFE * CARPSAFE
        V = {0: V0, 1: V1}
        self.__Bincar_RND = V

    def get_Bincar_RND(self):
        return self.__Bincar_RND
    
    def set_Binebike_RND(self, dbs, b, rnds):
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_EBIKE + rnds.EBIKETIME * EBIKETIME + rnds.EBIKECOST * EBIKECOST + rnds.EBIKEPSAFE * EBIKEPSAFE
        V = {0: V0, 1: V1}
        self.__Binebike_RND = V

    def get_Binebike_RND(self):
        return self.__Binebike_RND

    def set_Binesoot_RND(self, dbs, b, rnds):
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_ESCOOT + rnds.ESCOOTIME * ESCOOTIME + rnds.ESCOOTCOST * ESCOOTCOST + rnds.ESCOOTPSAFE * ESCOOTPSAFE
        V = {0: V0, 1: V1}
        self.__Binescoot_RND = V

    def get_Binescoot_RND(self):
        return self.__Binescoot_RND
    
    def set_Binwalk_RND(self, dbs, b, rnds):
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_WALK + rnds.WALKTIME * WALKTIME + rnds.WALKPSAFE * WALKPSAFE
        V = {0: V0, 1: V1}
        self.__Binwalk_RND = V

    def get_Binwalk_RND(self):
        return self.__Binwalk_RND   
    
    def set_cho(self, dbs, exp, typ):
        globals().update(dbs.variables)
        if exp == 'mode_choice': self.__cho = dat_defin(typ, 'CHOICE',  intchoice, dbs)
        elif exp == 'car_binary': self.__cho = dat_defin(typ, 'CHOICE',  binchoice1, dbs)
        elif exp == 'ebike_binary': self.__cho = dat_defin(typ, 'CHOICE',  binchoice2, dbs)
        elif exp == 'escoot_binary': self.__cho = dat_defin(typ, 'CHOICE',  binchoice3, dbs)
        elif exp == 'walk_binary': self.__cho = dat_defin(typ, 'CHOICE',  binchoice4, dbs)
        else: self.__cho = 0
        
    def get_cho(self):
        return self.__cho
    
    def set_modecho_av(self, exp):
        if exp == 'mode_choice': av = {4:1, 3:1, 2:1, 1:1}
        elif exp == 'car_binary' or exp == 'ebike_binary' or exp == 'escoot_binary' or exp == 'walk_binary':
            av = {0:1, 1:1}
        else: av = 0
        self.__modecho_av = av
     
    def get_modecho_av(self):
        return self.__modecho_av