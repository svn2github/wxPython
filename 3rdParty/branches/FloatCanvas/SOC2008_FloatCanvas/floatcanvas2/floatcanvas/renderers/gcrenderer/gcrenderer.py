import wx
from constantTable import ConstantTable
from buffering import MemoryDoubleBuffer, SingleBuffer
from graphicsObjects import GCPath, GCFont, GCBrush, GCPen, GCBitmap
from renderObjects import GCRenderObjectPath, GCRenderObjectText, GCRenderObjectBitmap
from renderSurface import RenderSurface

class GCRenderer(object):
    # implements(IRenderer)

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, double_buffered = True):
        if wx_renderer is None:
            wx_renderer = wx.GraphicsRenderer.GetDefaultRenderer()
            
        self.wx_renderer = wx_renderer

        self.double_buffered = double_buffered

        # force drawing to memory for now. This way we can easily switch the bitmap
        # for render to surface operations. if the gc was created with a client dc
        # this is not easily possible
        #if double_buffered and window and (not window.IsDoubleBuffered()):
        if True:
            self.main_render_surface = self.active_render_surface = self.CreateRenderSurface( window.GetClientSizeTuple(), hasAlpha = False )
            self.framebuffer = MemoryDoubleBuffer( window, self.main_render_surface )

            def disable_event(*args,**keys):
                pass            
            window.Bind(wx.EVT_ERASE_BACKGROUND, disable_event)
        else:
            self.framebuffer = SingleBuffer( window )
            
        #window = None
        #dc = self.dc        
        #
        #if window or dc:
        #    func = 'CreateContext'
        #elif native_window:
        #    func = 'CreateContextFromNativeWindow'
        #elif native_dc:
        #    func = 'CreateContextFromNativeContext'
        #else:
        #    raise ValueError('You have to supply exactly one of the window, dc, native_context or native_dc arguments!')

        #self.GC = getattr(self.renderer, func)( window or dc or native_window or native_dc )
        #self.transformMatrix = self.CreateMatrix()
        
        self.active_font = self.active_brush = self.active_pen = None
        self.fill_mode = 'fill_and_line'
        
    def CreateRenderSurface(self, size, hasAlpha):
        rs = RenderSurface( size, self, hasAlpha )
        return rs
        
    def Clear(self, background_color):
        self.framebuffer.Clear( background_color )
    
    def Present(self):
        self.framebuffer.Present()

    def getScreenshot(self, file_format):
        return self.main_render_surface.getData( file_format )

    def _setSize(self, size):
        self.framebuffer.size = size
        
    def _getSize(self):
        return self.framebuffer.size
        
    screen_size = property( _getSize, _setSize )
    
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

    def CreatePen(self, colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None, wx_pen = None ):
        return GCPen(self, colour, width, style, cap, join, dashes, stipple, wx_pen)

    # kind = 'plain', 'linearGradient', 'radialGradient'
    def CreateBrush(self, kind, *args, **keys):
        return GCBrush(self, kind, *args, **keys)

    def CreateFont(self, *args, **keys):
        return GCFont(self, *args, **keys)
    
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

    def CreateArc(self, x, y, r, startAngle, endAngle, clockwise):
        path = self.CreatePath()
        path.AddArc( x, y, r, startAngle, endAngle, clockwise )
        return GCRenderObjectPath( self, path )

    def CreateQuadraticSpline(self, controlPoints):
        path = self.CreatePath()
        if len(controlPoints) != 3:
            raise ValueError( 'controlPoints needs to be of length 3, got %d' % len(controlPoints) )
        path.MoveToPoint( controlPoints[0][0], controlPoints[0][1] )
        path.AddQuadCurveToPoint( controlPoints[1][0], controlPoints[1][1], controlPoints[2][0], controlPoints[2][1] )
        return GCRenderObjectPath( self, path )

    def CreateCubicSpline(self, controlPoints):
        path = self.CreatePath()
        if len(controlPoints) != 4:
            raise ValueError( 'controlPoints needs to be of length 4, got %d' % len(controlPoints) )
        path.MoveToPoint( controlPoints[0][0], controlPoints[0][1] )
        path.AddCurveToPoint( controlPoints[1][0], controlPoints[1][1], controlPoints[2][0], controlPoints[2][1], controlPoints[3][0], controlPoints[3][1] )
        return GCRenderObjectPath( self, path )

    def CreateText(self, *args, **keys):
        return GCRenderObjectText( self, *args, **keys)

    def CreateLinesList(self, lines_list, close = False):
        path = self.CreatePath()
        for line in lines_list:
            points = line
            if len(points) > 0:
                path.MoveToPoint( points[0][0], points[0][1] )
                for pnt in points[1:]:
                    path.AddLineToPoint( pnt[0], pnt[1] )
                if close:
                    path.CloseSubpath()
        return GCRenderObjectPath( self, path)

    def CreateLineSegmentsSeparate(self, startPoints, endPoints):
        path = self.CreatePath()
        if len(startPoints) != len(endPoints):
            raise ValueError( 'number of start and end points must be equal (%s %s)' % (startPoints, endPoints))
        
        for startPoint, endPoint in zip( startPoints, endPoints ):
            path.MoveToPoint( startPoint[0], startPoint[1] )
            path.AddLineToPoint( endPoint[0], endPoint[1] )
            
        return GCRenderObjectPath( self, path)

    def CreateBitmap(self, pixels, use_real_size):
        return GCRenderObjectBitmap( self, pixels, use_real_size )
    
    def CreateCompositeRenderObject(self, subobjects):
        # if all subobjects are path object, then merge the pathes into one
        for subobject in subobjects:
            if not isinstance( subobject, GCRenderObjectPath ):
                raise ValueError( 'All composite subobjects must be path objects!' )
            
        path = self.CreatePath()
        for subobject in subobjects:
            path.AddPath( subobject.path.path )
            
        return GCRenderObjectPath( self, path )
    
    # maps all the other functions
    def __getattr__(self, name):
        if name == 'GC':
            return self.active_render_surface.gc
        return getattr(self.active_render_surface.gc, name)