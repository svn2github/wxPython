from interfaces import IBitmap
from eventSender import DefaultModelEventSender

class Bitmap(DefaultModelEventSender):
    ''' Bitmap model. Has pixels which is a 2d numpy array. The parameter
        useRealSize specifies whether each pixel is seen as a unit, e.g. if the
        pixels array has 800x600 dimension the bitmap is considered to be
        800x600 units wide. If useRealSize is False, the bitmap size is assumed
        to be unit sized (-0.5, 0.5).
    '''
    implements_interfaces = IBitmap

    def __init__( self, pixels, useRealSize = True ):
        self.pixels = pixels
        self.useRealSize = useRealSize