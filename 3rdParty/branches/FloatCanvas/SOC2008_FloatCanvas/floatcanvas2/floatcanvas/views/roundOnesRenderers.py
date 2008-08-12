from baseRenderer import BaseRenderer
from ..models import IEllipse, IArc
from ..math import numpy


class DefaultEllipseRenderer(BaseRenderer):
    can_render = IEllipse

    def doCalcCoords(self, model):
        half_size = model.size / 2.0
        return numpy.array( [-half_size, half_size] )
           
    def doCreate(self, renderer, coords):
        x, y = coords[0].tolist()
        w, h = abs(coords[1] - coords[0]).tolist()

        return renderer.CreateEllipse( x, y, w, h )


class DefaultArcRenderer(BaseRenderer):
    can_render = IArc

    def doCalcCoords(self, model):
        return numpy.array( [0, 0] )
           
    def doCreate(self, renderer, coords):
        x, y = coords.tolist()

        return renderer.CreateArc( x, y, self.model.radius, self.model.startAngle, self.model.endAngle, self.model.clockwise )
