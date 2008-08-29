from ..math import LinearAndArbitraryCompoundTransform, LinearTransform2D
from ..math import boundingBox as boundingBoxModule
from ..events import EventSender


class RemoveNonLinearTransformFromCoords(EventSender):
    def __init__(self, getUntransformedCoords):
        self.getUntransformedCoords = getUntransformedCoords
        self._transform = LinearTransform2D()
        self.linearTransform = LinearTransform2D()
        self.lastNonLinearTransform = None
        self.calcCoords()

    def calcCoords(self):        
        ''' Get coordinates and pre-transform them '''
        self.coords = self.getUntransformedCoords()
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
            self.linearTransform = transform
            self.lastNonLinearTransform = None
            
        elif isinstance(transform, LinearAndArbitraryCompoundTransform):
            # check if the non-linear part is the same. If it is, no need to
            # recreate the shape
            if self.lastNonLinearTransform != transform.transform2:
                if type(self.coords) == list:
                    self.transformedCoords = [ transform.transform2( coord ) for coord in self.coords ]
                else:
                    self.transformedCoords = transform.transform2( self.coords )

                self.linearTransform = transform.transform1                    
                self.lastNonLinearTransform = transform.transform2
                # need to recreate our object since the coords changed
                self.send( 'coordsChanged', coords = self.transformedCoords )
        else:
            raise ValueError( 'NotImplemented %s %s' % (transform, type(transform)) )

       
    def _setTransform(self, transform):
        self._transform = transform        
        self.transformCoords()
        
    def _getTransform(self):
        return self._transform

    transform = property( _getTransform, _setTransform )



from ..patterns.partial import partial

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
    def __init__(self, renderer, look, model, primitiveRenderer, scaled = True):
        self.renderer = renderer
        self.look = look
        self.scaled = scaled
        self.model = model
        
        self.getCoords = partial( primitiveRenderer.getCoords, model )
        self.getViewModel = primitiveRenderer.getViewModel

        self.transformer = RemoveNonLinearTransformFromCoords( self.getCoords )
        self.transformer.subscribe( self.on_create, 'coordsChanged' )
        self.create( self.transformer.transformedCoords )
    
    def Render(self, camera):
        ''' Renders the render_object '''
        self.render_object.Draw( camera )
        
    def on_create(self, event):
        self.create( event.coords )
        
    def create(self, coords):
        ''' Called to create the render object '''
        viewModel = self.getViewModel( self.model, coords )
        self.render_object = self.renderer.CreateRenderObject( viewModel.kind, **viewModel.elements )
        try:
            self.render_object.transform = self.transform
        except AttributeError:
            pass
        self._recalculateBoundingBox()
        
    def rebuild(self):
        ''' Rebuild everything '''
        self.transformer.calcCoords()
        self.create( self.transformer.transformedCoords )
    
    def intersection(self, primitive):
        return self.render_object.intersects( primitive )

    def _setTransform(self, transform):
        ''' If the transform changes, we probably need to retransform our
            coordinates and the bounding box might change, too.
        '''
        self.transformer.transform = transform
        self.render_object.transform = self.transformer.linearTransform
        self._recalculateBoundingBox()
        
    def _getTransform(self):
        return self.transformer.transform

    transform = property( _getTransform, _setTransform )

    def _recalculateBoundingBox(self):
        ''' Calculates the bounding box by applying the linear part of our
            transform on our local bounding box.
        '''
        bb = self.localBoundingBox
        bbtransform = self.transformer.linearTransform
        self._boundingBox = boundingBoxModule.fromPoints( bbtransform( bb.corners ) )

    def _getBoundingBox(self):
        return self._boundingBox

    boundingBox = property( _getBoundingBox )

    def _getLocalBoundingBox(self):
        if self.render_object.boundingBoxDependentOnLook:
            self.look.Apply( self.renderer )
        return self.render_object.localBoundingBox
            
    localBoundingBox = property( _getLocalBoundingBox )
