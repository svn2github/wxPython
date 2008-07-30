import wx
from constantTable import ConstantTable
from buffering import MemoryDoubleBuffer, SingleBuffer
from graphicsObjects import GCPath, GCFont, GCBrush, GCPen, GCBitmap
from renderObjects import GCRenderObjectPath, GCRenderObjectText

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
