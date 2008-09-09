#!/usr/bin/env python

"""
Bases:

A collection of classes to implement Bases for FloatCanvas

A Base contains:

* (optional) an image, raster or vector
* methods to project to and from projected coordinates
* methods to format coordinates for display
"""

class Base(Object):
    def __init__(self):
        pass
    
    def WorldToProjected(self, coords):
        """
        calculates the projected coordinates from world coordinates
        
        coords in a NX2 numpy array of floats, 
        
        returns a NX2 numpy array of floats.
        """
        return coords
    
    def ProjectedToWorld(self, coords):
        return coords
    
    def Draw(self, Canvas):
        pass
    
class YDown(Base):
    """
    YDown
    
    A FloatCanvas Base that sets the coordinate system to y-down
    """
    pass

class Yup(Base):
    """
    Yup
    
    A FloatCanvas Base that sets the coordinate system to y-up
    """
    
    def ProjectedWorldToProjected(self, coords, center=None):
        return coords * (1, -1)
    
    def WorldToProjected(self, coords, center=None):
        return coords * (1, -1)
    

class DefaultBase = Yup

class FlatEarth(Base):
    MaxLatitude = 75 # these were determined essentially arbitrarily
    MinLatitude = -75
    
    def WorldToPojected(self, coords, CenterPoint):
        Lat = min(CenterPoint[1],MaxLatitude)
        Lat = max(Lat,MinLatitude)
        return coords * N.array((N.cos(N.pi*Lat/180),1),N.float)
    
