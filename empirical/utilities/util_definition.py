import pandas as pd
import biogeme.database as db
from biogeme.expressions.elementary_expressions import DefineVariable

def dat_defin(NAME, expr, database):
    """
    Defines a variable in the Biogeme database.

    Args:
        NAME (str): The name of the variable.
        expr (biogeme.expressions.Expression): The mathematical expression defining the variable.
        database (biogeme.database.Database): The Biogeme database where the variable is defined.
    
    Returns: The defined variable.
    
    IMPORTANT NOTE! Check if DefineVariable expression is still valid.

    """
    var = database.DefineVariable(NAME, expr)
    return var

class database:
    """
    A class to prepare the Perceived Safety Choices database to estimate discrete choice models.

    Attributes:
        link (str): The file path or URL of the dataset.
        __dbase (biogeme.database.Database): The Biogeme database instance.
    
    Args:
        link (str): The file path of the dataset.
        sele (list): The variable that will be excluded from the database

    """
    def __init__(self, link, sele = ['scenario', 'choice']):
        self.link = link
        self.set_dbase(link)
    
    def set_dbase(self, link, sele = ['scenario', 'choice']):
        """
        Reads the dataset, processes relevant variables, and initializes the Biogeme database.
        """
        df = pd.read_csv(link,',')
        df = df.drop(columns = sele)
        
        dbs = db.Database('Perceived&choices', df.dropna())
        dbs.panel('pid')
        
        globals().update(dbs.variables)
        CARTIME = dat_defin('CARTIME', cartime, dbs)
        CARCOST = dat_defin('CARCOST', carcost, dbs)
        CARPSAFE = dat_defin('CARPSAFE',carpsafe - 4, dbs)

        EBIKETIME = dat_defin('EBIKETIME',acttime, dbs) # new time variables based on the difference among modes
        EBIKECOST = dat_defin('EBIKECOST',ebikecost, dbs)
        EBIKEPSAFE = dat_defin('EBIKEPSAFE',ebikepsafe - 4, dbs)
                 
        ESCOOTIME = dat_defin('ESCOOTIME', (20/15) * acttime, dbs) # new time variables based on the difference among modes
        ESCOOTCOST = dat_defin('ESCOOTCOST', escootcost, dbs) # new time variables based on the difference among modes
        ESCOOTPSAFE = dat_defin('ESCOOTPSAFE', escootpsafe - 4, dbs)
        
        WALKTIME = dat_defin('WALKTIME',  (20/5) * acttime, dbs) # new time variables based on the difference among modes
        WALKPSAFE = dat_defin('WALKPSAFE',walkpsafe - 4, dbs)
        
        self.__dbase = dbs
     
    def get_dbase(self):
        """
        Returns the Biogeme database instance.
        """
        return self.__dbase


