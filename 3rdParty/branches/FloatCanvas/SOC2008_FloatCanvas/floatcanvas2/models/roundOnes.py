from interfaces import IEllipse, ICircle, IArc
from common import ModelWithSize, registerModelAdapter
from eventSender import DefaultModelEventSender
import numpy

class Ellipse(ModelWithSize, DefaultModelEventSender):
    implements_interfaces = IEllipse

        
class Circle(DefaultModelEventSender):
    implements_interfaces = ICircle

    def __init__( self, radius ):
        self.radius = radius


class Arc(object):
    implements_interfaces = IArc

    def __init__( self, radius ):
        self.radius = radius
    # radius prop
    # startAngle, endAngle props
    # clockwise prop
    pass


# ----- adapters -------

class CircleToEllipseAdapter(object):
    implements_interfaces = IEllipse
    
    def __init__(self, circle):
        self.circle = circle
        
    def _getSize(self):
        return numpy.array( (self.circle.radius, self.circle.radius) )
    
    def _setSize(self, value):
        assert value[0] == value[1], 'Circle objects need to the same size in x and y directions'
        self.circle.radius = value[0]
        
    size = property( _getSize, _setSize )

registerModelAdapter( ICircle, IEllipse, CircleToEllipseAdapter )
