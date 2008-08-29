from ..models import IEllipse, IArc
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import IEllipseViewModel, IArcViewModel

class DefaultEllipseRenderer(object):
    can_render = IEllipse
    implements_interfaces = IEllipseViewModel

    def getCoords(self, model):
        half_size = model.size / 2.0
        return numpy.array( [-half_size, half_size] )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'Ellipse', corner = coords[0], size = abs(coords[1] - coords[0]) )


class DefaultArcRenderer(object):
    can_render = IArc
    implements_interfaces = IArcViewModel

    def getCoords(self, model):
        return numpy.array( [0, 0] )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'CircularArc', center = coords, radius = model.radius, startAngle = model.startAngle, endAngle = model.endAngle, clockwise = model.clockwise )
