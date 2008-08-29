from ..models import IText
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import ITextViewModel

class DefaultTextRenderer(object):
    can_render = IText
    implements_interfaces = ITextViewModel

    def getCoords(self, model):
        return numpy.array( () )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'Text', text = model.text )