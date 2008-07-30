from renderer import IRenderer, IPath, IBitmap
import wx

class ConstantTable(object):
    stringToWx = { 'oddeven' : wx.ODDEVEN_RULE,
                   'winding' : wx.WINDING_RULE,
                 }
    
    def get(cls, string):
        return cls.stringToWx[string]
    
    get = classmethod(get)

    def getEnum(cls, kind, value):
        enum_name = '%s_%s' % (kind.upper(), value.upper())
        return getattr(wx, enum_name)

    getEnum = classmethod(getEnum)


class SingleBuffer(object):
    def __init__(self, window):
        self.window = window
        self.client_dc = self.dc = wx.ClientDC( self.window )
    
    def Present(self):
        pass

    def Clear(self):
        self.dc.Clear()

class DoubleBuffer(object):
    def __init__(self, window):
        self.window = window
        self.window.Bind( wx.EVT_SIZE, self.OnSize )
        self.client_dc = wx.ClientDC( self.window )
        self._recreate()
    
    def OnSize(self, event):
        self._recreate()
        event.Skip()
        
    def _recreate(self):
        raise NotImplementedError()
    
    def Present(self):
        pass

    def Clear(self):
        self.dc.Clear()

# some double buffer info: http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing
# also see wxAutoBufferedPaintDC (not mentioned in the wiki)
class NativeDoubleBuffer(DoubleBuffer):
    def _recreate(self):
        w, h = self.window.GetClientSizeTuple()
        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
        self.dc = wx.BufferedDC( self.client_dc, self._doubleBufferBitmap, wx.BUFFER_VIRTUAL_AREA  )
        
class MemoryDoubleBuffer(DoubleBuffer):
    def __init__(self, window):
        self.dc = self.memory_dc = wx.MemoryDC()
        DoubleBuffer.__init__( self, window )

    def _recreate(self):
        w, h = self.size = self.window.GetClientSizeTuple()
        self._doubleBufferBitmap = wx.EmptyBitmap(w, h)
        self.dc.SelectObject(self._doubleBufferBitmap)
        
    def Present(self):
        self.client_dc.Blit(0, 0, self.size[0], self.size[1], self.memory_dc, 0, 0)        


class GCRenderer(object):
    # implements(IRenderer)

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, double_buffered = True):
        self.double_buffered = double_buffered

        if double_buffered and window and (not window.IsDoubleBuffered()):
            self.draw_buffer = MemoryDoubleBuffer( window )

            def disable_event(*args,**keys):
                pass            
            window.Bind(wx.EVT_ERASE_BACKGROUND, disable_event)
        else:
            self.draw_buffer = SingleBuffer( window )
            
        window = None
        dc = self.draw_buffer.dc

        if window or dc:
            func = 'CreateContext'
        elif native_window:
            func = 'CreateContextFromNativeWindow'
        elif native_dc:
            func = 'CreateContextFromNativeContext'
        else:
            raise ValueError('You have to supply exactly one of the window, dc, native_context or native_dc arguments!')

        if wx_renderer is None:
            renderer = wx.GraphicsRenderer.GetDefaultRenderer()
            
        self.renderer = renderer
        self.GC = getattr(self.renderer, func)( window or dc or native_window or native_dc )
        self.transformMatrix = self.CreateMatrix()
        
        self.active_font = self.active_brush = self.active_pen = None
        
    def Clear(self):
        self.draw_buffer.Clear()
    
    def Present(self):
        self.draw_buffer.Present()

    # transform fucntions
    #def SetTransform(self, transform):
    #    self.transformMatrix.Set( *list(transform.transpose().flat) )
    #    #self.transformMatrix.Set( transform[0][0], transform[1][0], transform[0][1], transform[1][1] ,transform[0][2], transform[1][2] )
    #    self.GC.SetTransform( self.transformMatrix )

    # line functions
    def DrawLines(self, points, fillStyle = 'oddeven'):
        return self.GC.DrawLines(points, ConstantTable.get(fillStyle) )

    # factory functions
    def CreatePath(self):
        return GCPath(self)

    def CreateBitmap(self, bmp):
        return GCBitmap(self, bmp)

    def CreatePen(self, colour, **keys ):
        return GCPen(self, colour, **keys)

    # kind = 'plain', 'linearGradient', 'radialGradient'
    def CreateBrush(self, kind, *args, **keys):
        return GCBrush(self, kind, *args, **keys)

    def CreateFont(self, *args, **keys):
        return GCFont(self, *args, **keys)
    
    # render object creators
    def _getRenderObject(self, func_name, *args, **keys):
        path = self.CreatePath()
        getattr( path, func_name )( *args, **keys )
        return GCRenderObjectPath( self, path )
    
    # primitives support by GC:
    # Text, RotatedText, Bitmap, Icon, Line, Lines, LineSegments, Rectangle, Ellipse, RoundedRectangle, Curve, QuadCurve, Arc
    def CreateRenderObject(self, kind, *args, **keys):
        return self._getRenderObject( 'Add%s' % kind, *args, **keys )

    def CreateRectangle(self, x, y, w, h):
        path = self.CreatePath()
        path.AddRectangle( x, y, w, h )
        return GCRenderObjectPath( self, path )

    def CreateRoundedRectangle(self, x, y, w, h, radius):
        path = self.CreatePath()
        path.AddRoundedRectangle( x, y, w, h, radius )
        return GCRenderObjectPath( self, path )

    def CreateEllipse(self, x, y, w, h):
        path = self.CreatePath()
        path.AddEllipse( x, y, w, h )
        return GCRenderObjectPath( self, path )

    def CreateText(self, *args, **keys):
        return GCRenderObjectText( self, *args, **keys)

    def CreateListRenderObject(self, kind, offsets, x, y, w, h):
        path = self.CreatePath()
        for offset in offsets:
            path.AddRectangle( x[0] + offset[0], y[0] + offset[0], w, h )
        return GCRenderObjectText( self, *args, **keys)



    # maps all the other functions
    def __getattr__(self, name):
        return getattr(self.GC, name)
    


