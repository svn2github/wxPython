class IRectangle(object):
    # size prop
    pass

class IRoundedRectangle(object):
    # size prop
    # radius prop
    pass
    

class ICircle(object):
    # radius prop
    pass

class IEllipse(object):
    # size prop
    pass


class IArc(object):
    # radius prop
    # startAngle, endAngle props
    # clockwise prop
    pass

class ICubicSpline(object):
    # points prop
    pass

class IQuadraticSpline(object):
    # points prop
    pass



class ILine(object):
    # start, end props
    pass

class ILineLength(object):
    # length prop
    pass

class ILines(object):
    # points prop
    pass
    
class ILineSegments(object):
    # startAndEndPoints prop
    pass

class ILineSegmentsSeparate(object):
    # startPoints prop
    # endPoints prop
    pass
    
    
class IPolygon(object):
    # points prop
    pass

class IPoints(object):
    # points prop
    # shape prop
    # size prop
    pass


class IText(object):
    # text prop
    pass

class IBitmap(object):
    pass

# fc1 objects:
# Polygon, Line, Spline, Arrow, ArrowLine, PointSet, Point, SquarePoint, Rectangle, Ellipse, Circle, Text, ScaledTextBox, Bitmap, DotGrid, Arc
# remaining: Arrow, ArrowLine, Bitmap, DotGrid, Arc, RoundedRectangle, lines, scaled variants

import events

class DefaultModelEventSender(object):
    def __setattr__(self, name, value):
        old_value = getattr(self, name, '<undefined>')
        object.__setattr__(self, name, value)
        events.send( 'modelChanged', object = self, attributeName = name, oldAttributeValue = old_value, newAttributeValue = value )

import numpy

class ModelWithSize(object):
    def __init__( self, size ):
        self.size = size
        
    def _setSize(self, value):
        self._size = numpy.array( value )
        
    def _getSize(self):
        return self._size
    
    size = property( _getSize, _setSize )
    
        
class Rectangle(ModelWithSize, DefaultModelEventSender):
    implements_interfaces = IRectangle
    
    
class RoundedRectangle(ModelWithSize, DefaultModelEventSender):
    implements_interfaces = IRoundedRectangle

    def __init__( self, size, radius ):
        ModelWithSize.__init__(self, size)
        self.radius = radius


class Ellipse(ModelWithSize, DefaultModelEventSender):
    implements_interfaces = IEllipse

        
class Circle(DefaultModelEventSender):
    implements_interfaces = ICircle

    def __init__( self, radius ):
        self.radius = radius
        
class Line(DefaultModelEventSender):
    implements_interfaces = ILineLength

    def __init__( self, startPoint, endPoint ):
        self.startPoint = numpy.array( startPoint )
        self.endPoint = numpy.array( startPoint )

class LineLength(DefaultModelEventSender):
    implements_interfaces = ILineLength

    def __init__( self, length ):
        self.length = length
                
class Text(DefaultModelEventSender):
    implements_interfaces = IText

    def __init__( self, text = '' ):
        self.text = text

class Polygon(object):
    implements_interfaces = IPolygon

    def __init__( self, points = [] ):
        self.points = numpy.array( [ numpy.array( pnt ) for pnt in points ] )

class Points(object):
    implements_interfaces = IPoints

    def __init__( self, points, shape, size ):
        self.points = numpy.array( [ numpy.array( pnt ) for pnt in points ] )
        self.shape = shape
        self.size = size

class Spline(object):
    implements_interfaces = ISpline

    def __init__( self, points = [] ):
        self.points = numpy.array( [ numpy.array( pnt ) for pnt in points ] )



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
