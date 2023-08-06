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

# ## Module template
# 
# Goals of the module:
# - Template functions

##HEADER
from pryngles import *

Example_doc="""
Class Example
"""

class Example(object):
    example=1
    def __init__(self):
        self.a=1
Example.__doc__=Example_doc

Example_method_doc="""
    This is a test method of class Example.
"""
def method(self):
    print(self.a)
Example.method=method
Example.method.__doc__=Example_method_doc

