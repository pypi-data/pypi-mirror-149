#!/usr/bin/env python

import os
import time
import numpy as np
from datetime import datetime
import dill as pickle
from dlnpyutils import utils as dln
from astropy.table import Table
from astropy.io import fits
import dill as pickle
from . import utils,fitter
from .cube import Cube

def initialize_tracking(wander,yr):
    """ Initialize the tracking structures."""

    global BTRACK, GSTRUC

    # How many steps are we tracking
    ntrack = 0
    if wander==False:
        ntrack = yr[1]*3
        n = ntrack
    else:
        ntrack = 0
        n = 100000
    
    # Tracking lists
    BTRACK = {'data':[],'count':0,'wander':wander,'ntrack':ntrack,'x':np.zeros(n,int)-1,'y':np.zeros(n,int)-1}
    GSTRUC = {'data':[],'count':0,'ngauss':0,'x':np.zeros(n,int)-1,'y':np.zeros(n,int)-1}

    
def gstruc_add(tstr):
    """ Add to the GSTRUC tracking structure."""

    # data:   large list of data, one element per position (with padding)
    # count:  the number of elements in DATA we're using currently, also
    #           the index of the next one to start with.
    # x/y:    the x/y position for the gaussians

    global BTRACK, GSTRUC, NPIX

    if type(tstr) is list:
        print('list input')
        import pdb; pdb.set_trace()
    
    # Add new elements
    if len(tstr)+GSTRUC['count'] > len(GSTRUC['x']):
        print('Adding more elements to GSTRUC')
        for n in ['x','y']:
            GSTRUC[n] = np.hstack((GSTRUC[n],np.zeros(100000,int)-1))
    # Stuff in the new data
    count = GSTRUC['count']
    GSTRUC['data'].append(tstr)
    GSTRUC['x'][count] = tstr['x']
    GSTRUC['y'][count] = tstr['y']
    GSTRUC['ngauss'] += len(tstr['par'])//3
    GSTRUC['count'] += 1
        
    if type(GSTRUC['data'][-1]) is list:
        print('problem')
        import pdb; pdb.set_trace()

    
def gstruc_replace(tstr):
    """ Replace an old decomposition with a newer and better one."""
    # Double-check that the positions match
    ind, = np.where((GSTRUC['x']==tstr['x']) & (GSTRUC['y']==tstr['y']))
    if len(ind)==0:
        print('No position for (%d,%d) found in GSTRUC. Adding instead.' % (tstr['x'],tstr['y']))
        gstruc_add(tstr)
        return
    ind = ind[0]
    old_ngauss = len(GSTRUC['data'][ind]['par'])//3
    new_ngauss = len(tstr['par'])//3
    GSTRUC['data'][ind] = tstr
    GSTRUC['ngauss'] += new_ngauss - old_ngauss
    
def btrack_add(track):
    """ Add to the BTRACK tracking structure."""

    # data:   large list of data, one element per position (with padding)
    # count:  the number of elements in DATA we're using currently, also
    #           the index of the next one to start with.
    # x/y:    the x/y position for the gaussians

    global BTRACK, GSTRUC, NPIX
    
    # Wander
    if BTRACK['wander']:
        # Add new elements        
        if BTRACK['count']+1 > len(BTRACK['x']):
            print('Adding more elements to BTRACK')
            for n in ['x','y']:
                BTRACK[n] = np.hstack((BTRACK[n],np.zeros(100000,int)-1))
        # Stuff in the new data
        count = BTRACK['count']
        BTRACK['data'] += [track]
        BTRACK['x'][count] = track['x']
        BTRACK['y'][count] = track['y']
    # No wander
    else:
        # Stuff in the new data
        count = BTRACK['count']
        # shift all data/x/y value back by one
        if BTRACK['count'] >= BTRACK['ntrack']:
            del BTRACK['data'][0]
            BTRACK['x'][0:-1] = BTRACK['x'][1:]
            BTRACK['x'][-1] = -1
            BTRACK['y'][0:-1] = BTRACK['y'][1:]
            BTRACK['y'][-1] = -1
            # Now add the new values at the end
            BTRACK['data'] += [track]
            BTRACK['x'][-1] = track['x']
            BTRACK['y'][-1] = track['y']
        else:
            # Now add the new values
            BTRACK['data'] += [track]            
            BTRACK['x'][count] = track['x']
            BTRACK['y'][count] = track['y']

    BTRACK['count'] += 1
    
    
def gincrement(x,y,xr,yr,xsgn=1,ysgn=1,nstep=1,p2=False):
    """
    This program increments the position 
     
    Parameters
    ----------
    x : int
      X of current position 
    y : int
      Y of current position 
    xr : list/array
      Two element array of x limits.
    yr  : list/array
      Two element array of y limits.
    xsgn : int, optional
      Sign of x increment.  Default is 1.
    ysgn : int, optional
      Sign of y increment, Default is 1.
    nstep : int, optional
      Number of steps to increment.  Default is 1.
    p2 : boolean, optional
      Increment in y rather than in x. Default is False.
     
    Returns
    -------
    newx : int,
      X of new position 
    newy : int
      Y of new position 
     
    When this program has problems it returns: 
    newx = None
    newy = None
     
    Created by David Nidever April 2005 
    Translated to python by D. Nidever, March 2022
    """
 
    step = 1
     
    # Bad until proven okay 
    newx = None
    newy = None
     
    # X and y limits 
    x0 = xr[0]
    x1 = xr[1] 
    y0 = yr[0] 
    y1 = yr[1] 
        
    # Are we in the box? 
    if (x < x0) or (x > x1) or (y < y0) or (y > y1):
        return None,None

    # Wrong signs 
    if np.abs(xsgn) != 1: 
        return None,None
    if np.abs(ysgn) != 1:
        return None,None        
     
    # figuring out the case 
    #bit = ((ysgn+1.)*0.5) + 2.*((xsgn+1.)*0.5) 
    #bit = int(bit) 
    # 
    # bit (x,y) 
    # 0 - (-1,-1) 
    # 1 - (-1,+1) 
    # 2 - (+1,-1) 
    # 3 - (+1,+1) 

    tx = x
    ty = y
     
    # Looping through all the steps 
    for i in range(nstep): 
        
        # p2, incrementing vertically 
        if p2:
            # UP, at the end 
            if (ysgn == 1) and (ty == y1):
                return None,None
            # DOWN, at the end 
            if (ysgn == -1) and (ty == y0): 
                return None,None
            # Not at end, normal increment 
            newx = tx 
            newy = ty + ysgn * step 
            
        # Incrementing Sideways 
        else: 
            # RIGHT, xsgn = +1 
            if (xsgn == 1): 
                # UP, the very end 
                if (ysgn == 1) and (tx == x1) and (ty == y1): 
                    return None,None
                # DOWN, the very end 
                if (ysgn == -1) and (tx == x1) and (ty == y0): 
                    return None,None
                # At end of x, increment y 
                if (tx == x1): 
                    newx = x0 
                    newy = ty + ysgn * step 
                # Normal increment 
                if (tx != x1): 
                    newx = tx + xsgn * step 
                    newy = ty 
         
            # LEFT, xsgn = -1 
            if (xsgn == -1): 
                # UP, the very end 
                if (ysgn == 1) and (tx == x0) and (ty == y1): 
                    return None,None
                # DOWN, the very end 
                if (ysgn == -1) and (tx == x0) and (ty == y0): 
                    return None,None
                # At end of x, increment y 
                if (tx == x0): 
                    newx = x1 
                    newy = ty + ysgn * step 
                # Normal increment 
                if (tx != x0): 
                    newx = tx + xsgn * step 
                    newy = ty 
     
        # In case we're looping 
        tx = newx 
        ty = newy 
     
    # Final answer 
    newx = tx 
    newy = ty 

    return newx,newy


