from ..transform import LinearAndArbitraryCompoundTransform, LinearTransform2D
from .. import boundingBox as boundingBoxModule


class BaseRenderer(object):
    def __init__(self, renderer, model, look, scaled = True):
        self.renderer = renderer
        self.model = model
        self.look = look
        self.scaled = scaled
        self._lastNonLinearTransform = None
        self._transform = LinearTransform2D()
        self.rebuild()
    
    def Render(self, camera):
        self.render_object.Draw( camera )
        
    def create(self):
        self.render_object = self.doCreate( self.renderer, self.transformedCoords )
        try:
            self.render_object.transform = self._transform
        except AttributeError:
            pass
        
    def doCreate(self, coords):
        # override
        raise NotImplementedError()

    def rebuild(self):
        self.calcCoords()
        self.create()
        self._recalculateBoundingBox()

    def calcCoords(self):
        self.coords = self.doCalcCoords( self.model )
        self.transformCoords()
        
    def transformCoords(self):
        try:
            transform = self._transform
        except AttributeError:
            self.transformedCoords = self.coords
            return
        
        if isinstance(transform, LinearTransform2D):
            self.transformedCoords = self.coords
        elif isinstance(transform, LinearAndArbitraryCompoundTransform):
            # check if the non-linear part is the same. If it is, no need to
            # recreate the shape
            if self._lastNonLinearTransform != transform.transform2:
                self.transformedCoords = transform.transform2( self.coords )
                # need to recreate our object since the coords changed
                self.create()
        else:
            raise ValueError( 'NotImplemented %s %s' % (transform, type(transform)) )

        self.transformedCoords = self.coords

        
    def doCalcCoords(self, model):
        # override
        raise NotImplementedError()
    
    def intersection(self, primitive):
        return self.render_object.intersects( primitive )

    def _setTransform(self, transform):
        self._transform = transform        
        self.transformCoords()
        self.render_object.transform = self._transform
        self._recalculateBoundingBox()
        
    def _getTransform(self):
        return self._transform

    transform = property( _getTransform, _setTransform )

    def _recalculateBoundingBox(self):
        bb = self.localBoundingBox
        self._boundingBox = boundingBoxModule.fromPoints( self.transform( bb.corners ) )

    def _getBoundingBox(self):
        return self._boundingBox

    boundingBox = property( _getBoundingBox )

    def _getLocalBoundingBox(self):
        return self.render_object.localBoundingBox
            
    localBoundingBox = property( _getLocalBoundingBox )