class GCPath(object):
    # implements(IPath)
    
    def __init__(self, renderer):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.path = GC.CreatePath()

    def Draw(self, fillStyle = 'oddeven'):
        return self.GC.DrawPath(self.path, ConstantTable.get(fillStyle) )
    
    def Fill(self, fillStyle = 'oddeven'):
        return self.GC.DrawPath(self.path, ConstantTable.get(fillStyle) )    

    def Stroke(self):
        return self.GC.StrokePath(self.path)

    # maps all the other functions
    def __getattr__(self, name):
        return getattr(self.path, name)


class GCFont(object):
    def __init__(self, renderer, size, family, style, weight, underlined, faceName, colour):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        family = ConstantTable.getEnum( 'fontfamily', family)
        style = ConstantTable.getEnum( 'fontstyle', style)
        weight = ConstantTable.getEnum( 'fontweight', weight)
        font = wx.Font( size, family, style, weight, underlined, faceName )
        self.font = GC.CreateFont( font, colour )

    def Activate(self):
        if self.renderer.active_font == self:
            return
        self.renderer.active_font = self
        self.GC.SetFont(self.font)


class GCBrush(object):
    def __init__(self, renderer, kind, *args, **keys):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.kind = kind
        if kind == 'plain':
            brush = GC.CreateBrush( wx.Brush( *args, **keys ) )
        elif kind == 'linearGradient':
            brush = GC.CreateLinearGradientBrush( *args, **keys )
        elif kind == 'radialGradient':
            brush = GC.CreateRadialGradientBrush( *args, **keys )
        elif kind is None:
            brush = GC.CreateBrush( wx.NullBrush )
        else:
            raise ValueError('Wrong kind for brush %s' % kind)

        self.brush = brush

    def Activate(self):
        if self.renderer.active_brush == self:
            return
        self.renderer.active_brush = self
        self.GC.SetBrush(self.brush)

class GCPen(object):
    def __init__(self, renderer, colour, **keys):
        # keys: width = 1, style = 'solid', stipple_bmp = None, cap = 'round', dashes = None, join = 'round', pen = None        

        self.renderer = renderer
        self.GC = GC = renderer.GC
        
        if 'pen' in keys:
            pen = keys['pen']
            del keys['pen']
        else:
            pen = wx.Pen(colour)
            
        for name, value in keys.iteritems():
            getattr( pen, 'Set%s' % (name.capitalize(),))( value )

        self.pen = GC.CreatePen( pen )

    def Activate(self):
        if self.renderer.active_pen == self:
            return
        self.renderer.active_pen = self
        self.GC.SetPen(self.pen)
                

class GCBitmap(object):
    # implements (IBitmap)

    def __init__(self, renderer, bmp):
        self.renderer = renderer
        self.GC = renderer.GC
        #self.bitmap = renderer.CreateBitmap()
        self.bmp = bmp

    def Draw(self, x, y, w, h):
        self.GC.DrawBitmap(self.bmp, x, y, w, h)


from transform import LinearTransform2D
import boundingBox as boundingBoxModule
import numpy

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
