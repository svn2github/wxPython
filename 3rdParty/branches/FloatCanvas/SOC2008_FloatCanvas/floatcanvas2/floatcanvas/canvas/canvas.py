import observables
from rtree import RTree

class Canvas(observables.ObservableDefaultRenderableNode):
    def __init__(self, *args, **keys):
        observables.ObservableDefaultRenderableNode.__init__(self, *args, **keys)
        self.rtree = RTree()
        
    def _registerBoundedNode(self, node):
        self.rtree.addChild(node)

    def _unregisterBoundedNode(self, node):
        self.rtree.removeChild(node)

    def performSpatialQuery( self, query ):
        return self.rtree.performSpatialQuery( query )
