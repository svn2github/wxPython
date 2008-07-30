from baseRenderer import BaseRenderer
from ..models import IText
import numpy

class DefaultTextRenderer(BaseRenderer):
    can_render = IText

    def doCalcCoords(self, model):
        return numpy.array( () )
           
    def doCreate(self, renderer, coords):
        return renderer.CreateText( self.model.text )

    def _getBoundingBox(self):
        self.look.Apply( self.renderer )
        return self._boundingBox

    boundingBox = property( _getBoundingBox )

    def _getLocalBoundingBox(self):
        self.look.Apply( self.renderer )
        return self.render_object.localBoundingBox
            
    localBoundingBox = property( _getLocalBoundingBox )
