from ..models import IPolygonList
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import IPolygonListViewModel

class DefaultPolygonListRenderer(object):
    can_render = IPolygonList
    implements_interfaces = IPolygonListViewModel

    def getCoords(self, model):
        return numpy.array( model.polygon_list )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'LinesList', lines_list = coords, close = True )
