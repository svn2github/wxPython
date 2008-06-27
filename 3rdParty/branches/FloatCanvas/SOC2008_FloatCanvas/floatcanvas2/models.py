# todo: clear this up if/when we decide for an external interface package
def implements(arg):
    pass

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


class Rectangle(DefaultModelEventSender):
    implements( IRectangle )
    def __init__( self, size = (0,0) ):
        self.size = size
    
class Ellipse(DefaultModelEventSender):
    implements( IEllipse )
    def __init__( self, size = (0,0) ):
        self.size = size
        
class Circle(DefaultModelEventSender):
    implements( ICircle )
    def __init__( self, radius = 0 ):
        self.radius = radius
        
class Line(DefaultModelEventSender):
    implements( ILine )
    def __init__( self, length = 0 ):
        self.length = length
                
class Text(DefaultModelEventSender):
    implements( IText )
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
