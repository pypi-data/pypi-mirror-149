#!/usr/bin/env python

"""CUBE.PY - Datacube model class

"""

from __future__ import print_function

__authors__ = 'David Nidever <dnidever@montana.edu>'
__version__ = '20220326'  # yyyymmdd                                                                                                                           
import os
import numpy as np
import warnings
import copy
from scipy import sparse
from scipy.interpolate import interp1d
from astropy import units
from astropy.io import fits
from astropy.wcs import WCS
from dlnpyutils import utils as dln
from . import utils,spectrum

# Ignore these warnings, it's a bug
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

class Cube:
    # A class for the radio data cube
        
    # Initialize the object
    def __init__(self,data=None,header=None,getfunction=None,vdim=None,vel=None):
        self.getfunction = getfunction
        self.data = data  # assuming this has already been properly transposed!!!
        if data is not None:       
            self.shape = data.shape
        else:
            self.shape = None
        self.header = copy.deepcopy(header)
        if self.header is not None:
            self.wcs = WCS(self.header)
        else:
            self.wcs = None
        if vdim is not None:
            self.vdim = vdim
        if header is not None and vdim is None:
            for i in range(3):
                ctype = header.get('ctype'+str(i+1))
                if 'vel' in ctype.lower() or 'vrad' in ctype.lower() or 'vlsr' in ctype.lower():
                    self.vdim = i
        if self.vdim is not None:
            naxis = header.get('naxis'+str(self.vdim+1))
            cdelt = header.get('cdelt'+str(self.vdim+1))
            crval = header.get('crval'+str(self.vdim+1))
            crpix = header.get('crpix'+str(self.vdim+1))
            vel = crval + cdelt * (np.arange(naxis)+1-crpix)
            self.vunit = units.km/units.s  # assume km/s
            # Convert from m/s to km/s
            vunit = self.header.get('CUNIT'+str(self.vdim+1))
            if vunit is not None:
                if vunit.lower().strip()=='m/s':
                    vel /= 1e3
                    self.vunit = units.km/units.s
            else:
                print('No units for velocity.  Assuming m/s')
                vel /= 1e3
                self.vunit = units.km/units.s
            self.vel = vel
            self.nvel = naxis
        else:
            self.vel = None
            self.nvel = None
        # X and Y dimensions and sizes
        if self.vdim is not None:
            left = np.arange(3)
            left = np.delete(left,self.vdim)
            self.xdim = left[0]
            naxis1 = header.get('naxis'+str(self.xdim+1))            
            x = np.arange(naxis1).astype(int)
            self.x = x
            self.nx = len(x)
            #self.xtype = ctype1
            self.ydim = left[1]            
            naxis2 = header.get('naxis'+str(self.ydim+1))
            y = np.arange(naxis2).astype(int)
            self.y = y
            self.ny = len(y)
            #self.ytype = ctype2
        else:
            self.xdim = None
            self.ydim = None
            self.nx = None
            self.ny = None
            self.x = None
            self.y = None
        
    def __repr__(self):
        out = self.__class__.__name__
        if self.data is not None:
            out += '([%d,%d,%d], %.2f < V < %.2f %s)\n' % \
                   (self.shape[0],self.shape[1],self.shape[2],np.min(self.vel),np.max(self.vel),self.vunit)             
        return out

    def __str__(self):
        out = self.__class__.__name__
        if self.data is not None:
            out += '([%d,%d,%d], %.2f < V < %.2f %s)\n' % \
                   (self.shape[0],self.shape[1],self.shape[2],np.min(self.vel),np.max(self.vel),self.vunit) 
        return out

    def __call__(self,x,y):
        """ Return the spectrum at a given X/Y position."""
        if x<0 or y<0:  # out of bounds
            return None
        if self.getfunction is not None:
            return self.getfunction(x,y)
        else:
            if x>(self.nx-1) or y>(self.ny-1):  # out of bounds
                return None
            if self.vdim == 0:
                vel,flux = np.copy(self.vel), np.copy(self.data[:,x,y])
            elif self.vdim == 1:
                vel,flux = np.copy(self.vel), np.copy(self.data[x,:,y])                
            elif self.vdim == 2:
                vel,flux = np.copy(self.vel), np.copy(self.data[x,y,:])                
            else:
                print('not understood')
        # Return spectrum object
        return spectrum.Spectrum(flux,vel)
                
                
    def coords(self,x,y):
        """ Get the coordinates for this X/Y position."""
        if self.wcs is not None:
            if self.vdim==0:
                out = self.wcs.pixel_to_world(0,x,y)
                if len(out)==3:
                    dum,lon,lat = out
            elif self.vdim==1:
                out = self.wcs.pixel_to_world(x,0,y)
                if len(out)==3:
                    lon,dum,lat = out
            elif self.vdim==2:
                out = self.wcs.pixel_to_world(x,y,0)
                if len(out)==3:
                    lon,lat,dum = out
            if len(out)==2:
                c = out[0]
                keys = list(c.frame.representation_component_names.keys())
                lon = getattr(c,keys[0]).value
                lat = getattr(c,keys[1]).value
            return lon,lat        
        else:
            return x,y

    def copy(self):
        """ Create a copy of the cube."""
        return copy.deepcopy(self)
                    
    def write(self,outfile):
        """ Write cube to a file."""
        if self.data is None:
            print('No data to write out')
            return
        hdu = fits.HDUList()
        hdu.append(fits.PrimaryHDU(self.cube,self.header))
        # add values to header
        if self.vdim is not None:
            hdu[0].header['vdim'] = vdim
        hdu.writeto(outfile,overwrite=True)

    @classmethod
    def read(cls,infile):
        """ Read in a cube from a file."""
        data,head = fits.getdata(infile,header=True)
        # get information from header?
        return Cube(data.T,header=head)
