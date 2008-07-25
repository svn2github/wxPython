from renderer import IRenderer, IPath, IBitmap
import wx

class ConstantTable(object):
    stringToWx = { 'oddeven' : wx.ODDEVEN_RULE,
                   'winding' : wx.WINDING_RULE
                 }
    
    def get(cls, string):
        return cls.stringToWx[string]

    get = classmethod(get)


class DoubleBuffer(object):
    def __init__(self, window):
        self.window = window
        self.window.Bind( wx.EVT_SIZE, self.OnSize )
        self.client_dc = wx.ClientDC( self.window )
        self._recreate()
    
    def OnSize(self, event):
        self._recreate()
        
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
        if double_buffered and window and (not window.IsDoubleBuffered()):
            self.double_buffer = MemoryDoubleBuffer( window )
            window = None
            dc = self.dc = self.double_buffer.dc
            
        self.double_buffered = double_buffered

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
        self.GC = getattr(self.renderer, func)( window or dc or native_dinow or native_dc )
        self.transformMatrix = self.CreateMatrix()
        
    def Clear(self):
        if self.double_buffered:
            self.double_buffer.Clear()
    
    def Present(self):
        if self.double_buffered:
            self.double_buffer.Present()

    # transform fucntions
    def SetTransform(self, transform):
        self.transformMatrix.Set( *list(transform.transpose().flat) )
        #self.transformMatrix.Set( transform[0][0], transform[1][0], transform[0][1], transform[1][1] ,transform[0][2], transform[1][2] )
        self.GC.SetTransform( self.transformMatrix )

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
    
    def CreateRectangle(self, *args, **keys):
        path = self.CreatePath()
        path.AddRectangle( *args, **keys )
        return GCRenderObject( self, path )
       
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
    def __init__(self, renderer, colour, *args, **keys):
        self.renderer = renderer
        self.GC = GC = renderer.GC
        self.font = GC.CreateFont( wx.Font(*args, **keys), colour)

    def Activate(self):
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

class GCRenderObject(object):
    transformMethod = 'global'          # 'global' or 'path'

    def __init__(self, renderer, path):
        self.renderer = renderer
        self.path = path
        self._transform = renderer.CreateMatrix()
        self.lastTransform = LinearTransform2D()
        
    def Draw(self):
        if self.transformMethod == 'global':
            self.renderer.SetTransform( self.transform )
        self.path.Draw()
                       
    def GetBoundingBox(self):
        self.path.GetBox()
        
    def _getTransform(self):
        return self._transform
    
    def _setTransform(self, transform):
        method = self.transformMethod
        if method == 'path':
            m = ( transform * self.lastTransform.inverse ).matrix[ :-1, ... ]
            self._transform.Set( *list(m.transpose().flat) )
            self.path.Transform( self._transform )
            self.lastTransform = transform
        elif method == 'global':
            self._transform = transform.matrix[ :-1, ... ]
        else:
            assert False
        
    transform = property( _getTransform, _setTransform )
    
    #boundingBox = property( _getBoundingBox )
        