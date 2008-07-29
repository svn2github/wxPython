class IRectangle(object):
    # size prop
    pass

class ICircle(object):
    # radius prop
    pass

class IEllipse(object):
    # size prop
    pass

class ILine(object):
    # length prop
    pass

class IPolygon(object):
    # points prop
    pass

class IPoints(object):
    # points prop
    pass

class ISpline(object):
    # points prop
    pass

class IText(object):
    # text prop
    pass


import events

class DefaultModelEventSender(object):
    def __setattr__(self, name, value):
        old_value = getattr(self, name, '<undefined>')
        object.__setattr__(self, name, value)
        events.send( 'modelChanged', object = self, attributeName = name, oldAttributeValue = old_value, newAttributeValue = value )

import numpy

class Rectangle(DefaultModelEventSender):
    implements_interfaces = IRectangle
    
    def __init__( self, size = (0,0) ):
        self.size = size
        
    def _setSize(self, value):
        self._size = numpy.array( value )
        
    def _getSize(self):
        return self._size
    
    size = property( _getSize, _setSize )
    
class Ellipse(DefaultModelEventSender):
    implements_interfaces = IEllipse

    def __init__( self, size = (0,0) ):
        self.size = numpy.array( size )
        
class Circle(DefaultModelEventSender):
    implements_interfaces = ICircle

    def __init__( self, radius = 0 ):
        self.radius = radius
        
class Line(DefaultModelEventSender):
    implements_interfaces = ILine

    def __init__( self, length = 0 ):
        self.length = length
                
class Text(DefaultModelEventSender):
    implements_interfaces = IText

    def __init__( self, text = '' ):
        self.text = text

class Polygon(object):
    # points prop
    pass

class Points(object):
    # points prop
    pass

class Spline(object):
    # points prop
    pass



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

from patterns.adapter import adapterRegistry
adapterRegistry.register( ICircle, IEllipse, CircleToEllipseAdapter )
