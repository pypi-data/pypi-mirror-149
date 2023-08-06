#!/usr/bin/env python

"""SPECTRUM.PY - Spectrum model class

"""

from __future__ import print_function

__authors__ = 'David Nidever <dnidever@noao.edu>'
__version__ = '20200122'  # yyyymmdd                                                                                                                           
import os
import numpy as np
import warnings
import copy
from astropy.io import fits
from scipy import sparse
from scipy.interpolate import interp1d
from dlnpyutils import utils as dln
from . import utils

# Ignore these warnings, it's a bug
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

class Spectrum:
    # A class for the radio spectra
        
    # Initialize the object
    def __init__(self,flux,vel,gpars=None,blankvrange=None):
        self.flux = flux
        self.vel = vel
        self.vrange = [np.min(vel),np.max(vel)]
        self.dv = np.median(np.diff(vel))
        self.blankvrange = blankvrange
        self.n = len(flux)
        self._noise = None
        self._gpars = gpars
        self._model = None

    def __repr__(self):
        out = self.__class__.__name__ + '('
        out += 'N=%d, %.2f < V < %.2f)\n' % \
               (self.n,self.vrange[0],self.vrange[1])
        return out

    def __str__(self):
        out = self.__class__.__name__ + '('
        out += 'N=%d, %.2f < V < %.2f)\n' % \
               (self.n,self.vrange[0],self.vrange[1])
        return out
    
    @property
    def noise(self):
        if self._noise is not None:
            return self._noise
        noise = utils.computenoise(self)
        self._noise = noise
        return noise

    @property
    def model(self):
        if self._model is not None:
            return self._model
        if self._gpars is None:
            return None
        model = utils.gaussmodel(self._gpars,self.vel)
        self._model = model
        return model

    def copy(self):
        """ Create a copy of the spectrum."""
        return copy.deepcopy(self)
    
    def write(self,outfile):
        """ Write spectrum to a file."""
        out = np.zeros((n,2),float)
        out[:,0] = self.flux
        out[:,1] = self.vel
        hdu = fits.HDUList()
        hdu.append(fits.PrimaryHDU(out))
        hdu.writeto(outfile,overwrite=True)
        
    @classmethod
    def read(cls,infile):
        """ Read in a spectrum from a file."""
        data,head = fits.getdata(infile,header=True)
        return Spectrum(data[:,0],data[:,1])
    
