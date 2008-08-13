from interfaces import IEllipse, ICircle, IArc
from common import ModelWithSize, registerModelAdapter
from eventSender import DefaultModelEventSender
from ..math import numpy


class Ellipse(ModelWithSize, DefaultModelEventSender):
    ''' Model of an ellipse which is assumed to be centered around (0,0) which
        has a 2d tuple size attribute.
    '''
    implements_interfaces = IEllipse

        
class Circle(DefaultModelEventSender):
    ''' Model of an ellipse which is assumed to be centered around (0,0) which
        has a radius attribute.
    '''
    implements_interfaces = ICircle

    def __init__( self, radius ):
        self.radius = radius


class Arc(object):
    ''' Model of an arc (a piece of a circle). Radius specifies the radius of
        the circle, startAngle and endAngle specify which piece of the circle
        to take and clockwise is a bool which specifies whether the clockwise or
        anticlockwise piece between startAngle and endAngle are taken.
    '''
    implements_interfaces = IArc

    def __init__( self, radius, startAngle, endAngle, clockwise ):
        self.radius = radius
        self.startAngle = startAngle
        self.endAngle = endAngle
        self.clockwise = clockwise


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
