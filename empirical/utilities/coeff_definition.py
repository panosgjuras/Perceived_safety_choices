"""
Tools to define the unknown parameters of the model

@author: ptzouras
National Technical University of Athens
"""

from biogeme.expressions import Beta, bioDraws

class betas:    
    def __init__(self, mean, mink, maxk, st):
        self.ASC_CAR = Beta('ASC_CAR', mean, mink, maxk, st)
        self.CARTIME = Beta('BETA_CARTIME', mean, mink, maxk, st)
        self.CARCOST = Beta('BETA_CARCOST', mean, mink, maxk, st)
        self.CARPSAFE = Beta('BETA_CARPSAFE', mean, mink, maxk, st)
        self.ASC_EBIKE = Beta('ASC_EBIKE', mean, mink, maxk, st)
        self.EBIKETIME = Beta('BETA_EBIKETIME', mean, mink, maxk, st)
        self.EBIKECOST = Beta('BETA_EBIKECOST', mean, mink, maxk, st)
        self.EBIKEPSAFE = Beta('BETA_EBIKEPSAFE', mean, mink, maxk, st)
        self.ASC_ESCOOT = Beta('ASC_ESCOOT', mean, mink, maxk, st)
        self.ESCOOTIME = Beta('BETA_ESCOOTIME', mean, mink, maxk, st)
        self.ESCOOTCOST = Beta('BETA_ESCOOTCOST', mean, mink, maxk, st)
        self.ESCOOTPSAFE = Beta('BETA_ESCOOTPSAFE', mean, mink, maxk, st)
        self.ASC_WALK = Beta('ASC_WALK', mean, mink, maxk, st)
        self.WALKPSAFE = Beta('BETA_WALKPSAFE', mean, mink, maxk, st)
        self.WALKCOST = Beta('BETA_WALKTIME', mean, mink, maxk, st)
        self.WALKTIME = Beta('BETA_WALKTIME', mean, mink, maxk, st) 

class sigmas:
    def __init__(self, mean, mink, maxk, st):
        self.ASC_CAR = Beta('SIGMA_ASC_CAR', mean, mink, maxk, st)
        self.CARTIME = Beta('SIGMA_CARTIME', mean, mink, maxk, st)
        self.CARCOST = Beta('SIGMA_CARCOST', mean, mink, maxk, st)
        self. CARPSAFE = Beta('SIGMA_CARPSAFE', mean, mink, maxk, st)
        self.ASC_EBIKE = Beta('SIGMA_ASC_EBIKE', mean, mink, maxk, st)
        self.EBIKETIME = Beta('SIGMA_EBIKETIME', mean, mink, maxk, st)
        self.EBIKECOST = Beta('SIGMA_EBIKECOST', mean, mink, maxk, st)
        self.EBIKEPSAFE = Beta('SIGMA_EBIKEPSAFE', mean, mink, maxk, st)
        self.ASC_ESCOOT = Beta('SIGMA_ASC_ESCOOT', mean, mink, maxk, st)
        self.ESCOOTIME = Beta('SIGMA_ESCOOTIME', mean, mink, maxk, st)
        self.ESCOOTCOST = Beta('SIGMA_ESCOOTCOST', mean, mink, maxk, st)
        self.ESCOOTPSAFE = Beta('SIGMA_ESCOOTPSAFE',mean, mink, maxk, st)
        self.ASC_WALK = Beta('SIGMA_ASC_WALK', mean, mink, maxk, st)
        self.WALKPSAFE = Beta('SIGMA_WALKPSAFE',mean, mink, maxk, st)
        self.WALKCOST = Beta('SIGMA_WALKTIME',mean, mink, maxk, st)
        self.WALKTIME = Beta('SIGMA_WALKTIME',mean, mink, maxk, st) 

class randoms:
    def __init__(self, b, s, distr):
        self.ASC_CAR = b.ASC_CAR + s.ASC_CAR * bioDraws('ASC_CAR_RND', distr)
        self.CARTIME = b.CARTIME + s.CARTIME * bioDraws('BETA_CARTIME_RND', distr)
        self.CARCOST = b.CARCOST + s.CARCOST * bioDraws('BETA_CARCOST_RND', distr)
        self.CARPSAFE = b.CARPSAFE + s.CARPSAFE * bioDraws('BETA_CARPSAFE_RND', distr)
        self.ASC_EBIKE = b.ASC_EBIKE + s.ASC_EBIKE * bioDraws('ASC_EBIKE_RND', distr)
        self.EBIKETIME = b.EBIKETIME + s.EBIKETIME * bioDraws('BETA_EBIKETIME_RND', distr)
        self.EBIKECOST = b.EBIKECOST + s.EBIKECOST * bioDraws('BETA_EBIKECOST_RND', distr)
        self.EBIKEPSAFE = b.EBIKEPSAFE + s.EBIKEPSAFE * bioDraws('BETA_EBIKEPSAFE_RND', distr)
        self.ASC_ESCOOT = b.ASC_ESCOOT + s.ASC_ESCOOT * bioDraws('ASC_ESCOOT_RND', distr)
        self.ESCOOTIME = b.ESCOOTIME + s.ESCOOTIME * bioDraws('BETA_ESCOOTIME_RND', distr)
        self.ESCOOTCOST = b.ESCOOTCOST + s.ESCOOTCOST * bioDraws('BETA_ESCOOTCOST_RND', distr)
        self.ESCOOTPSAFE = b.ESCOOTPSAFE + s.ESCOOTPSAFE * bioDraws('BETA_ESCOOTPSAFE_RND', distr)
        self.ASC_WALK = b.ASC_WALK + s.ASC_WALK * bioDraws('ASC_WALK_RND', distr)
        self.WALKTIME = b.WALKTIME + s.WALKTIME * bioDraws('BETA_WALKTIME_RND', distr)
        self.WALKLCOST = b.WALKCOST + s.WALKCOST * bioDraws('BETA_WALKCOST_RND', distr)
        self.WALKPSAFE = b.WALKPSAFE + s.WALKPSAFE * bioDraws('BETA_WALKPSAFE_RND', distr)