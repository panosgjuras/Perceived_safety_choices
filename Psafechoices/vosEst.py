"""
Tools to play with the Value of Safety based on a default choice model

@author: ptzouras
National Technical University of Athens
"""

def mode_params(df, mode):
    """
    This function downloads the beta parameters of time, cost and safety

    Parameters
    ----------
    df : DataFrame
       the output of the choice model in df format
    mode : str
        the transport mode for which the data will be downloaded

    Returns
    -------
    btime : float
        the beta parameter of time in utilis/min
    bcost : float
       the beta parameter of cost in utils/euro
    bsafe : float
        the beta parameter of safety in utils/level
    """
    
    df = df.set_index('Unnamed: 0')

    if mode == 'car':
        btime = df.loc["BETA_CARTIME", "Value"]
        bcost = df.loc["BETA_CARCOST", "Value"]
        bsafe = df.loc["BETA_CARPSAFE", "Value"]
    elif mode == 'ebike':
        btime = df.loc["BETA_EBIKETIME", "Value"]
        bcost = df.loc["BETA_EBIKECOST", "Value"]
        bsafe = df.loc["BETA_EBIKEPSAFE", "Value"]
    elif mode == 'escooter':
        btime = df.loc["BETA_ESCOOTIME", "Value"]
        bcost = df.loc["BETA_ESCOOTCOST", "Value"]
        bsafe = df.loc["BETA_ESCOOTPSAFE", "Value"]
    elif mode == 'walk':
        btime = df.loc["BETA_WALKTIME", "Value"]
        bcost = 0
        bsafe = df.loc["BETA_WALKPSAFE", "Value"]
    # print('Beta of travel time:', btime)
    return btime, bcost, bsafe

def vosEstFun(df, mode, speed, dcost):
    """
    It estimates the value of time, the value of safe time and the value of safe distance
    

    Parameters
    ----------
    df : DataFrame
       the output of the choice model in df format
    mode : str
        the transport mode for which the data will be downloaded
    speed : float
        the mean travel speed of the transport mode in km/h
    dcost : float
        the mean cost per km of the transport mode in euros/km

    Returns
    -------
    vos : float
        The value of safe distance in km/level
    """
    
    btime = mode_params(df, mode)[0]
    bcost = mode_params(df, mode)[1]
    bsafe = mode_params(df, mode)[2]
    
    bdist = (btime/speed) + bcost * dcost
    vos = bsafe / bdist
    print('The value of safety of', mode, ' is: ', vos, 'km/level')
    return vos