def gredo(x,y,guessx,guessy,guesspar):
    """
    This function checks wether we can redo this location again.
    The "redo" is denied if the new guess is essentially the same
    as a previous guess.
    
    Parameters
    ----------
    x : int
      X of current position 
    y : int
      Y of current position 
    guessx : int
      X of guess position 
    guessy : int
      Y of guess position 
    guesspar : list/array
      Guess parameters 
     
    Returns
    -------
    flag : boolean,
      Is this redo okay.
        True - Redo okay. This guess has not been done before 
        False - Redo NOT okay. This guess has been done before 
     
    When there are any problems in this program it returns: 
    flag = -1 
     
    Created by David Nidever April 2005 
    Translated to python by D. Nidever, March 2022
    """

    global BTRACK, GSTRUC, NPIX
    
    flag = True  # do it unless proven wrong 
     
    # FROM **ANY** PREVIOUS POSITION 
    prev, = np.where((BTRACK['x']==x) & (BTRACK['y']==y))
    nprev = len(prev)

    if guesspar is None:
        return False
    tguesspar = guesspar
    nguesspar = len(tguesspar) 
    ngg = nguesspar//3 
     
    # FROM **ANY** PREVIOUS POSITION 
    # We have used a guess from this position before 
    #  but have the parameters changed sufficiently
    nogaussians = True  # no gaussians found by default
    if (nprev > 0): 
         
        # Looping through the previous ones 
        for i in range(nprev):
            guesspar2 = BTRACK['data'][prev[i]]['guesspar']
         
            # Some gaussians found 
            if (guesspar2 is not None):
                nogaussians = False
                tpar = guesspar2
                ntpar = len(tpar) 
                ntg = ntpar//3      # number of gaussians in this guess 
             
                # Same number of gaussians 
                if (ntpar == nguesspar): 
                    # Sorting, largest first 
                    tpar2 = utils.gsort(tpar) 
                    tguesspar2 = utils.gsort(tguesspar) 
                    
                    # Fixing possible zeros that could ruin the ratio 
                    dum = np.copy(tpar2)
                    bd, = np.where(dum == 0.) 
                    if len(bd) > 0:
                        dum[bd] = 1e-5 
                    diff = np.abs(tpar2 - tguesspar2) 
                    ratio = diff/np.abs(dum) 
                 
                    # These differences are too small, NO redo 
                    if (np.max(ratio) < 0.01): 
                        return False
                    
        # Some previous visits, but no Gaussians detected, redo=False
        if nogaussians:
            return False
                    
    return flag 

def gbetter(res1,res2):
    """
    This function tries to figure out if one gaussian 
    analysis is better than another. 
     
    Parameters
    ----------
    res1 : dict
      Results from position 1 with par, rms, noise.
    res2 : dict
      Results from position 2 with par, rms, noise.
     
    Returns
    -------
    better : int
       The function value is either: 
         1 - Second position better than the first 
         0 - First position better than the second 
        -1 - Any problems 
    dbic : float
       Difference of Bayesian Information Criterion (BIC)
         between the two solutions (BIC1-BIC2).
         Lower BIC is better.
         dbic < 0    Solution 1 is better.
         dbic == 0   Solutions are equally good.
         dbic > 0    Solution 2 is better.
     
    If the first one is better then it returns 0 
    and if the second one is better it returns 1 
     
    When this program has any problems is return: 
      better = -1 
     
    Created by David Nidever April 2005 
    Translated to python by D. Nidever, March 2022
    """
 
    better = -1   # default unless proven wrong 
    dbic = 0      # same to start with
        
    rms1,noise1,par1 = res1.get('rms'),res1.get('noise'),res1.get('par')
    rms2,noise2,par2 = res2.get('rms'),res2.get('noise'),res2.get('par')
    
    # Calculate Bayesian Information Criterion (BIC)
    # lower BICs are better
    bic1 = utils.bayesinfocrit(res1)
    bic2 = utils.bayesinfocrit(res2)
    dbic = bic1-bic2

    # Solution 1 is better
    if dbic <= 0:
        better = 0
    # Solution 2 is better
    if dbic > 0 :
        better = 1

    return better,dbic

    # ---------- OLD CODE, NOT USED ANYMORE ----------
        
    # In case either one is -1 (bad)
    if par1 is not None and par2 is not None:
        if (rms1 == -1) and (rms2 != -1): 
            better = 1
        if (rms1 != -1) and (rms2 == -1): 
            better = 0 
        if (rms1 == -1) and (rms2 == -1): 
            better = -1 
        if (rms1 == -1) or (rms2 == -1): 
            return better,dbic
        if (len(par1) < 3) and (len(par2) >= 3): 
            better = 1 
        if (len(par2) < 3) and (len(par1) >= 3): 
            better = 0 
        if (len(par1) < 3) or (len(par2) < 3): 
            return better,dbic

    # One is bad, second is better
    if par1 is None:
        return -1,dbic
    
    # Two is bad, first is better    
    if par2 is None:
        return -1,dbic
    
    drms1 = rms1-noise1 
    drms2 = rms2-noise2 
    n1 = len(par1)/3 
    n2 = len(par2)/3 
        
    # Clear cut, rms better, n equal or less 
    if (drms1 < drms2) and (n1 <= n2): 
        better = 0 
    if (drms1 > drms2) and (n1 >= n2): 
        better = 1 
     
    # RMS same, N different 
    if (drms1 == drms2) and (n1 <= n2): 
        better = 0 
    if (drms1 == drms2) and (n1 > n2): 
        better = 1 
     
    # Mixed bag, lower RMS but higher N
    if (drms1 < drms2) and (n1 > n2): 
        ddrms = drms2-drms1 
        rdrms = ddrms/drms2   # ratio compared to worse one 
        dn = n1-n2 
         
        better = 1    # default 
        if (dn == 1) and (rdrms > 0.2) : 
            better = 0 
        if (dn == 2) and (rdrms > 0.5) : 
            better = 0 
        if (dn == 3) and (rdrms > 1.0) : 
            better = 0 
        if (dn >= 4) and (rdrms > 2.0) : 
            better = 0 
     
    if (drms2 < drms1) and (n2 > n1): 
        ddrms = drms1-drms2 
        rdrms = ddrms/drms1    # ratio compared to worse one 
        dn = n2-n1 
         
        better = 0   # default 
        if (dn == 1) and (rdrms > 0.2) : 
            better = 1 
        if (dn == 2) and (rdrms > 0.5) : 
            better = 1 
        if (dn == 3) and (rdrms > 1.0) : 
            better = 1 
        if (dn >= 4) and (rdrms > 2.0) : 
            better = 1 
     
    return better,dbic