class utils:
    
    """
    A class to prepare the utility functions

    Attributes:
        __MNLVs (dict): A dictionary containing the utility functions for the MNL mode choice.
        __MLVs (dict): A dictionary containing the utility functions for the ML mode choice.
        __Bincar_RND (dict): A dictionary containing the utility functions for the Binary Choice Model of CAR.
        __Binebike_RND (dict): A dictionary containing the random utility for the Binary Choice Model of E-BIKE.
        __Binescoot_RND (dict): A dictionary containing the random utility for the Binary Choice Model of E-SCOOTER.
        __Binwalk_RND (dict): A dictionary containing the random utility for the Binary Choice Model of WALK.
        __cho (biogeme.expressions.Expression): The choice variable used in the model.
        __modecho_av (dict): A dictionary indicating the availability of each alternative for the mode choice model.

    Args:
        dbs (biogeme.database.Database): The Biogeme database.
        b (object): The coefficient object that contains the parameters for the utility functions.
        rnds (object): The object containing random draws for the Mixed Logit model (default is 0).
        exp (str): The type of experiment ('mode_choice', 'car_binary', 'ebike_binary', etc.).

    Example:
        >>> utils_instance = utils(dbs, b, rnds, 'mode_choice')
        >>> mnl_utility = utils_instance.get_MNLVs()
        >>> mode_choice_availability = utils_instance.get_modecho_av()
    """
     
    def __init__(self, dbs, b, rnds = 0, exp = 'mode_choice'):        
        self.set_MNLVs(dbs, b)
        self.set_MLVs(dbs, b, rnds)
        self.set_Bincar_RND(dbs, b, rnds)
        self.set_Binebike_RND(dbs, b, rnds)
        self.set_Binesoot_RND(dbs, b, rnds)
        self.set_Binwalk_RND(dbs, b, rnds)
        self.set_modecho_av(exp)
        self.set_cho(dbs, exp)

    def set_MNLVs(self, dbs, b):
        """
        Defines the utility functions for the MNL mode choice.
        """
        globals().update(dbs.variables)
        V1 = b.CARTIME * CARTIME + b.CARCOST * CARCOST + b.CARPSAFE * CARPSAFE
        V2 = b.ASC_EBIKE + b.EBIKETIME * EBIKETIME + b.EBIKECOST * EBIKECOST + b.EBIKEPSAFE * EBIKEPSAFE
        V3 = b.ASC_ESCOOT + b.ESCOOTIME * ESCOOTIME + b.ESCOOTCOST * ESCOOTCOST + b.ESCOOTPSAFE * ESCOOTPSAFE
        V4 = b.ASC_WALK + b.WALKTIME * WALKTIME + b.WALKPSAFE * WALKPSAFE
        V = {4: V1, 3: V2, 2: V3, 1:V4}
        self.__MNLVs = V
    
    def get_MNLVs(self):
        """
        Returns the MNL mode choice utility functions.
        """
        return self.__MNLVs

    def set_MLVs(self, dbs, b, rnds):
        """
        Defines the utility functions for the ML mode choice.
        """  
        globals().update(dbs.variables)
        V1 = b.CARTIME * CARTIME + b.CARCOST * CARCOST + rnds.CARPSAFE * CARPSAFE
        V2 = rnds.ASC_EBIKE + b.EBIKETIME * EBIKETIME + b.EBIKECOST * EBIKECOST + rnds.EBIKEPSAFE * EBIKEPSAFE
        V3 = rnds.ASC_ESCOOT + b.ESCOOTIME * ESCOOTIME + b.ESCOOTCOST * ESCOOTCOST + rnds.ESCOOTPSAFE * ESCOOTPSAFE
        V4 = rnds.ASC_WALK + b.WALKTIME * WALKTIME + rnds.WALKPSAFE * WALKPSAFE
        V = {4: V1, 3: V2, 2: V3, 1:V4}
        self.__MLVs = V

    def get_MLVs(self):
        """
        Returns the ML mode choice utility functions.
        """
        return self.__MLVs
    
    def set_Bincar_RND(self, dbs, b, rnds):
        """
        Defines the utility functions for the CAR Binary Choice Model.
        """
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_CAR + rnds.CARTIME * CARTIME + rnds.CARCOST * CARCOST + rnds.CARPSAFE * CARPSAFE
        V = {0: V0, 1: V1}
        self.__Bincar_RND = V

    def get_Bincar_RND(self):
        """
        Returns the CAR Binary Choice Model utility functions.
        """
        return self.__Bincar_RND
    
    def set_Binebike_RND(self, dbs, b, rnds):
        """
        Defines the utility functions for the E-BIKE Binary Choice Model.
        """
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_EBIKE + rnds.EBIKETIME * EBIKETIME + rnds.EBIKECOST * EBIKECOST + rnds.EBIKEPSAFE * EBIKEPSAFE
        V = {0: V0, 1: V1}
        self.__Binebike_RND = V

    def get_Binebike_RND(self):
        """
        Returns the E-BIKE Binary Choice Model utility functions.
        """
        return self.__Binebike_RND

    def set_Binesoot_RND(self, dbs, b, rnds):
        """
        Defines the utility functions for the E-SCOOTER Binary Choice Model.
        """
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_ESCOOT + rnds.ESCOOTIME * ESCOOTIME + rnds.ESCOOTCOST * ESCOOTCOST + rnds.ESCOOTPSAFE * ESCOOTPSAFE
        V = {0: V0, 1: V1}
        self.__Binescoot_RND = V

    def get_Binescoot_RND(self):
        """
        Returns the E-SCOOTER Binary Choice Model utility functions.
        """
        return self.__Binescoot_RND
    
    def set_Binwalk_RND(self, dbs, b, rnds):
        """
        Defines the utility functions for the WALK Binary Choice Model.
        """
        globals().update(dbs.variables)
        V0 = 0
        V1 = b.ASC_WALK + rnds.WALKTIME * WALKTIME + rnds.WALKPSAFE * WALKPSAFE
        V = {0: V0, 1: V1}
        self.__Binwalk_RND = V

    def get_Binwalk_RND(self):
        """
        Returns the WALK Binary Choice Model utility functions.
        """
        return self.__Binwalk_RND   
    
    def set_cho(self, dbs, exp):
        """
        Defines the choice variable for the model based on the specified type of model.
        """
        globals().update(dbs.variables)
        if exp == 'mode_choice': self.__cho = dat_defin('CHOICE',  intchoice, dbs)
        elif exp == 'car_binary': self.__cho = dat_defin('CHOICE',  binchoice1, dbs)
        elif exp == 'ebike_binary': self.__cho = dat_defin('CHOICE',  binchoice2, dbs)
        elif exp == 'escoot_binary': self.__cho = dat_defin('CHOICE',  binchoice3, dbs)
        elif exp == 'walk_binary': self.__cho = dat_defin('CHOICE',  binchoice4, dbs)
        else: self.__cho = 0
        
    def get_cho(self):
        """
        Returns the choice variable.
        """
        return self.__cho
    
    def set_modecho_av(self, exp):
        """
        Defines the availability of each alternative for the mode choice model.
        """
        if exp == 'mode_choice': av = {4:1, 3:1, 2:1, 1:1}
        elif exp == 'car_binary' or exp == 'ebike_binary' or exp == 'escoot_binary' or exp == 'walk_binary':
            av = {0:1, 1:1}
        else: av = 0
        self.__modecho_av = av
     
    def get_modecho_av(self):
        """
        Returns the availability of each alternative for the mode choice model.
        """
        return self.__modecho_av