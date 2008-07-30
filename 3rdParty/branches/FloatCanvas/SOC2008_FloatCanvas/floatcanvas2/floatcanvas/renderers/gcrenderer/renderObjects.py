from ...math import LinearTransform2D, numpy
from ...math import boundingBox as boundingBoxModule


class GCRenderObjectBase(object):
    def __init__(self, renderer):
        self.renderer = renderer
        self._rendererTransform = renderer.CreateMatrix()
        self._transform = LinearTransform2D()
        
    def Draw(self, camera):
        self._rendererTransform.Set( *list( (camera.viewTransform * self.transform).matrix[ :-1, ... ].transpose().flat) )
        self.renderer.SetTransform( self._rendererTransform )
                                     
    def _getTransform(self):
        return self._transform
    
    def _setTransform(self, transform):
        self._rendererTransform.Set( *list(transform.matrix[ :-1, ... ].transpose().flat) )
        self._transform = transform
        
    transform = property( _getTransform, _setTransform )    
   
    
class GCRenderObjectPath(GCRenderObjectBase):
    def __init__(self, renderer, path):
        GCRenderObjectBase.__init__(self, renderer)
        self.path = path

        x, y, w, h = self.path.GetBox()
        corner = numpy.array( (x,y) )
        size = numpy.array( (w,h) )
        self._localBoundingBox = boundingBoxModule.fromRectangleCornerSize( corner, size )
        
    def Draw(self, camera):
        GCRenderObjectBase.Draw(self, camera)
        self.path.Draw()
        
    def intersects(self, primitive):
        assert primitive.min == primitive.max, ('Can only test against points', primitive)
        #print primitive.min
        pnt = self.transform.inverse( (primitive.min,) )[0]
        if self.path.Contains( *pnt.tolist() ):
            return 'full'
        else:
            return 'none'
        
    def _getLocalBoundingBox(self):
        return self._localBoundingBox

    localBoundingBox = property( _getLocalBoundingBox )
        
        
class GCRenderObjectText(GCRenderObjectBase):
    def __init__(self, renderer, text):
        GCRenderObjectBase.__init__(self, renderer)
        self.text = text
        self.active_font = None
        self._localBoundingBox = boundingBoxModule.BoundingBox( ( (0,0), (0,0) ) )
        
    def Draw(self, camera):
        GCRenderObjectBase.Draw(self, camera)

        offset = self.localBoundingBox.min
        backgroundBrush = self.renderer.active_brush.brush
        self.renderer.GC.DrawText( self.text, offset[0], offset[1], backgroundBrush )
        #angle = 0
        #self.renderer.GC.DrawRotatedText( self.text, 0, 0, angle, backgroundBrush )
        
    def intersects(self, primitive):
        return True
        
    def _getLocalBoundingBox(self):
        assert not ( (self.active_font is None) and (self.renderer.active_font is None) ), 'Could not get text bounding box, first need to set a font'
        if self.active_font != self.renderer.active_font and self.renderer.active_font:
            w, h = self.renderer.GC.GetTextExtent( self.text )
            size = numpy.array( (w,h) )
            self._localBoundingBox = boundingBoxModule.fromRectangleCenterSize( (0,0), size )

        return self._localBoundingBox

    localBoundingBox = property( _getLocalBoundingBox )
