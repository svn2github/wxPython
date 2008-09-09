from ..models import IRectangle, IRoundedRectangle
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import IRectangleViewModel,IRoundedRectangleViewModel

class DefaultRectangleRenderer(object):
    can_render = IRectangle
    implements_interfaces = IRectangleViewModel
    
    def getCoords(self, model):
        half_size = model.size / 2.0
        return numpy.array( [-half_size, half_size] )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'Rectangle', corner = coords[0], size = abs(coords[1] - coords[0]) )
        

class DefaultRoundedRectangleRenderer(object):
    can_render = IRoundedRectangle
    implements_interfaces = IRoundedRectangleViewModel
    
    def getCoords(self, model):
        half_size = model.size / 2.0
        return numpy.array( [-half_size, half_size] )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'RoundedRectangle', corner = coords[0], size = abs(coords[1] - coords[0]), radius = model.radius )
        
