##################################################################
#                                                                #
#.#####...#####...##..##..##..##...####...##......######...####..#
#.##..##..##..##...####...###.##..##......##......##......##.....#
#.#####...#####.....##....##.###..##.###..##......####.....####..#
#.##......##..##....##....##..##..##..##..##......##..........##.#
#.##......##..##....##....##..##...####...######..######...####..#
#................................................................#
#                                                                #
# PlanetaRY spanGLES                                             #
# The bright-side of the light-curve of (ringed) exoplanets      #
#                                                                #
##################################################################
# Jorge I. Zuluaga, Mario Sucerquia, Jaime A. Alvarado (C) 2022  #
##################################################################
#!/usr/bin/env python
# coding: utf-8

# # Pryngles module

# ## Module of basic functions
# 
# Goals of the module:
# - Future `__init__`

##HEADER
from pryngles import *
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

# ## Package macros use across the modules

from collections import OrderedDict as odict

# ## Global constants
# 
# All global constants in Pryngles have a capital name and a lowercase version in the class util.

#Root directory
import os
try:
    __rootdir__=os.path.abspath(os.path.dirname(__file__))
except:
    import IPython
    __rootdir__=os.path.abspath('')

#Version
import pkg_resources
__version__=pkg_resources.require('pryngles')[0].version

#Mathematical constants
import numpy as np
rad=180/np.pi
deg=1/rad

#Astronomical constants
import rebound as rb
from rebound.units import times_SI,lengths_SI,masses_SI

# ## Clases

util_doc="""
Util routines.

This is a set of util routines intended for a diversity of purposes.

Routines included:

    get_data(file)
""";

class util(object):
    def getData(path):
        """
        Get the full path of the `datafile` which is one of the datafiles provided with the package.
        
        Parameters:
            datafile: Name of the data file, string.
            
        Return:
            Full path to package datafile in the python environment.
            
        """
        return os.path.join(__rootdir__,'data',path);
util.__doc__=util_doc

class PrynglesCommon(object):
    def __str__(self):
        return str(self.__dict__)    

