from baseRenderer import BaseRenderer
from ..models import IPolygonList
from ..math import numpy

class DefaultPolygonListRenderer(BaseRenderer):
    can_render = IPolygonList
    
    def doCalcCoords(self, model):
        return numpy.array( model.polygon_list )
           
    def doCreate(self, renderer, coords):
        return renderer.CreateLinesList( coords, True )