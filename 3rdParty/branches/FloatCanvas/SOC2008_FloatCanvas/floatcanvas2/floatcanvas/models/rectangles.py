from interfaces import IRectangle, IRoundedRectangle
from common import ModelWithSize
from eventSender import DefaultModelEventSender

class Rectangle(ModelWithSize, DefaultModelEventSender):
    implements_interfaces = IRectangle
    
    
class RoundedRectangle(ModelWithSize, DefaultModelEventSender):
    implements_interfaces = IRoundedRectangle

    def __init__( self, size, radius ):
        ModelWithSize.__init__(self, size)
        self.radius = radius