def gfind(x,y,xr=None,yr=None):
    """
    This function helps find a y and x in 
    the gaussian components structure. 
     
    Parameters
    ----------
    x : int
      X to search for.
    y : int
      Y to search for.
    xr : list/array, optional
      Two element array of x limits, xr=[xmin,xmax].
    yr : list/array, optional
      Two element array of y limits, yr=[ymin,ymax].
     
    Returns
    -------
    flag : 
      The function value is either 0 or 1: 
         1 - the position exists in the structure 
         0 - the position does NOT exist in the structure 
        -1 - any problems 
    results : dict
      Dictionary of resuts with pind, rms, noise, par.
        pind    Index of position in GSTRUC. 
        rms     RMS of gaussian fit at the desired position 
        noise   Noise level at desired position 
        par     Parameters of gaussians in GSTRUC with the desired position 
     
    When there are any problems in this program it returns: 
     flag = None
     rms = None
     noise = None 
     par = None
     pind = None
     
    Created by David Nidever April 2005 
    Translated to python by D. Nidever, March 2022
    """

    global BTRACK, GSTRUC, NPIX
    
    # Assume bad until proven otherwise 
    flag,rms,noise,par,pind = None,None,None,None,None
    results = {'x':x,'y':y,'pind':pind,'rms':rms,'noise':noise,'par':par,'visited':None,'npix':None}  # initial bad values

    if x is None or y is None:
        results['visited'] = 0
        return 0,results
    
    # Setting the ranges
    if xr is not None:
        x0 = xr[0] 
        x1 = xr[1] 
    else: 
        x0 = 0 
        x1 = 1000
    if yr is not None:
        y0 = yr[0] 
        y1 = yr[1] 
    else: 
        y0 = 0
        y1 = 1000
     
    if (x < x0) or (x > x1) or (y < y0) or (y > y1): 
        flag = 0
        results['visited'] = 0
        return flag,results
     
    # No GSTRUC yet, first position
    try:
        dum = len(GSTRUC)
    except:
        return 0,results
    
    # Looking for the position 
    t0 = time.time() 
    # Check GSTRUC
    pind, = np.where((GSTRUC['x']==x) & (GSTRUC['y']==y))
    # Check if it was visited before but no good spectrum/solution
    if len(pind)==0:
        bind, = np.where((BTRACK['x']==x) & (BTRACK['y']==y))
        # Found it
        if len(bind)>0:
            return 1,{'x':x,'y':y,'pind':None,'rms':np.inf,'noise':None,'par':None,'visited':1,'npix':None}
    
    # Found something, getting the values 
    if len(pind) > 0:
        tstr = GSTRUC['data'][pind[0]]
        rms = tstr['rms']
        noise = tstr['noise']
        par = tstr['par']
        npix = tstr['npix']
        flag = 1 
            
    # Nothing found 
    else:
        pind,rms,noise,par,npix = None,None,None,None,None
        flag = 0 
        
    results = {'x':x,'y':y,'pind':pind,'rms':rms,'noise':noise,'par':par,'visited':flag,'npix':npix}
    return flag,results


def gguess(x,y,xr,yr,xsgn,ysgn):
    """
    This program finds the best guess for the new profile 
    The one from the backwards positions. 
    If it can't find one then it returns 999999.'s 
     
    Parameters
    ----------
    x : int
      X of current position 
    y : int
      Y of current position 
    xr : list
      Two element array of x limits 
    yr : list
      Two element array of y limits 
    xsgn : int
      Sign of x increment 
    ysgn : int
      Sign of y increment 

     
    Returns
    -------
    guesspar : numpy array
      The first guess gaussian parameters 
    guessx : int
      The x of the position where the 
        guess parameters came from 
    guessy : ijnt
      The y of the position where the 
        guess parameters came from 
     
    When this program has problems it returns: 
      guesspar = None
      guessx = None 
      guessy = None
     
    Created by David Nidever April 2005 
    Translated to python by D. Nidever, March 2022
    """
     
    # Bad until proven okay 
    guesspar = None
    guessx = None 
    guessy = None
     
    # Making sure it's the right structure 
    #tags = tag_names(*(!gstruc.data)) 
    #if (len(tags) != 6) : 
    #    return guesspar,guessx,guessy 
    #comp = (tags == ['X','Y','RMS','NOISE','PAR','SIGPAR']) 
    #if ((where(comp != 1))(0) != -1) :
    #    return guesspar,guessx,guessy         
     
    # Saving the originals 
    orig_x = x 
    orig_y = y 

    if xr is None:
        xr = [0,2000]
    if yr is None:
        yr = [0,2000] 
     
    # Is the x range continuous??
    # Assume not continuous in general
    cont = 0 
    
    # getting the p3 and p4 positions 
    # P3 back in x (l-0.5), same y 
    # P4 back in y (b-0.5), same x 
    x3,y3 = gincrement(x,y,xr,yr,xsgn=-xsgn,ysgn=-ysgn)
    x4,y4 = gincrement(x,y,xr,yr,xsgn=xsgn,ysgn=-ysgn,p2=True)
     
    # CHECKING OUT THE EDGES 
    # AT THE LEFT EDGE, and continuous, Moving RIGHT, use neighbor on other side 
    # Use it for the guess, but never move to it directly 
    if (x == xr[0]) and (xsgn == 1) and (cont == 1): 
        y3 = y 
        x3 = xr[1] 
     
    # AT THE RIGHT EDGE, and continuous, Moving LEFT 
    if (x == xr[1]) and (xsgn == -1) and (cont == 1): 
        y3 = y 
        x3 = xr[0] 
     
    # At the edge, NOT continuous, Moving RIGHT, NO P3 NEIGHBOR 
    if (x == xr[0]) and (xsgn == 1) and (cont == 0): 
        x3 = None 
        y3 = None 
     
    # At the edge, NOT continuous, Moving LEFT, NO P3 NEIGHBOR 
    if (x == xr[1]) and (xsgn == -1) and (cont == 0): 
        x3 = None
        y3 = None
     
    # Have they been visited before? 
    p3,res3 = gfind(x3,y3)
    p4,res4 = gfind(x4,y4)
     
    # Comparing the solutions 
    b34,dbic34 = gbetter(res3,res4)
     
    # selecting the best guess 
    if (dbic34<0): # using P3 
        guesspar = res3['par']
        guessx = x3
        guessy = y3 
    if (dbic34>=0): # using P4 
        guesspar = res4['par']
        guessx = x4 
        guessy = y4 
    if np.isfinite(dbic34)==False:
        guesspar = None
        guessx = None 
        guessy = None
     
    # Putting the originals back 
    x = orig_x 
    y = orig_y 

    return guesspar,guessx,guessy  


