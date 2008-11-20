#!/usr/bin/env python

"""
A Bounding Box object and assorted utilities , subclassed from a numpy array

"""

import numpy as N

class BoundingBox(N.ndarray):
    """
    A Bounding Box object:
    
    Takes Data as an array. Data is any python sequence that can be turned into a 
    2x2 numpy array of floats:

    [[MinX, MinY ],
     [MaxX, MaxY ]]

    It is a subclass of numpy.ndarray, so for the most part it can be used as 
    an array, and arrays that fit the above description can be used in its place.
    
    Usually created by the factory functions:
    
        asBoundingBox
        
        and 
        
        fromPoints
    
    """
    def __new__(subtype, data):
        """
        Takes Data as an array. Data is any python sequence that can be turned into a 
        2x2 numpy array of floats:

        [[MinX, MinY ],
        [MaxX, MaxY ]]

        You don't usually call this directly. BoundingBox objects are created with the factory functions:
        
        asBoundingBox
        
        and 
        
        fromPoints

        """
        arr = N.array(data, N.float)
        arr.shape = (2,2)
        if arr[0,0] > arr[1,0] or arr[0,1] > arr[1,1]:
            # note: zero sized BB OK.
            raise ValueError("BoundingBox values not aligned: \n minimum values must be less that maximum values")
        return N.ndarray.__new__(BoundingBox, shape=arr.shape, dtype=arr.dtype, buffer=arr)

    def Overlaps(self, BB):
        """
        Overlap(BB):

        Tests if the given Bounding Box overlaps with this one.
        Returns True is the Bounding boxes overlap, False otherwise
        If they are just touching, returns True
        """

        if ( (self[1,0] >= BB[0,0]) and (self[0,0] <= BB[1,0]) and
             (self[1,1] >= BB[0,1]) and (self[0,1] <= BB[1,1]) ):
            return True
        else:
            return False

    def Inside(self, BB):
        """
        Inside(BB):

        Tests if the given Bounding Box is entirely inside this one.

        Returns True if it is entirely inside, or touching the
        border.

        Returns False otherwise
        """
        if ( (BB[0,0] >= self[0,0]) and (BB[1,0] <= self[1,0]) and
             (BB[0,1] >= self[0,1]) and (BB[1,1] <= self[1,1]) ):
            return True
        else:
            return False
    
    def Merge(self, BB):
        """
        Joins this bounding box with the one passed in, maybe making this one bigger

        """ 

        if BB[0,0] < self[0,0]: self[0,0] = BB[0,0]
        if BB[0,1] < self[0,1]: self[0,1] = BB[0,1]
        if BB[1,0] > self[1,0]: self[1,0] = BB[1,0]
        if BB[1,1] > self[1,1]: self[1,1] = BB[1,1]
        
    def intersection(self, other):
        # if other is a point instead of a bb, make a bb out of it
        if isinstance( other, tuple ):
            other = BoundingBox( ( other, other ) )
        
        # check intersection with bbox
        if not self.Overlaps(other):
            return 'none'
        elif self.Inside(other):
            return 'full'
        else:
            return 'partial'
        

    def _getWidth(self):
        return self[1,0] - self[0,0]

    def _getHeight(self):
        return self[1,1] - self[0,1]
    
    def _getSize(self):
        return self[1] - self[0]
        
    def _getMin(self):
        return self[0]

    def _getMax(self):
        return self[1]
    
    def _getCorners(self):
        center = self.center
        half_size = self.Size / 2.0
        
        upper_right = center + half_size
        lower_left  = center - half_size
        lower_right = center + half_size * ( 1, -1)
        upper_left  = center + half_size * (-1,  1)

        return N.array( (lower_left, upper_right, lower_right, upper_left) )

    width = property(_getWidth)
    height = property(_getHeight)
    Size = property(_getSize)
    min = property(_getMin)
    max = property(_getMax)
    corners = property(_getCorners)
    
    def _getCenter(self):
        return self.sum(0) / 2.0
    center = property(_getCenter)
    ### This could be used for a make BB from a bunch of BBs

    #~ def _getboundingbox(bboxarray): # lrk: added this
        #~ # returns the bounding box of a bunch of bounding boxes
        #~ upperleft = N.minimum.reduce(bboxarray[:,0])
        #~ lowerright = N.maximum.reduce(bboxarray[:,1])
        #~ return N.array((upperleft, lowerright), N.float)
    #~ _getboundingbox = staticmethod(_getboundingbox)


    ## Save the ndarray __eq__ for internal use.
    Array__eq__ = N.ndarray.__eq__
    def __eq__(self, BB):
        """
        __eq__(BB) The equality operator

        A == B if and only if all the entries are the same

        """
        return N.all(self.Array__eq__(BB))
        

