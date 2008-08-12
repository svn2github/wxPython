from baseRenderer import BaseRenderer
from ..models import IBitmap
from ..math import numpy

class DefaultBitmapRenderer(BaseRenderer):
    can_render = IBitmap
    
    def doCalcCoords(self, model):
        return ()
           
    def doCreate(self, renderer, coords):
        return renderer.CreateBitmap( self.model.pixels, self.model.useRealSize )