class SpatialQuery(object):
    def __init__(self):
        pass

    def GetIntersection(self, rootNode):
        raise NotImplementedError()

    
class QueryWithPrimitive(SpatialQuery):
    def __init__(self, primitive, exact = True):
        SpatialQuery.__init__(self)
        self.primitive = primitive
        self.exact = exact
        
    def GetIntersection(self, rootNode):
        result = [ node for node in rootNode.children if node.boundingBox.intersection( self.primitive ) != 'none' ]
        if self.exact:
            result = [ node for node in result if node.intersection( self.primitive ) != 'none' ]
        return result
