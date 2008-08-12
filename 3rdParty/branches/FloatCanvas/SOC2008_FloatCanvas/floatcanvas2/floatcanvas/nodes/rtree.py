# stub implementation of an r-tree
# for real one see: http://pypi.python.org/pypi/Rtree
# unfortunately it requires an underlying c library and is not available
# in packaged form. If huge trees/lots of spatial queries become an issue
# we might take a look at it again (or write a pure python implementation).

from ..math.boundingBox import BoundingBox

class RTree(object):
    children = []
    
    ''' maintains a flat list of nodes and performs queries in linear fashion '''
    def performSpatialQuery( self, query ):
        return query.GetIntersection( self )
    
    def addChild( self, child ):
        self.children.append( child )

    
    def _getBoundingBox(self):
        bb = BoundingBox( [ [0,0], [0,0] ] )
        for child in self.children:
            bb.Merge( child.boundingBox )
            
        return bb

    boundingBox = property( _getBoundingBox )