def nextmove(x,y,xr,yr,count,xsgn=1,ysgn=1,redo=False,redo_fail=False,back=False,
             noback=False,backret=True,wander=True,silent=False):
    """
    Figure out the next move, the next position to decompose.

    Parameters
    ----------
    x : int
      X of current position 
    y : int
      Y of current position 
    xr : list/array
      Two element array of x limits.
    yr  : list/array
      Two element array of y limits.
    count : int
      The current iteration count.
    xsgn : int, optional
      Sign of x increment.  Default is 1.
    ysgn : int, optional
      Sign of y increment, Default is 1.
    redo : boolean, optional
      Was the current position a "redo"?  Default is False.
    redo_fail : boolean, optional
      If the current position was a "redo", was the redo successful
        (better than the previous attempt)?  Default is False.
    back : boolean, optional
      Was the current position a "backwards" step?  Default is False.
    noback : boolean, optional
      The program is not allowed to go backwards.  Default is False.
    backret : boolean, optional
      Any backwards motion must return to the position it 
         came from.  Default is True.
    wander : boolean, optional
      Allow backwards motion. Haud's algorithm.  Default is False.
    silent : boolean, optional
      Do not print anything to the screen.  Default is False.

    Returns
    -------
    newx : int
      X of new position 
    newy : int
      Y of new position 
    guessx : int
      X position for guess parameters.
    guessy : int
      X position for guess parameters.
    guesspar : list/array
      Guess parameter array.
    back : boolean
      Are we going backwards or not.
    redo : boolean
      New position is a redo.
    skip : boolean
      Skip the next position.
    endflag : boolean
      Whether to end of now.

    Example
    -------

    newx,newy,guessx,guessy,guesspar,redo,skip,endflag = nextmove(x,y,xr,yr,count,redo=redo,redo_fail=redo_fail,back=back)

    """

    global BTRACK, GSTRUC, NPIX

    endflag = False
    

    # This is the very end 
    if (x==xr[1] and y==yr[1]):
        endflag = True
        return None,None,None,None,None,False,False,endflag
    

    # If back, redo and BACKRET=1 then return to pre-redo position
    #=============================================================
    # This is done separately from the normal algorithm 
    if backret and back and redo: 
        back = False
        lastcount = BTRACK['count']
        newx = BTRACK['data'][-1]['lastx']
        newy = BTRACK['data'][-1]['lasty']
        lastx = BTRACK['data'][-1]['x']
        lasty = BTRACK['data'][-1]['y']
        par0 = BTRACK['data'][-1]['par']  # parameters from the current position

        # p0 is the redo position, p5 is the pre-redo position 
        p0,res0 = gfind(lastx,lasty,xr=xr,yr=yr)
        p5,res5 = gfind(newx,newy,xr=xr,yr=yr)

        b,dbic = gbetter(res0,res5)
        redo = gredo(newx,newy,lastx,lasty,par0) 

        # back position better, redo pre-redo position 
        if (dbic<0) and redo: 
            # Getting the guess
            guesspar,guessx,guessy = gguess(x,y,xr,yr,xsgn,ysgn)
            redo = True
            skip = False
        # back position worse, or can't redo pre-position, skip 
        else:
            redo = False
            skip = True
            guesspar,guessx,guessy = None,None,None
            
        return newx,newy,guessx,guessy,guesspar,back,redo,skip,endflag


    # Redo Failed! Return to original position
    #   If we went back and backret=1 then return to pre-redo position
    #   if we went forward then don't do anything, should continue forward 
    if redo and redo_fail and back: 
        # Go back to pre-redo position and skip
        newx = BTRACK[-1]['data']['lastx']
        newy = BTRACK[-1]['data']['lasty']
        skip = True
        return newx,newy,None,None,None,False,False,skip,endflag
    

    # Some default values
    skip = False
    newx,newy = None,None
    guesspar,guessx,guessy = None,None,None

    
    # Positions
    #
    # ^ Y    P2     
    # |   P3 P0 P1
    # |      P4
    #   --------> X
    
    # Get the positions, THIS IS THE PROPER WAY TO DO IT!!!!! 
    x1,y1 = gincrement(x,y,xr,yr,xsgn=xsgn,ysgn=ysgn)
    x2,y2 = gincrement(x,y,xr,yr,xsgn=xsgn,ysgn=ysgn,p2=True) 
    x3,y3 = gincrement(x,y,xr,yr,xsgn=-xsgn,ysgn=-ysgn)
    x4,y4 = gincrement(x,y,xr,yr,xsgn=xsgn,ysgn=-ysgn,p2=True)

    # Have they been visited before?
    # ps are 0 or 1
    p0,res0 = gfind(x,y,xr=xr,yr=yr)
    par0 = res0['par']
    p1,res1 = gfind(x1,y1,xr=xr,yr=yr)
    p2,res2 = gfind(x2,y2,xr=xr,yr=yr)
    p3,res3 = gfind(x3,y3,xr=xr,yr=yr)
    p4,res4 = gfind(x4,y4,xr=xr,yr=yr)

    # Comparing the solutions at neighboring positions
    # bs are 0, 1 or -1
    b1,dbic1 = gbetter(res0,res1)
    res1['better'] = b1
    res1['dbic'] = dbic1
    b2,dbic2 = gbetter(res0,res2)
    res2['better'] = b2
    res2['dbic'] = dbic2
    b3,dbic3 = gbetter(res0,res3)
    res3['better'] = b3
    res3['dbic'] = dbic3
    b4,dbic4 = gbetter(res0,res4)
    res4['better'] = b4
    res4['dbic'] = dbic4    
    
    # Do we need to redo?
    red1,red2,red3,red4 = False,False,False,False
    if (p1==1) and (b1==0): 
        red1 = True
    if (p2==1) and (b2==0): 
        red2 = True
    if (p3==1) and (b3==0): 
        red3 = True
    if (p4==1) and (b4==0): 
        red4 = True

    xx = [x1,x2,x3,x4]
    yy = [y1,y2,y3,y4]
    pp = [p1,p2,p3,p4]
    bb = [b1,b2,b3,b4]
    rr = [red1,red2,red3,red4]
    
    # Printing out the info
    if silent==False:
        if count>0:
            print(' ')
        print('Count = %d' % count)
        print('Last/Current Position = (%d,%d)' %(x,y))
        print('Neighbors (position)  visited  better  redo')
        for i in range(4):
            if xx[i] is not None:
                strx = '%5d' % xx[i]
            else:
                strx = '-----'
            if yy[i] is not None:
                stry = '%5d' % yy[i]
            else:
                stry = '-----'            
            print('P%1d (%5s,%5s)  %7d  %7d  %7s' % (i+1,strx,stry,pp[i],bb[i],str(rr[i])))    
        print('')

        
    # If P3 or P4 worse than P0 then move back to worst decomp 
    # If P3 and P4 better than P0 then move forward,
    #   -if both have been visited before then do the worst decomp 
    #   -if neither has been visited before then move to P1. 

    

    # Starting Normal Algorithm
    #  (not redo+back+backred)
    #==========================

    # More generic algorithm, checks all 4 positions and possible redos
    newscheme = True
    if noback==False and newscheme:
        endflag = False
        res1['redo'] = False
        if res1['visited']==True:
            res1['redo'] = gredo(res1['x'],res1['y'],x,y,par0)
        res2['redo'] = False
        if res2['visited']==True:
            res2['redo'] = gredo(res2['x'],res2['y'],x,y,par0)    
        res3['redo'] = False
        if res3['visited']==True:
            res3['redo'] = gredo(res3['x'],res3['y'],x,y,par0)    
        res4['redo'] = False
        if res4['visited']==True:
            res4['redo'] = gredo(res4['x'],res4['y'],x,y,par0)
        res = [res1,res2,res3,res4]
        redos = [res1['redo'],res2['redo'],res3['redo'],res4['redo']]
        dbic = np.array([res1['dbic'],res2['dbic'],res3['dbic'],res4['dbic']])
        toredo, = np.where((np.array(redos)==True) & (dbic<0))
        # Some redos
        if len(toredo)>0:
            # Find the one with the worst solution
            if len(toredo)>1:
                best1 = np.argmin(dbic[toredo])
                best = toredo[best1]
            else:
                best = toredo[0]
            if best>=2:
                back = True
            else:
                back = False
            newres = res[best]
            newx,newy = newres['x'],newres['y']
            guessx,guessy,guesspar = x,y,par0
            redo = True
        # No redos, more foward to P1
        else:
            redo = False
            back = False
            newx,newy = x1,y1
            guessx,guessy,guesspar = x,y,par0
            # if we already visited P1, then skip
            if res1['visited']:
                skip = True
            else:
                skip = False
            
        return newx,newy,guessx,guessy,guesspar,back,redo,skip,endflag
            
        # check if the position is a "valid" one
        # check if it was previously visited
        # check if it CAN be redone
        # for all that can be redone, which one has the largest negative dbic (worse solution)
        
            

    #==============================                    
    #---- CHECKING BACKWARDS ----
    #==============================                
    if ((p3==1) or (p4==1)) and (noback==False): 

        # Only P3 visited before
        #=======================
        if (p3==1) and (p4==0): 
            # Can this position be redone
            redo = gredo(x3,y3,x,y,par0)
            # P3 worse than P0, moving back
            #------------------------------
            if (b3==0) and redo: 
                newx,newy = x3,y3
                back = True   # moving backwards
                guessx,guessy,guesspar = x,y,par0
            else: 
                back = False
                redo = False

        # Only P4 visited before
        #=======================
        elif (p3==0) and (p4==1): 
            # Can this position be redone
            redo = gredo(x4,y4,x,y,par0)
            # P4 worse than P0, moving back
            #------------------------------
            if (b4==0) and redo: 
                newx,newy = x4,y4
                back = True   # moving backwards
                guessx,guessy,guesspar = x,y,par0
            else: 
                back = False
                redo = False

        # Both visited before
        #====================
        elif (p3==1) and (p4==1): 
            redo = False    # not redo unless proven otherwise 
            # Can these positions be redone
            redo3 = gredo(x3,y3,x,y,par0) 
            redo4 = gredo(x4,y4,x,y,par0) 

            # P3 worse than P0, but P4 better than P0 (or no gauss) (b3==0 and b4!=0)
            #----------------------------------------
            if (b3==0) and (b4!=0): 
                # We can redo it, moving back to P3 
                if redo3:
                    redo = True
                    newx,newy = x3,y3
                # Can't redo, move forward 
                else:
                    redo = False
                    back = False

            # P4 worse than P0, but P3 better than P0 (or no gauss) (b3!=0 and b4==0)
            #----------------------------------------
            elif (b3!=0) and (b4==0): 
                # We can redo it, moving back to P4 
                if redo4:
                    redo = True
                    newx,newy = x4,y4
                # Can't redo, move forward 
                else: 
                    redo = False
                    back = False

            # Both P3 and P4 are worse than P0
            #---------------------------------
            elif (b3==0) and (b4==0): 
                # Can redo either one, redo the one with the worse solution
                if redo3 and redo4:
                    redo = True
                    b34,dbic34 = gbetter(res3,res4)
                    # Moving back to P3 (P3 worse than P4) 
                    if (b34==1):   # to P3 
                        newx,newy = x3,y3
                    # Moving back to P4 (P4 worse than P3)
                    if (b34==0):   # to P4 
                        newx,newy = x4,y4
                # Can't redo P4, go to P3 
                if redo3 and (redo4==False):
                    redo = True
                    newx,newy = x3,y3   # to P3
                # Can't redo P3, go to P4 
                if (redo3==False) and redo4:
                    redo = True
                    newx,newy = x4,y4   # to P4
                # Can't do either, move forward 
                if (redo3==False) and (redo4==False): 
                    redo = False 
                    back = False

            # Both are better than P0 or both no Gaussians, move forward
            #-----------------------------------------------------------
            elif (b3!=0) and (b4!=0):
                back = False
                redo = False

            # Shouldn't ever happen
            else:
                import pdb; pdb.set_trace()
                
            # One is worse than P0
            #---------------------
            if redo: 
                back = True  # moving backwards 
                guessx,guessy,guesspar = x,y,par0

        # Neither visited before, backwards not possible
        #  p3==0 and p4==0
        else:
            back = False


    #==============================
    # ---- CHECKING FORWARD ----
    #==============================
    if ((p3==0) and (p4==0)) or (back==False) or noback: 

        # This is the very end 
        if (x1 is None) or (x==xr[1] and y==yr[1]):
            endflag = True
            return None,None,None,None,None,False,False,False,endflag

        back = False  # moving forward 

        # Only P1 has been visited before
        #================================
        if (p1==1) and (p2==0): 
            redo = True
            # Can this position be redone
            redo1 = gredo(x1,y1,x,y,par0) 
            # Moving to P1 (P1 worse than P0) 
            if (b1==0) and redo1: 
                newx,newy = x1,y1
            # Can't redo P1, or P1 better than P0, move another step ahead 
            else: 
                newx,newy = x1,y1
                redo = False
                skip = True  # don't fit this one 

        # Only P2 has been visited before, THIS SHOULD NEVER HAPPEN
        #================================                    
        elif (p1==0) and (p2==1): 
            print('This should never happen!!')
            import pdb; pdb.set_trace() 

        # Both have been visited before
        #==============================                  
        elif (p1==1) and (p2==1):
            # Can this position be redone            
            redo1 = gredo(x1,y1,x,y,par0) 
            redo2 = gredo(x2,y2,x,y,par0) 
            if (redo1==False) and (redo2==False):  # no redo 
                redo = False

            # P1 worse than P0, and P2 better than P0 (or no gauss) (b1==0 and b2!=0)
            #------------------------------------------------------
            if (b1==0) and (b2!=0): 
                # Can redo, moving to P1 
                if redo1: 
                    newx,newy = x1,y1
                    redo = True
                # Can't redo, increment to P1 and skip 
                else: 
                    newx,newy = x1,y1  # to P1 
                    redo = False
                    skip = True

            # P2 worse than P0, and P1 better than P0 (or no gauss) (b1==1 and b2==0)
            #------------------------------------------------------
            elif (b1!=0) and (b2==0): 
                # Can redo, moving to P2 
                if redo2: 
                    newx,newy = x2,y2
                    redo = True
                # Can't redo, increment to P1 and skip 
                else: 
                    newx,newy = x1,y1  # to P1 
                    redo = False
                    skip = True

            # Both worse than P0
            #-------------------
            elif (b1==0) and (b2==0):  # both bad, find worst 
                # Can redo either one, move to the one with the worse solution
                if redo1 and redo2:
                    redo = True
                    b12,dbic12 = gbetter(res1,res2)
                    # Moving to P1 (P1 worse than P2) 
                    if (b12==1):  # to P1 
                        newx,newy = x1,y1
                    # Moving to P2 (P2 worse than P1) 
                    if (b12==0):  # to P2
                        newx,newy = x2,y2

                # Can't redo P2, go to P1 
                if redo1 and (redo2==False):
                    redo = True
                    newx,newy = x1,y1  # to P1 
                # Can't redo P1, go to P2 
                if (redo1==False) and redo2:
                    redo = True
                    newx,newy = x2,y2   # to P2 
                # Can't do either, increment to P1 and skip 
                if (redo1==False) and (redo2==False): 
                    newx,newy = x1,y1  # to P1 
                    redo = False
                    skip = True 

            # Both better than P0 or both no Gaussians, increment to P1 and skip
            #-------------------------------------------------------------------
            elif (b1!=0) and (b2!=0):
                newx,newy = x1,y1    # to P1 
                redo = False
                skip = True 

            # Shouldn't ever happen
            else:
                print('Should not happen 1')
                import pdb; pdb.set_trace()
                

        # Neither has been visited before, increment to P1
        #=================================================
        elif (p1==0) and (p2==0): 
            # Increment to P1
            newx,newy = x1,y1

        # Should never happen
        else:
            print('Should not happen 2')
            import pdb; pdb.set_trace()            
            

    # No new position determined yet, move forward to P1
    if newx is None or newy is None:
        # Increment to P1
        newx,newy = x1,y1

    # Getting guess
    if newx is not None and newy is not None and guesspar is None:
        guesspar,guessx,guessy = gguess(newx,newy,xr,yr,xsgn,ysgn)
        
    try:
        dumx,dumy = newx,newy
    except:
        print('problem')
        import pdb; pdb.set_trace()

        
    return newx,newy,guessx,guessy,guesspar,back,redo,skip,endflag


