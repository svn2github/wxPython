import numpy

class ModelWithSize(object):
    def __init__( self, size ):
        self.size = size
        
    def _setSize(self, value):
        self._size = numpy.array( value )
        
    def _getSize(self):
        return self._size
    
    size = property( _getSize, _setSize )
    
    
class ModelWithPoints(object):
    def __init__( self, points ):
        self.points = points
        
    def _setPoints(self, points):
        self._points = numpy.array( [ numpy.array( pnt ) for pnt in points ] )
        
    def _getPoints(self):
        return self._points
    
    points = property( _getPoints, _setPoints )
    

defaultAdapters = []

def registerModelAdapter( from_interface, to_interface, adapter ):
    return defaultAdapters.append( ( from_interface, to_interface, adapter ) )
