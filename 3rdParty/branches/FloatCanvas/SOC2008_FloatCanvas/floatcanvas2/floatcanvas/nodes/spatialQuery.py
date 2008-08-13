class SpatialQuery(object):
    ''' Base class for a spatial query '''
    def __init__(self):
        pass

    def GetIntersection(self, rootNode):
        ''' Derived classes provide this method. rootNode gets passed and this
            function returns a list of nodes that match the query
        '''
        raise NotImplementedError()

    
class QueryWithPrimitive(SpatialQuery):
    ''' A spatial query which tests against a primitive. The only type of primi-
        tive supported so far are (axes aligned) bounding boxes.
    '''
    def __init__(self, primitive, exact = True):
        ''' primitive is the primitive to check against (only BoundingBox
            allowed right now.
            If exact is False then only intersection against the bounding boxes
            of the nodes is performed. exact = True is only valid for point
            queries and checks not only the node bounding boxes against this
            query's point, but performs more elaborate checks to see if the
            query point is inside the bounds of the node.
        '''        
        SpatialQuery.__init__(self)
        self.primitive = primitive
        self.exact = exact
        
    def GetIntersection(self, rootNode):
        ''' Implementation of the base class method. Returns a list of the nodes
            that match the criteria. The intersection method should return one
            of 'full', 'none' or 'partial'.
        '''
        result = [ node for node in rootNode.children if node.boundingBox.intersection( self.primitive ) != 'none' ]
        if self.exact:
            result = [ node for node in result if node.intersection( self.primitive ) != 'none' ]
        return result
