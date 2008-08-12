from baseRenderer import BaseRenderer
from ..models import ILinesList, ILineSegmentsSeparate
from ..math import numpy

class DefaultLinesListRenderer(BaseRenderer):
    can_render = ILinesList
    
    def doCalcCoords(self, model):
        return model.lines_list
           
    def doCreate(self, renderer, coords):
        return renderer.CreateLinesList( coords )
        
        
class DefaultLineSegmentsSeparateRenderer(BaseRenderer):
    can_render = ILineSegmentsSeparate
    
    def doCalcCoords(self, model):
        self.startPntIndex = len(model.startPoints)
        return numpy.concatenate( (model.startPoints, model.endPoints ) )
           
    def doCreate(self, renderer, coords):
        return renderer.CreateLineSegmentsSeparate( coords[:self.startPntIndex], coords[self.startPntIndex:] )
        