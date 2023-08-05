#!/usr/bin/env python

import os
import time
import numpy as np
from . import utils
from dlnpyutils import utils as dln

def gaussfitter(spectrum,initpar=None,noplot=True,ngauss=None,silent=False,
                color=False,vmax=None,vmin=None,debug=False,noremovesmall=False):
                
    """
    This program tries to do gaussian analysis 
    on HI spectra. 
     
    Parameters
    ----------
    spectrum : Spectrum object
       The spectrum to fit.
    initpar : numpy array, optional
       Initial guess of parameters 
    vmin : float, optional
       The minimum velocity to use.
    vmax : float, optional
       The maximum velocity to use 
    noplot : boolean, optional
       Don't plot anything 
    silent : boolean, optional
       Don't print anything 
    debug : boolean, optional
       Diagnostic printing and plotting.
    noremovesmall : boolean, optional
       Do not try to remove small Gaussians
         at the end.
     
    Returns
    -------
    par0      Final parameters 
    v         Array of velocities 
    spec      Spectrum 
    resid     The residuals 
    rms       The rms of the residuals 
     
    Example
    -------

    par,v,spec,resid,rms = gaussfitter(spectrum)
     
    Written by D. Nidever, April 2005 
    Translated to python by D. Nidever, March 20222
    """

    noresults = {'par':None,'sigpar':None,'resid':None,'rms':None,'noise':None,'npix':None}
    
    # Start time 
    gt0 = time.time() 
     
    # Getting the HI spectrum
    v = np.copy(spectrum.vel)
    spec = np.copy(spectrum.flux)
    npix = len(spec)    
    # Estimating the noise
    noise = spectrum.noise
    noise_orig = noise
    sigma = np.ones(npix,float)*noise
    noresults['noise'] = noise
    noresults['rms'] = utils.computerms(v,spec)
    noresults['npix'] = npix
    
    # Velocity range 
    if vmin is None:
        vmin = np.min(v)
    if vmax is None:
        vmax = np.max(v)
    gd, = np.where((v >= vmin) & (v <= vmax))
    ngd = len(gd)
    spec = spec[gd]
    v = v[gd] 
    dv = v[1]-v[0]
    dum,vindcen = dln.closest(v,0)
     
    # Initalizing Some Parameters
    par0 = None
    npts = len(v) 
    rms = 999999. 
    rms0 = 999999. 
    count = 0 
    npar0 = 0 
    y = np.copy(spec)
    endflag = 0 
    addt0 = time.time() 
 
    # TRYING THE FIRST GUESS PARAMETERS
    #----------------------------------
    finpar = None
    if initpar is not None:
        if silent==False:
            print('Using First Guess Parameters')
        inpar = np.copy(initpar)     
        inpar = utils.gremove(inpar,v,y) # removing bad ones 
        inpar = utils.gremdup(inpar,v)   # removing the duplicates 
     
        # Letting everything float
        if inpar is not None:
            finpar,sigpar,rms,chisq,residuals,noise,success,rt1 = utils.gfit(v,y,inpar,noise=noise)
            finpar = utils.gremove(finpar,v,y)  # removing bad ones 
            finpar = utils.gremdup(finpar,v)    # removing the duplicates 

        
    # ADDING GAUSSIANS
    #-----------------
 
    # One gaussian added per loop
    flag = 0
    while (flag != 1): 

        if silent==False:
            print('count = ',str(count))
     
        # Using the initial guess 
        if finpar is not None:
            par0 = np.copy(finpar)
        if par0 is not None:
            npar0 = len(par0)
            
        # Getting the Residuals 
        if par0 is not None and len(par0)>0:
            th = utils.gfunc(v,*par0)
            if th[0] != 999999.: 
                resid = y-th 
            else: 
                resid = np.copy(y)
        else:
            resid = np.copy(y)
         
        # Smoothing the data
        smresid4 = dln.savgol(resid, 9,2) 
        smresid16 = dln.savgol(resid, 33,2) 
        if (npts > 61): 
            smresid30 = dln.savgol(resid, 61,2) 
        else: 
            smresid30 = np.zeros(npts,float)
        if (npts > 101): 
            smresid50 = dln.savgol(resid, 101,2) 
        else: 
            smresid50 = np.zeros(npts,float)
        if (npts > 201): 
            smresid100 = dln.savgol(resid, 201,2) 
        else: 
            smresid100 = np.zeros(npts,float)
        maxy = np.max(resid) 

         
        # Setting up some arrays 
        rmsarr = []
        pararr = []
        gcount = 0 
         
        # Looping through the different smoothed spectra 
        for s in range(5):
         
            # Getting the right smoothed spectrum 
            if s==0:
                smresid = smresid4
            elif s==1:
                smresid = smresid16
            elif s==2:
                smresid = smresid30
            elif s==3:
                smresid = smresid50
            elif s==4:
                smresid = smresid100 
         
            # Getting maxima 
            maxarr = utils.gpeak1(smresid,np.maximum(5*noise,0.5*maxy))
            if len(maxarr)==0:
                maxarr = utils.gpeak1(smresid,np.maximum(5*noise,0.1*maxy))
            if len(maxarr)==0:
                maxarr = utils.gpeak1(smresid,5*noise)
            if len(maxarr)==0:
                maxarr = utils.gpeak1(smresid,3*noise)
            if len(maxarr)==0:
                maxarr = utils.gpeak1(smresid,2*noise)
            ngd = len(maxarr) 
         
            # If there are any peaks check them out 
            if ngd > 0:
                # Looping through the peaks and fitting them 
                # to the proper residual spectrum 
                # only one gaussian, plus a line 
                for i in range(ngd): 
                    maxi = maxarr[i]
                    # Getting guess and fitting it
                    par2,gind = utils.gest(v,smresid,maxi)
                    # Only do it if there is a good range
                    if len(gind)>0:
                        par2s = np.hstack((par2,np.array([0.01,0.01])))
                        fpar2s,sigpar2,rms2,chisq2,residuals,noise2,success2,rt2 = utils.gfit(v[gind],smresid[gind],par2s,noise=noise)
                        fpar2 = fpar2s[0:3]
                        rms = np.std(resid-utils.gfunc(v,*fpar2))
                    else: 
                        rms = 999999.
                        fpar2 = np.zeros(3,float)+999999.
             
                    # Adding to the rms and par arrays 
                    rmsarr.append(rms)
                    pararr.append(fpar2)
             
                    gcount += 1
 
        # Only taking the good rms
        ngdrms = 0
        if len(rmsarr)>0:
            rmsarr = np.array(rmsarr)
            pararr = np.array(pararr)
            # Only taking the good rms 
            gdrms, = np.where(rmsarr < 999999.) 
        else:
            gdrms = np.array([],int)
        ngdrms = len(gdrms)
        
        # No good ones 
        if ngdrms == 0:
            if (count == 0):
                return noresults
            else: 
                flag = 1
                count += 1
                continue 
        rmsarr = rmsarr[gdrms]
        pararr = pararr[gdrms,:]
        pararr = pararr.flatten()
        
        # Removing bad gaussians 
        pararr = utils.gremove(pararr,v,y)
 
        # Removing the duplicates
        if pararr is not None:
            pararr = utils.gremdup(pararr,v)
        
        # No good ones
        if pararr is None:
            flag = 1
            count += 1
            continue
        if len(pararr) < 2:
            return noresults
            flag = 1
            count += 1
            continue
 
 
        # Setting up some arrays 
        n = len(pararr)//3 
        rmsarr2 = np.zeros(n,float)
        if par0 is not None:
            pararr2 = np.zeros((n,len(par0)+3),float)
        else:
            pararr2 = np.zeros((n,3),float)
        sigpararr2 = np.copy(pararr2) 
        successarr2 = np.zeros(n,bool)
        
        if silent is False:
            print(str(n)+' gaussian candidates')
 
 
        # Looping through the candidates that are left 
        #  allowing everything to float 
        for i in range(n): 
            ipar = pararr[3*i:3*i+3] 
            if par0 is not None:
                par = np.hstack((par0,ipar))
            else:
                par = np.copy(ipar)
                
            # Letting everything float
            fpar,sigpar,rms,chisq,residuals,noise5,success5,rt5 = utils.gfit(v,y,par,noise=noise)
            npar = len(fpar)
            rmsarr2[i] = rms 
            pararr2[i,:] = fpar 
            sigpararr2[i,:] = sigpar 
            successarr2[i] = success5
            
            # Giagnostic plotting and printing
            if debug:
                utils.gplot(v,y,fpar)
                utils.printgpar(fpar,sigpar=sigpar,rms=rms,noise=noise,chisq=chisq,success=success)
                sleep(1.5)
 
        # Adding the gaussian with the lowest rms
        gdi, = np.where((rmsarr2 == np.min(rmsarr2)) & (rmsarr2 != 999999) & (successarr2==True))
        if len(gdi)>0:
            par0 = pararr2[gdi,:].flatten()
            npar0 = len(par0) 
            sigpar = sigpararr2[gdi,:].flatten()
            rms = rmsarr2[gdi][0]
            sigpar00 = sigpar 
            rms00 = rms 
        else:
            par0 = None
            npar0 = 0
            sigpar = None
            rms = 999999.
            rms00 = rms
            
        # Plot what we've got so far 
        #if not keyword_set(noplot) then gplot,v,spec,par0 
 
        # Printing the parameters 
        if silent==False and rms != 999999: 
            utils.printgpar(par0,sigpar=sigpar,rms=rms,noise=noise,chisq=chisq)
 
        # Ending Criteria 
        drms = (rms0-rms)/rms0 
        if (rms <= noise) : 
            flag = 1 
        if (rms >= rms0) : 
            flag = 1 
        if (drms < 0.02) : 
            flag = 1 
 
        # Saving the rms 
        rms0 = rms 
 
        count += 1
        
      
    if silent==False:
        print(' Addition of Gaussians ',time.time()-addt0,' sec')

    # No gaussians found 
    if par0 is None or len(par0)==0:
        return noresults
        
    # Saving the results of the fit
    sigpar00 = sigpar 
    rms00 = rms 
 
    # Plot what we've got so far
    if noplot is False:
        utils.gplot(v,spec,par0)
 
    # Printing the parameters 
    if silent==False:
        utils.printgpar(par0,sigpar=sigpar00,rms=rms,noise=noise)
 
    # REMOVING GAUSSIANS 

    
    # Removing bad gaussians 
    par0 = utils.gremove(par0,v,y)
    
    # Removing the duplicates 
    par0 = utils.gremdup(par0,v)
 
    # None left - End
    if par0 is None:
        return noresults
 
    # Sorting the gaussians by area 
    orig_par0 = par0 
    ngauss = len(par0)//3 
    par0 = utils.gsort(par0) 

    
    # See if removing the smallest (in area) gaussian changes much
    if noremovesmall:
        if silent==False:
            print('Attempting to remove small Gaussians')
    
        count = 0 
        ngauss = len(par0)//3
        if silent==False:
            print('Ngauss = %d' % ngauss)
    
        orig_par0 = par0 
        nrefit = int(np.ceil(ngauss/2))
        if ngauss==1:
            nrefit = 0

        sigma = np.ones(npts,float)*noise
        weights = 1/sigma**2
        rms0 = utils.computerms(v,spec,par0)
        bic0 = utils.bayesinfocrit({'par':par0,'rms':rms0,'noise':noise,'npix':npix})
    
        # Loop through the smallest 1/2 
        for i in range(nrefit): 
            ig = ngauss-i-1 
            tpar = np.copy(par0)
            # Remove the gaussian in question
            todel = np.arange(3)+ig*3
            tpar = np.delete(tpar,todel)
            # Finding the best fit
            fpar,sigpar,rms,chisq,residuals,noise5,success,rt5 = utils.gfit(v,y,tpar,noise=noise)
            drms = rms-rms0
            bic1 = utils.bayesinfocrit({'par':fpar,'rms':rms,'noise':noise,'npix':npix})
            # Remove the gaussian 
            if (success==True) and (bic1 < bic0):   # (drms/rms0 < 0.02)
                if silent==False:
                    print('removing gaussian')
                par0 = fpar
                rms0 = utils.computerms(v,spec,par0)            
                # saving the results of the fit 
                #  without this gaussian 
                sigpar00 = sigpar 
                rms00 = rms 
                chisq00 = chisq 
                success00 = success
            
    # Removing bad gaussians 
    par0 = utils.gremove(par0,v,y)

    # No parameters left
    if par0 is None or len(par0)==0:
        return noresults
    
    # Run it one last time for the final values
    fpar,sigpar,rms,chisq,resid,noise5,success,rt5 = utils.gfit(v,y,par0,noise=noise)
    par0 = fpar 
    if success==False:
        return noresults
    
    # Final Results 
    if noplot==False:
        utils.gplot(v,spec,par0)
    if silent==False:
        utils.printgpar(par0,sigpar=sigpar,rms=rms,noise=noise,chisq=chisq)
 
    # Printing the total time
    if silent==False:
        print('Total time = ',str(time.time()-gt0))
 
    # No gaussians found 
    if par0 is None:
        return noresults

    results = {'par':par0,'sigpar':sigpar,'resid':resid,'rms':rms,'noise':spectrum.noise,'npix':npix}
    return results
