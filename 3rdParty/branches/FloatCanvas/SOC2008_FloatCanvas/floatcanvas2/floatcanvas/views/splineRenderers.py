from ..models import ICubicSpline, IQuadraticSpline
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import ICubicSplineViewModel, IQuadraticSplineViewModel

class DefaultCubicSplineRenderer(object):
    can_render = ICubicSpline
    implements_interfaces = ICubicSplineViewModel
    
    def getCoords(self, model):
        return numpy.array( model.points )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'CubicSpline', controlPoints = coords )
    
class DefaultQuadraticSplineRenderer(object):
    can_render = IQuadraticSpline
    implements_interfaces = IQuadraticSplineViewModel
    
    def getCoords(self, model):
        return numpy.array( model.points )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'QuadraticSpline', controlPoints = coords )
