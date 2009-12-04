from __future__ import absolute_import
from ..math.boundingBox import BoundingBox

class StubRTree(object):
    ''' stub implementation of an r-tree (slow)
    Maintains a flat list of nodes and performs queries in linear fashion. '''

    def __init__(self):
        self.children = []
  
    def performSpatialQuery( self, query ):
        ''' perform a spatial query on the tree '''
        return query.GetIntersection( self )
    
    def intersect( self, boundingBox ):
        return [ node for node in self.children if node.boundingBox.intersection( boundingBox ) != 'none' ]
    
    def addChild( self, child ):
        ''' add a child to the tree '''
        self.children.append( child )
        
    def removeChild( self, child ):
        self.children.remove( child )
    
    def _getBoundingBox(self):
        ''' bounding box of all children '''
        bb = BoundingBox( [ [0,0], [0,0] ] )
        for child in self.children:
            bb.Merge( child.boundingBox )
            
        return bb

    boundingBox = property( _getBoundingBox )
    childCount = property( lambda self: len(self.children) )



class FastRTree(object):
    '''
    fast implementation of an r-tree, requires http://pypi.python.org/pypi/Rtree
    '''

    def __init__(self):
        self.childToId = {}
        self.idToChild = {}
        self.id = 0
        self.rtree = rtree.Rtree()
  
    def performSpatialQuery( self, query ):
        ''' perform a spatial query on the tree '''
        return query.GetIntersection( self )
    
    def intersect( self, boundingBox ):
        ids = self.rtree.intersection( boundingBox.flat )
        #print ids
        return [ self.idToChild[id][0] for id in ids ]

    def addChild( self, child ):
        ''' add a child to the tree '''
        try:
            bounds = child.boundingBox
        except ValueError:
            bounds = BoundingBox( (0,0,0,0) )
        self.idToChild[ self.id ] = (child, bounds)
        self.childToId[ child ] = self.id
        self.rtree.add( self.id, bounds.flat )
        #print '+', self.id, bounds.center, bounds.Size
        child.subscribe( self.onInvalidBounds, 'nodeBoundsInvalid' )
        self.id += 1

    def onInvalidBounds(self, evt):
        self.removeChild( evt.node )
        self.addChild( evt.node )
        
    def removeChild( self, child ):
        id = self.childToId[ child ]
        del self.childToId[ child ]
        bounds = self.idToChild[ id ][1]
        del self.idToChild[ id ]
        self.rtree.delete( id, bounds.flat )
        #print '-', id, bounds.center, bounds.Size
        child.unsubscribe( self.onInvalidBounds, 'nodeBoundsInvalid' )
    
    def _getBoundingBox(self):
        ''' bounding box of all children '''
        return BoundingBox( self.rtree.bounds )

    boundingBox = property( _getBoundingBox )
    childCount = property( lambda self: len(self.childToId) )



try:
    import rtree
except ImportError:
    RTree = StubRTree
else:    
    RTree = FastRTree
