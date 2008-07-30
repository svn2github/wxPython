from interfaces import IBitmap
from eventSender import DefaultModelEventSender

class Bitmap(DefaultModelEventSender):
    implements_interfaces = IBitmap

    def __init__( self, pixels ):
        self.pixels = pixels