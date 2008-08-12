from interfaces import IBitmap
from eventSender import DefaultModelEventSender

class Bitmap(DefaultModelEventSender):
    implements_interfaces = IBitmap

    def __init__( self, pixels, useRealSize = True ):
        self.pixels = pixels
        self.useRealSize = useRealSize