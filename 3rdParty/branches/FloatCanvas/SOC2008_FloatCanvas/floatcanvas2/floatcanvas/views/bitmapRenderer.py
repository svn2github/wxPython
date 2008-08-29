from ..models import IBitmap
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import IBitmapViewModel

class DefaultBitmapRenderer(object):
    can_render = IBitmap
    implements_interfaces = IBitmapViewModel
    
    def getCoords(self, model):
        return ()
           
    def getViewModel(self, model, coords):
        return ViewModel( 'Bitmap', pixels = model.pixels, use_real_size = model.useRealSize )