def asBoundingBox(data):
    """
    returns a BoundingBox object.

    If object is a BoundingBox, it is returned unaltered

    If object is a numpy array, a BoundingBox object is returned that shares a
    view of the data with that array

    """

    if isinstance(data, BoundingBox):
        return data
    arr = N.asarray(data, N.float)
    return N.ndarray.__new__(BoundingBox, shape=arr.shape, dtype=arr.dtype, buffer=arr)

def fromPoints(Points):
    """
    fromPoints (Points).

    returns the bounding box of the set of points in Points. Points can
    be any python object that can be turned into a numpy NX2 array of Floats.

    If a single point is passed in, a zero-size Bounding Box is returned.
    
    """
    Points = N.asarray(Points, N.float).reshape(-1,2)

    arr = N.vstack( (Points.min(0), Points.max(0)) )
    return N.ndarray.__new__(BoundingBox, shape=arr.shape, dtype=arr.dtype, buffer=arr)

def fromBBArray(BBarray):
   """
   Builds a BoundingBox object from an array of Bounding Boxes. 
   The resulting Bounding Box encompases all the included BBs.
   
   The BBarray is in the shape: (Nx2x2) where BBarray[n] is a 2x2 array that represents a BoundingBox
   """
   
   #upperleft = N.minimum.reduce(BBarray[:,0])
   #lowerright = N.maximum.reduce(BBarray[:,1])

#   BBarray = N.asarray(BBarray, N.float).reshape(-1,2)
#   arr = N.vstack( (BBarray.min(0), BBarray.max(0)) )
   BBarray = N.asarray(BBarray, N.float).reshape(-1,2,2)
   arr = N.vstack( (BBarray[:,0,:].min(0), BBarray[:,1,:].max(0)) )
   return asBoundingBox(arr)
   #return asBoundingBox( (upperleft, lowerright) ) * 2
   

def fromRectangleCenterSize(center, size):
    half_size = size / 2.0
    
    #upper_right = center + half_size
    #lower_left  = center - half_size
    #lower_right = center + half_size * ( 1, -1)
    #upper_left  = center + half_size * (-1,  1)
                            
    #points = [ upper_right, lower_left, lower_right, upper_left ]
                             
    #return fromPoints( points )
    return BoundingBox( ( center - half_size, center + half_size ) )
   

def fromRectangleCornerSize(corner, size):
    #lower_left  = corner + size * ( 0, 0 )
    #upper_right = corner + size * ( 1, 1 )
    #lower_right = corner + size * ( 1, 0 )
    #upper_left  = corner + size * ( 0, 1 )
                            
    #points = [ upper_right, lower_left, lower_right, upper_left ]
                             
    #return fromPoints( points )
    return BoundingBox( ( corner, corner + size ) )


def fromPoint(point):
    return BoundingBox( ( point, point ) )

def getAlignedCoordinate(box, aligned):
    vert = aligned[0]
    horiz = aligned[1]

    # check if values are allowed
    if horiz not in ('l', 'c', 'm', 'r'):
        raise ValueError( 'Horizontal alignment needs to be either l, c, m or r' )
    if vert not in ('t', 'c', 'm', 'b'):
        raise ValueError( 'Vertical alignment needs to be either t, c, m or b' )

    multipliers = { 'l' : 0, 'c' : 0.5, 'm' : 0.5, 'r' : 1, 't' : 0, 'b' : 1 }

    return box.min + box.Size * N.array( (multipliers[horiz], multipliers[vert]) )