def savedata(outfile):
    """ Save the data to files."""

    global BTRACK, GSTRUC, NPIX
    
    print('SAVING DATA to '+outfile)

    # Back up any existing file
    picklefile = outfile.replace('.fits','.pkl')
    backpicklefile = picklefile+'.backup'    
    if os.path.exists(picklefile):
        if os.path.exists(backpicklefile):
            shutil.move(picklefile,backpicklefile)
    
    # Write tracking structures to pickle file
    with open(picklefile, 'wb') as f:
        pickle.dump(BTRACK, f)
        pickle.dump(GSTRUC, f)                    

    # Remove backup file if it exists
    if os.path.exists(backpicklefile):
        os.remove(backpicklefile)
        
    # Construct gstruc output structure
    count = GSTRUC['count']
    ngauss = GSTRUC['ngauss']
    dtype = np.dtype([('x',int),('y',int),('par',float,3),('sigpar',float,3),('rms',float),
                      ('noise',float),('lon',float),('lat',float)])
    gstruc = np.zeros(ngauss,dtype=dtype)
    cnt = 0
    for i in range(count):
        tstr1 = GSTRUC['data'][i]
        ngauss1 = len(tstr1['par'])//3
        gstruc1 = np.zeros(ngauss1,dtype=dtype)
        gstruc1['x'] = tstr1['x']
        gstruc1['y'] = tstr1['y']
        gstruc1['lon'] = tstr1['lon']
        gstruc1['lat'] = tstr1['lat']        
        gstruc1['rms'] = tstr1['rms']
        gstruc1['noise'] = tstr1['noise']
        gstruc1['par'] = tstr1['par'].reshape(ngauss1,3)
        gstruc1['sigpar'] = tstr1['sigpar'].reshape(ngauss1,3)
        gstruc[cnt:cnt+ngauss1] = gstruc1
        cnt += ngauss1
    gstruc = Table(gstruc)
    gstruc.write(outfile,overwrite=True)
    print(str(len(gstruc))+' gaussians')
    
    return gstruc
    
