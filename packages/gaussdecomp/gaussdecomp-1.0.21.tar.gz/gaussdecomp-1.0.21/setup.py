#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='gaussdecomp',
      version='1.0.21',
      description='Gaussian Decomposition',
      author='David Nidever',
      author_email='dnidever@montana.edu',
      url='https://github.com/dnidever/gaussdecomp',
      packages=find_packages(exclude=["tests"]),
      scripts=['bin/gaussdecomp'],
      install_requires=['numpy','astropy(>=4.0)','scipy','dlnpyutils(>=1.0.3)','dill']
)
