from interfaces import IRectangle, IRoundedRectangle
from common import ModelWithSize
from eventSender import DefaultModelEventSender

class Rectangle(ModelWithSize, DefaultModelEventSender):
    ''' A rectangle which is assumed to be centered around (0,0) and with a
        2d size attribute.
    '''
    implements_interfaces = IRectangle
    
    
class RoundedRectangle(ModelWithSize, DefaultModelEventSender):
    ''' A rounded rectangle which is assumed to be centered around (0,0) and 
        with a 2d  size attribute. Additionally it features a radius attribute.
        The bigger the radius, the rounder the corners.
    '''

    implements_interfaces = IRoundedRectangle

    def __init__( self, size, radius ):
        ModelWithSize.__init__(self, size)
        self.radius = radius