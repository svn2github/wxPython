import observables
from ..nodes import RTree

class Canvas(observables.ObservableDefaultRenderableNode):
    ''' A plain canvas is basically the same as a renderable node. It features
         an rtree to perform spatial queries. Bounded children register to it.
        It's the base class for the other canvasses (especially SimpleCanvas)
        The rtree is not (yet?) implemented and a stub implementation.
    '''
    
    def __init__(self, *args, **keys):
        observables.ObservableDefaultRenderableNode.__init__(self, *args, **keys)
        self.rtree = RTree()
        
    def _registerBoundedNode(self, node):
        ''' internal. Bounded children call this function to register
            themselves.
        '''
        self.rtree.addChild(node)

    def _unregisterBoundedNode(self, node):
        ''' internal. Bounded children call this function to unregister
            themselves.
        '''
        self.rtree.removeChild(node)

    def performSpatialQuery( self, query ):
        ''' Call this with a nodes.spatialQuery.SpatialQuery object. Returns a
             bunch of nodes.
        '''
        return self.rtree.performSpatialQuery( query )