def driver(datacube,xstart=0,ystart=0,xr=None,yr=None,xsgn=1,ysgn=1,outfile=None,
           plotxr=None,trackplot=False,noplot=True,silent=False,
           noback=False,backret=True,wander=False,startfile=None,
           savestep=10000,clobber=False):
    """
    This program runs the gaussian fitting program 
    on a large part of the HI all sky survey 
     
    This program can be run in three different modes. 
    backret: The program is allowed to go backwards, but MUST return to 
             the position it came from.  This seems to be the best mode 
             to run the program in for most purposes. 
             This is now the DEFAULT mode. 
    noback: The program is not allowed to go backwards.  It will always 
             move in a forward direction until it is finished.  Therefore 
             there is essentially no re-decomposition of positions. 
             To use this mode set noback=True on the command line. 
    wander: The program is allowed to go backwards and forwards (Haud's 
             original algorithm).  If it goes back in y and only 
             the forward x position has been visited before then 
             it will need to go through all x positions before 
             returning to where it came from.  So either use strips 
             narrow in x or run this only once an initial solution 
             for every position has been found. 
             To use this mode set wander=True on the command line. 
     
    If you input gstruc and btrack from a previous run, then the program 
    will start where it left off.  This is useful when you ran it with 
    backret and then want to use the wander mode.  But currently it 
    start where it left off, so if you want it to start at the very 
    beginning again you need to do something (such as adding btrack(0) 
    to the end of btrack: btrack = [btrack,btrack(0)]. 
    This can also be used for debugging purposes. 
     
    Parameters
    ----------
    datacube : array or st
      Cube object or filename.
    xstart : int, optional
       The x to start with.  Default is 0.
    ystart : int, optional
       The y to start with.  Default is 0.
    xr : list/array
       Two-element X range.
    yr : list/array
       Two-element Y range.
    xsgn : int, optional
       Direction of x increments (-1 or 1).  Default is 1.
    ysgn : int, optional
       Direction of y increments (-1 or 1). Default is 1.
    outfile : str, optional
       File to save the structures to.
    plotxr : list
       Plotting xrange.
    trackplot : boolean, optional
      Track the progression visually 
    noplot : boolean, optional
      Don't plot anything.  Default is True.
    silent : boolean, optional
      Don't print anything 
    noback : boolean, optional
      The program is not allowed to go backwards.  Default is False.
    backret : boolean, optional
       Any backwards motion must return to the position it 
         came from.  Default is True.
    wander : boolean, optional
       Allow backwards motion. Haud's algorithm.  Default is False.
    startfile : str, optional
       Start at the last position of this tracking file (pickle).
    savestep : int, optional
       Number of steps to save on.  Default is 5000.
    clobber : boolean, optional
       Overwrite any existing files.  Default is False.


    Returns
    -------
    gstruc : list
      List of all the gaussians found.

    Example
    -------

    gstruc = driver(cube)

    Created by David Nidever April 2005 
    Translated to python by D. Nidever, March 2022
    """

    global BTRACK, GSTRUC, NPIX

    savetime = time.time()
    endflag = False
    count = 0
    tstart = time.time() 


    # Load the cube
    if type(datacube) is str:
        datacubefile = datacube
        print('Loading '+datacubefile)
        datacube = Cube.read(datacubefile)
    
    # Setting parameters
    if xr is None:
        xr = [0,datacube.nx-1]
    if yr is None:
        yr = [0,datacube.ny-1]  
    if xstart is None:
        if xsgn == 1: 
            xstart = xr[0] 
        else: 
            xstart = xr[1]
    if ystart is None:
        if ysgn == 1 : 
            ystart = yr[0] 
        else: 
            ystart = yr[1]
    if wander:
        backret = False
    if noback:
        backret = False

    # No mode selected, using default mode (backret) 
    if (backret == False) and (noback == False) and (wander == False): 
        print('' )
        print('!!! WARNING !!!  NO MODE SELECTED  ->  USING DEFAULT (BACKRET) MODE' )
        print('')
        sleep(3) 
        backret = True


    # Checking the file
    if outfile is None:
        logtime = datetime.now().strftime("%Y%m%d%H%M%S") 
        outfile = 'gaussdecomp_'+logtime+'.fits' 

    # STARTING WITH BTRACK, RESTORING THE LAST STATE
    if startfile is not None:
        print('Starting with last state of input file '+str(startfile))
        with open(startfile,'rb') as f: 
            BTRACK = pickle.load(f)
            GSTRUC = pickle.load(f)
        count = BTRACK['count']
        x = BTRACK['x'][count-1]
        y = BTRACK['y'][count-1]
        track = BTRACK['data'][count-1]
        back = track['back']
        redo = track['redo']
        redo_fail = track['redo_fail']
        skip = False
        count += 1
        xstart = x
        ystart = y
        lastx = x 
        lasty = y
    # STARTING TRACKING FRESH
    else:
        initialize_tracking(wander,yr)
        redo_fail = False 
        redo = False
        back = False
        lastx = None
    lasty = None
        
    # Printing out the inputs
    if silent==False:
        print(' RUNNING GAUSSIAN ANALYSIS WITH THE FOLLOWING PARAMETERS')
        print('-----------------------------------------------------------')
        print(' STARTING POSITION = (%d,%d)' % (xstart,ystart))
        print(' X RANGE = [%d,%d]' % (xr[0],xr[1]))
        print(' Y RANGE = [%d,%d]' % (yr[0],yr[1]))
        print(' X DIRECTION = '+str(xsgn))
        print(' Y DIRECTION = '+str(ysgn))
        print(' OUTFILE = '+outfile)
        print('-----------------------------------------------------------')
        if (backret == 1) : 
            print(' USING (BACKRET) MODE')
        if (noback == 1) : 
            print(' USING (NOBACK) MODE')
        if (wander == 1) : 
            print(' USING (WANDER) MODE')
        print('-----------------------------------------------------------')
        print('')
 
    # Initializing some parameters 
    p0 = False
    p1 = False
    p2 = False
    p3 = False
    p4 = False     
    # Where are we starting 
    x = xstart 
    y = ystart 

    track_dict = {'count':None,'x':None,'y':None,'rms':None,'noise':None,'par':None,
                  'guesspar':None,'guessx':None,'guessy':None,'back':None,'redo':None,
                  'redo_fail':None,'skip':None,'lastx':None,'lasty':None,'npix':None}
    gstruc_dict = {'x':None,'y':None,'rms':None,'noise':None,'par':None,
                   'sigpar':None,'lon':None,'lat':None,'npix':None}

    
        
    # STARTING THE LARGE LOOP 
    while (endflag == False): 
        t00 = time.time() 
        skip,guessx,guessy,guesspar = False,None,None,None        
        tstr = {'par':None}
        tstr1 = {'par':None}
        tstr2 = {'par':None}        

        # FIGURE OUT THE NEXT MOVE 
        #------------------------- 
        if (count > 0):
            lastx,lasty = x,y
            out = nextmove(x,y,xr,yr,count,xsgn,ysgn,backret=backret,noback=noback,
                           wander=wander,redo=redo,back=back,redo_fail=redo_fail,silent=silent)
            x,y,guessx,guessy,guesspar,back,redo,skip,endflag = out
            
        # The end
        if endflag:
            break
            
        # Starting the tracking structure, bad until proven good
        track = track_dict.copy()
        track['count'] = count 
        track['x'] = x 
        track['y'] = y 
        track['lastx'] = lastx 
        track['lasty'] = lasty 
        track['guesspar'] = guesspar 
        track['guessx'] = guessx 
        track['guessy'] = guessy 
        track['back'] = back 
        track['redo'] = redo 
        track['skip'] = skip 

        # Minimal structure, in case we skip
        tstr = {'x':x,'y':y,'rms':np.inf,'noise':None,'par':None,
                'sigpar':None,'lon':None,'lat':None}
        
        # Some bug checking 
        if x is None: 
            import pdb; pdb.set_trace() 
        if (x == lastx) and (y == lasty): 
            import pdb; pdb.set_trace() 
 
        if skip:
            if silent==False:
                print('SKIP')
 
        # FITTING THE SPECTRUM, UNLESS WE'RE SKIPPING IT 
        #------------------------------------------------ 
        if skip == False: 
            t0 = time.time() 
            
            # Initial Printing
            if silent==False:
                print('Fitting Gaussians to the HI spectrum at (%d,%d)' % (x,y))
                strout = ''
                if redo:
                    strout = strout+'REDO '
                if back:
                    strout = strout+'BACK'
                if back is False:
                    strout = strout+'FORWARD' 
                print(strout) 
                          
            # Getting the HI spectrum
            spec = datacube(x,y)  # Get the new spectrum
            # No good spectrum 
            if spec is None or np.sum(spec.flux)==0:
                if silent==False:
                    print('No spectrum to fit')
                skip = True
                count += 1
                btrack_add(track)
                continue

            lon,lat = datacube.coords(x,y)
            noise = spec.noise
            npts = spec.n
            sigma = np.ones(npts,float)*noise
            NPIX = npts
            
            # Zero-velocity region INCLUDED
            #====================================            
            if np.min(spec.vel) < 0:
                # GETTIING THE VELOCITY RANGE around the zero-velocity MW peak
                if silent==False:
                    print('Zero-velocity region INCLUDED.  Fitting it separately')
                smspec = dln.savgol(spec.flux,21,2) 
                dum,vindcen = dln.closest(spec.vel,0)
            
                # Finding the vel. low point 
                lflag = 0 
                i = vindcen
                lo = 0
                while (lflag == 0): 
                    if smspec[i] <= noise: 
                        lo = i 
                    if smspec[i] <= noise: 
                        lflag = 1
                    i -= 1 
                    if i < 0: 
                        lflag = 1 
                lo = np.maximum(0,(lo-20))
 
                # Finding the vel. high point 
                hflag = 0 
                i = vindcen
                hi = npts-1
                while (hflag == 0): 
                    if smspec[i] <= noise : 
                        hi = i 
                    if smspec[i] <= noise : 
                        hflag = 1 
                    i += 1 
                    if i > npts-1: 
                        hflag = 1 
                hi = np.minimum((npts-1),(hi+20))
 
                vmin = spec.vel[lo] 
                vmax = spec.vel[hi] 
 
                # RUNNING GAUSSFITTER ON ZERO VELOCITY REGION, WITH GUESS 
                v0results = fitter.gaussfitter(spec,vmin=vmin,vmax=vmax,initpar=guesspar,silent=True,noplot=True)            
                
                # FIT WITH NO GUESS (if first time and previous fit above with guess) 
                tp0,tres0 = gfind(x,y,xr=xr,yr=yr) 
                if (tp0 == 0) and (guesspar is not None):
                    v0results_noguess = fitter.gaussfitter(spec,vmin=vmin,vmax=vmax,silent=True,noplot=True)
                    b,dbic = gbetter(results,results2)
                    # The fit without the guess is better 
                    if (dbic>0):
                        v0results = v0results_noguess.copy()
                        
                # ADDING THE BEST RESULTS TO THE STRUCTURE, TSTR1
                if v0results['par'] is not None:
                    ngauss = len(v0results['par'])//3
                    tstr1 = gstruc_dict.copy()
                    for n in ['par','sigpar','rms','npix']:
                        tstr1[n] = v0results[n]                                        
                    tstr1['x'] = x 
                    tstr1['y'] = y
                    tstr1['noise'] = spec.noise                    
                    tstr1['lon'] = lon
                    tstr1['lat'] = lat
                else:
                    tstr1 = {'par':None}
                    
                # REMOVING ZERO-VELOCITY parameters and spectrum
                guesspar2 = None
                inspec = spec.copy()
                if v0results['par'] is not None:
                    th = utils.gfunc(spec.vel,*v0results['par'])
                    inspec = spec.copy()
                    inspec.flux -= th
                    npts = spec.n
                    if guesspar is not None:
                        guesspar2 = np.array([],float)
                        inpar1 = np.copy(guesspar)
                        inpar2 = np.copy(guesspar)
                        inpar1 = utils.gremove(inpar1,spec.vel[0:lo],spec.flux[0:lo])
                        if inpar1 is not None:
                            guesspar2 = np.hstack((guesspar2,inpar1))
                        inpar2 = utils.gremove(inpar2,spec.vel[hi:npts],spec.flux[hi:npts])
                        if inpar2 is not None:
                            guesspar2 = np.hstack((guesspar2,inpar2))
                        if len(guesspar2)==0:
                            guesspar2 = None
 
                            
                # RUNNING GAUSSFITTER ON EVERYTHING WITHOUT THE ZERO-VELOCITY REGION, WITH GUESS 
                results = fitter.gaussfitter(inspec,initpar=guesspar2,noplot=True,silent=True)
            
 
                # FIT WITH NO GUESS (if first time and previous fit above with guess) 
                if (tp0 == 0) and (guesspar is not None):
                    results_noguess = fitter.gaussfitter(inspec,silent=True,noplot=True)                    
                    b,dbic34 = gbetter(results3,results4)
                    # The fit without the guess is better 
                    if (b == 1):
                        results = results_noguess.copy()
 
                # ADDING THE RESULTS TO THE STRUCTURE, TSTR2
                if results['par'] is not None:
                    ngauss = len(results['par'])//3 
                    tstr2 = gstruc_dict.copy()
                    for n in ['par','sigpar','rms','npix']:
                        tstr2[n] = results[n]               
                    tstr2['x'] = x 
                    tstr2['y'] = y
                    tstr2['noise'] = spec.noise
                    tstr2['lon'] = lon 
                    tstr2['lat'] = lat
                else:
                    tstr2 = {'par':None}
                    
                # ADDING THE STRUCTURES TOGETHER, TSTR = [TSTR1,TSTR2]
                if tstr1['par'] is not None and tstr2['par'] is not None:
                    tstr = tstr1.copy()
                    tstr['par'] = np.hstack((tstr1['par'],tstr2['par']))
                    tstr['sigpar'] = np.hstack((tstr1['sigpar'],tstr2['sigpar']))
                    tstr['rms'] = utils.computerms(spec.vel,spec.flux,tstr['par'])
                if tstr1['par'] is not None  and tstr2 is None:
                    tstr = tstr1.copy()
                if tstr1['par'] is None and tstr2['par'] is not None:
                    tstr = tstr2.copy()
                if tstr1['par'] is None and tstr2['par'] is None:  # no gaussians
                    tstr = gstruc_dict.copy()
                    tstr['x'] = x 
                    tstr['y'] = y 
                    tstr['lon'] = lon 
                    tstr['lat'] = lat 
                    tstr['rms'] = np.inf
                    tstr['noise'] = spec.noise 
                    tstr['npix'] = len(spec.flux)
                    
                        
            # Does NOT cover zero-velocity region
            #====================================
            else:
                if silent==False:
                    print('Zero-velocity NOT covered')
                # RUNNING GAUSSFITTER ON EVERYTHING WITH GUESS 
                results = fitter.gaussfitter(spec,initpar=guesspar,noplot=True,silent=True)            
                
                # FIT WITH NO GUESS (if first time and previous fit above with guess)
                tp0,res0 = gfind(x,y,xr=xr,yr=yr)
                results2 = None
                if (tp0 == 0) and (guesspar is not None):
                    results2 = fitter.gaussfitter(spec,silent=True,noplot=True)                    
                    b,dbic = gbetter(results,results2)
                    # The fit without the guess is better 
                    if (dbic>0): 
                        results = results2.copy()                        
                         
                # Creating the structure with the results
                if results['par'] is not None:
                    ngauss = len(results['par'])//3
                    tstr = gstruc_dict.copy()
                    for n in ['par','sigpar','rms','npix']:
                        tstr[n] = results[n]                    
                    tstr['x'] = x
                    tstr['y'] = y
                    tstr['noise'] = spec.noise
                    tstr['lon'] = lon 
                    tstr['lat'] = lat
                else:
                    tstr = {'par':None}
                    
 
            # PLOTTING/PRINTING, IF THERE WAS A FIT 
            if tstr['par'] is not None:
                # Getting the rms of all the components of the whole spectrum
                tstr['rms'] = utils.computerms(spec.vel,spec.flux,tstr['par'])
                    
                # Printing and plotting
                if noplot==False:
                    utils.gplot(spec.vel,spec.flux,tstr['par'],xlim=plotxr)
                if silent==False:
                    utils.printgpar(tstr['par'],sigpar=tstr['sigpar'],rms=tstr['rms'],noise=tstr['noise'])
                if trackplot:
                    utils.gtrackplot(x,y,lastx,lasty,redo, count,xr=xr,yr=yr,pstr=pstr,xstr=xstr,ystr=ystr)
            else:
                if silent==False:
                    print('No gaussians found at this position!')

            # ADDING SOLUTION TO GSTRUC
            if tstr['par'] is not None:
                if count == 0: 
                    gstruc_add(tstr)
                if count > 0: 
                    old,res1 = gfind(x,y,xr=xr,yr=yr)
 
                    # This is a re-decomposition 
                    if (old==1) and redo: 
                        # Checking the two decompositions 
                        b,dbic = gbetter(tstr,res1)
                        # New one is better 
                        if (b == False): 
                            gstruc_replace(tstr)  # replacing the solution
                            redo_fail = False
                        else: # re-decomposition failed 
                            redo_fail = True
                            if silent==False:
                                print('REDO FAILED!')
 
                    # This is NOT a re-decomposition, add it 
                    if (old==0) or (redo == False): 
                        t1 = time.time()
                        gstruc_add(tstr)
                        redo_fail = False


        # SKIP FITTING PART
        else: 
            # Creating a dummy structure 
            tstr = {'par':None}
            redo_fail = False
            redo = False
            back = False
 
            if trackplot:
                utils.gtrackplot(x,y,lastx,lasty,redo,count,xr=xr,yr=yr,pstr=pstr,xstr=xstr,ystr=ystr)

                
        # FINISHING UP THE TRACKING STRUCTURE
        if tstr['par'] is not None:
            npar = len(tstr['par'])
            track['par'] = tstr['par']
            track['rms'] = tstr['rms']
            track['noise'] = tstr['noise']
            track['npix'] = tstr['npix']
        else:
            npar = 0
        track['redo_fail'] = redo_fail 
 
        # UPDATING THE TRACKING STRUCTURE
        btrack_add(track)

        # The end
        if ((x>=xr[1]) and (y>=yr[1])):
            break
        
        count += 1 
 
        # Saving the last position 
        lastx = x 
        lasty = y 
  
        # SAVING THE STRUCTURES, periodically
        if (count % savestep == 0) and (time.time()-savetime) > 1800:
            gstruc = savedata(outfile)
            savetime = time.time()
            
    # FINAL SAVE
    ngauss = GSTRUC['ngauss']
    print(str(ngauss)+' final Gaussians')
    gstruc = savedata(outfile)
    
    # Clean up the tracking structures
    del BTRACK
    del GSTRUC

    print('Total time = %.2f sec.' % (time.time()-tstart))
    
    return gstruc

