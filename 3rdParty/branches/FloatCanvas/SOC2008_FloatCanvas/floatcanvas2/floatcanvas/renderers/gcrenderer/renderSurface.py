import wx
from constantTable import ConstantTable

class RenderSurface(object):
    _activeSurfaces = []
    
    def __init__(self, size, renderer, hasAlpha):
        self.renderer = renderer
        self.hasAlpha = hasAlpha
        self.active = False
        self._size = None
        self.size = size
           
    def _setSize(self, size):
        if size == self._size:
            return
        
        #print size
        w, h = self._size = size
        self._bitmap = wx.EmptyBitmap(w, h, 32)
        if self.hasAlpha:
            self._bitmap.UseAlpha()
        
        self.dc = wx.MemoryDC( self._bitmap )
        self.gc = self.renderer.wx_renderer.CreateContext( self.dc )
        
        
    def _getSize(self):
        return self._size
        
    size = property( _getSize, _setSize )
    
    def _getBitmap(self):
        return self._bitmap
    
    bitmap = property( _getBitmap )
        
    def Clear(self, background_color):
        if background_color:
            backgroundBrush = wx.Brush( background_color, style = wx.SOLID )
        else:
            backgroundBrush = wx.NullBrush
        
        self.dc.SetBackground( backgroundBrush )
        self.dc.Clear()
        if self.hasAlpha:
            print 'Warning, alpha channel not cleared because of performance'
        #for pixel in wx.AlphaPixelData( self._bitmap ):
        #    values = pixel.Get()[0:3] + (255, )
        #    pixel.Set( *values )

    def Activate(self):
        RenderSurface._activeSurfaces.append( self )
        self._doActivate()
    
    def Deactivate(self):
        try:
            lastSurface = RenderSurface._activeSurfaces.pop()
        except IndexError:
            raise Exception( 'Cannot deactivate the last active render surface' )
            return
        
        if lastSurface != self:
            raise Exception( 'You need to deactivate render surfaces in "stack" order' )
        
        self.active = False
        
        try:
            prev_surface = RenderSurface._activeSurfaces[-1]
        except IndexError:
            # we're the last active surface
            pass
        else:
            prev_surface._doActivate()
            
    def _doActivate(self):
        self.renderer.active_render_surface = self
        self.active = True
 
    def getData(self, file_format):
        if file_format == 'raw':     
            return wx.NativePixelData(self.bitmap).GetPixels().Get()
        
        img = self.bitmap.ConvertToImage()        
        
        import cStringIO
        outputStream = cStringIO.StringIO()
        img.SaveStream( wx.OutputStream(outputStream), ConstantTable.getEnum( 'bitmap_type', file_format ) )
        data = outputStream.getvalue()
        outputStream.close()
              
        return data