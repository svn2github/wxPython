from baseRenderer import BaseRenderer
from ..models import IRectangle
import numpy   

class DefaultRectangleRenderer(BaseRenderer):
    can_render = IRectangle
    
    def doCalcCoords(self, model):
        half_size = model.size / 2.0
        return numpy.array( [-half_size, half_size] )
           
    def doCreate(self, renderer, coords):
        x, y = coords[0].tolist()
        w, h = abs(coords[1] - coords[0]).tolist()

        return renderer.CreateRectangle( x, y, w, h )
        
