from ...math import LinearTransform2D, numpy
from ...math import boundingBox as boundingBoxModule
import wx

class GCRenderObjectBase(object):
    ''' Base class for a "render object" which is an object with a
        wxGraphicsMatrix that can be drawn.
    '''
    
    def __init__(self, renderer):
        self.renderer = renderer
        self._rendererTransform = renderer.CreateMatrix()
        self._transform = LinearTransform2D()
        
    def Draw(self, camera):
        self._rendererTransform.Set( *list( (camera.viewTransform * self.transform).matrix[ :-1, ... ].transpose().flat) )
        self.renderer.SetTransform( self._rendererTransform )
        self.DoDraw( camera )
        
        #self.renderer.SwitchToGreyscale()
        
        #self.DoDraw( camera )
                                     
    def _getTransform(self):
        return self._transform
    
    def _setTransform(self, transform):
        self._rendererTransform.Set( *list(transform.matrix[ :-1, ... ].transpose().flat) )
        self._transform = transform
        
    transform = property( _getTransform, _setTransform )    
   
    
class GCRenderObjectPath(GCRenderObjectBase):
    ''' A path render object. Draws a path graphics object and knows hot to get
        its bounding box and perform an intersection test with a point.
    '''
    boundingBoxDependentOnLook = False

    def __init__(self, renderer, path):
        GCRenderObjectBase.__init__(self, renderer)
        self.path = path

        x, y, w, h = self.path.GetBox()
        corner = numpy.array( (x,y) )
        size = numpy.array( (w,h) )
        self._localBoundingBox = boundingBoxModule.fromRectangleCornerSize( corner, size )
        
    def DoDraw(self, camera):
        ''' Just draws the path '''
        #GCRenderObjectBase.Draw(self, camera)
        self.path.Render()
        
    def intersects(self, primitive):
        ''' Returns true if the primitive - which must be a point - is inside
            the path.
        '''
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
    ''' A text render object. Draws a text object and knows hot to get
        its bounding box and perform an intersection test with a point.
    '''
    boundingBoxDependentOnLook = True

    def __init__(self, renderer, text):
        GCRenderObjectBase.__init__(self, renderer)
        self.text = text
        self.active_font = None
        self._localBoundingBox = boundingBoxModule.BoundingBox( ( (0,0), (0,0) ) )
        
    def DoDraw(self, camera):
        #GCRenderObjectBase.Draw(self, camera)

        offset = self.localBoundingBox.min
        if self.renderer.active_brush is not None:
            backgroundBrush = self.renderer.active_brush.brush
        else:
            backgroundBrush = wx.NullGraphicsBrush
        self.renderer.GC.DrawText( self.text, offset[0], offset[1], backgroundBrush )
        #angle = 0
        #self.renderer.GC.DrawRotatedText( self.text, 0, 0, angle, backgroundBrush )
        
    def intersects(self, primitive):
        return True
        
    def _getLocalBoundingBox(self):
        assert not ( (self.active_font is None) and (self.renderer.active_font is None) ), 'Could not get text bounding box, first need to set a font'
        if self.active_font != self.renderer.active_font and self.renderer.active_font:
            w, h = self.renderer.measuringContext.GetTextExtent( self.text )
            size = numpy.array( (w,h) )
            self._localBoundingBox = boundingBoxModule.fromRectangleCenterSize( (0,0), size )

        return self._localBoundingBox

    localBoundingBox = property( _getLocalBoundingBox )


class GCRenderObjectBitmap(GCRenderObjectBase):
    ''' A bitmap render object. Draws a bitmap object and knows hot to get
        its bounding box and perform an intersection test with a point.
    '''
    boundingBoxDependentOnLook = False

    def __init__(self, renderer, pixels, use_real_size):
        GCRenderObjectBase.__init__(self, renderer)
        self.pixels = pixels
        self.use_real_size = use_real_size
        
        if isinstance( pixels, wx.Bitmap ):
            self.bitmap = pixels
            w, h = pixels.GetWidth(), pixels.GetHeight()
        else:
            w, h, components = pixels.shape
    
            pixels = numpy.ascontiguousarray(pixels, dtype = 'B' )
 
            if components == 3:
                self.bitmap = wx.BitmapFromBuffer(w, h, pixels )
            elif components == 4:
                self.bitmap = wx.BitmapFromBufferRGBA(w, h, pixels)
            else:
                raise ValueError( 'pixels must be a 2d-array where each pixel has either 3 (RGB) or 4 (RGBA) components' )
        
        if not use_real_size:
            w, h = 1, 1

        self.width, self.height = w, h        
        self._localBoundingBox = boundingBoxModule.fromRectangleCenterSize( (0,0), numpy.array( (w, h) ) )
        
    def DoDraw(self, camera):
        #GCRenderObjectBase.Draw(self, camera)

        offset = self.localBoundingBox.min
        self.renderer.GC.DrawBitmap( self.bitmap, offset[0], offset[1], self.width, self.height )
        
    def intersects(self, primitive):
        return True
        
    def _getLocalBoundingBox(self):
        return self._localBoundingBox

    localBoundingBox = property( _getLocalBoundingBox )
