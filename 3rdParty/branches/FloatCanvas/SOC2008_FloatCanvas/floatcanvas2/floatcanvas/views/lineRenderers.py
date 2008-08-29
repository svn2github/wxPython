from ..models import ILinesList, ILineSegmentsSeparate
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import ILinesListViewModel, ILineSegmentsSeparateViewModel

class DefaultLinesListRenderer(object):
    can_render = ILinesList
    implements_interfaces = ILinesListViewModel
    
    def getCoords(self, model):
        return model.lines_list
           
    def getViewModel(self, model, coords):
        return ViewModel( 'LinesList', lines_list = coords )
        
        
class DefaultLineSegmentsSeparateRenderer(object):
    can_render = ILineSegmentsSeparate
    implements_interfaces = ILineSegmentsSeparateViewModel
    
    def getCoords(self, model):
        self.startPntIndex = len( model.startPoints )
        return numpy.concatenate( (model.startPoints, model.endPoints ) )
           
    def getViewModel(self, model, coords):
        return ViewModel( 'LineSegmentsSeparate', startPoints = coords[:self.startPntIndex], endPoints = coords[self.startPntIndex:] )
        
