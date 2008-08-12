from baseRenderer import BaseRenderer
from ..models import ICubicSpline, IQuadraticSpline
from ..math import numpy

class DefaultCubicSplineRenderer(BaseRenderer):
    can_render = ICubicSpline
    
    def doCalcCoords(self, model):
        return numpy.array( model.points )
           
    def doCreate(self, renderer, coords):
        return renderer.CreateCubicSpline( coords )
    
class DefaultQuadraticSplineRenderer(BaseRenderer):
    can_render = IQuadraticSpline
    
    def doCalcCoords(self, model):
        return numpy.array( model.points )
           
    def doCreate(self, renderer, coords):
        return renderer.CreateQuadraticSpline( coords )