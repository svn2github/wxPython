from ..math import LinearAndArbitraryCompoundTransform, LinearTransform2D
from ..math import boundingBox as boundingBoxModule


class BaseRenderer(object):
    ''' Base class for all default primitive renderers.
        It mainly deals with transformation issues. To do so, it splits its
        transformation in linear and arbitrary transform. Then it calculates
        pre-transformed coordinates by putting the coordinates which it gets
        from doCalcCoords (implemented in derived class) into the arbitary
        transform. Then those coordinates are fed into doCreate (which is also
        implemented in the derived classes). When the arbitrary transform
        changes it will re-transform the pre-transformed coordinates and
        re-create the render_object.
        It forwards things like boundingBox and intersection check code to its
        render_object.
        Derived classes should implement the doCreate and doCalcCoords methods.
    '''
    def __init__(self, renderer, model, look, scaled = True):
        self.renderer = renderer
        self.model = model
        self.look = look
        self.scaled = scaled
        self._lastNonLinearTransform = None
        self._transform = LinearTransform2D()
        self.rebuild()
    
    def Render(self, camera):
        ''' Renders the render_object '''
        self.render_object.Draw( camera )
        
    def create(self):
        ''' Called to create the render object '''
        self.render_object = self.doCreate( self.renderer, self.transformedCoords )
        try:
            self.render_object.transform = self._transform
        except AttributeError:
            pass
        
    def doCreate(self, coords):
        ''' Base classes should override this one. It's fed with the
            pre-transformed coordinates and should return the render_object
            to be used for drawing.
        '''
        raise NotImplementedError()

    def rebuild(self):
        ''' Rebuild everything '''
        self.calcCoords()
        self.create()
        self._recalculateBoundingBox()

    def calcCoords(self):        
        ''' Get coordinates and pre-transform them '''
        self.coords = self.doCalcCoords( self.model )
        self.transformCoords()
        
    def transformCoords(self):
        ''' Pre-transform the coordinates with the non-linear parts of the
            transform and re-create if neccessary.
        '''
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
                if type(self.coords) == list:
                    self.transformedCoords = [ transform.transform2( coord ) for coord in self.coords ]
                else:
                    self.transformedCoords = transform.transform2( self.coords )
                # need to recreate our object since the coords changed
                self.create()
        else:
            raise ValueError( 'NotImplemented %s %s' % (transform, type(transform)) )

       
    def doCalcCoords(self, model):
        ''' Base classes should override this one. Should return the
            untransformed coordinates for creation of the object.
        '''
        raise NotImplementedError()
    
    def intersection(self, primitive):
        return self.render_object.intersects( primitive )

    def _setTransform(self, transform):
        ''' If the transform changes, we probably need to retransform our
            coordinates and the bounding box might change, too.
        '''
        self._transform = transform        
        self.transformCoords()
        self.render_object.transform = self._transform
        self._recalculateBoundingBox()
        
    def _getTransform(self):
        return self._transform

    transform = property( _getTransform, _setTransform )

    def _recalculateBoundingBox(self):
        ''' Calculates the bounding box by applying the linear part of our
            transform on our local bounding box.
        '''
        bb = self.localBoundingBox
        try:
            transform = self.transform.transform1
        except AttributeError:
            transform = self.transform
        self._boundingBox = boundingBoxModule.fromPoints( transform( bb.corners ) )

    def _getBoundingBox(self):
        return self._boundingBox

    boundingBox = property( _getBoundingBox )

    def _getLocalBoundingBox(self):
        return self.render_object.localBoundingBox
            
    localBoundingBox = property( _getLocalBoundingBox )
