import wx
from constantTable import ConstantTable

class RenderSurface(object):
    _activeSurfaces = []
    
    def __init__(self, size, renderer):
        self.renderer = renderer
        self.active = False
        self._size = None
        self.size = size
           
    def _setSize(self, size):
        if size == self._size:
            return
        
        #print size
        w, h = self._size = size
        self._bitmap = wx.EmptyBitmap(w, h, 32)
        
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
        # todo: fixme: Now for the weirdest call of all...
        self.bitmap.UseAlpha()
        
        #self._trash = wx.EmptyBitmap(1, 1, 32)
        #self.dc.SelectObject( self._trash )
        
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
        
        pixelData = wx.AlphaPixelData(self.bitmap)
        alphaData = ''
        for pixel in pixelData:
            alphaData += chr( pixel.Get()[3] )
        img.SetAlphaData( alphaData )
        
        import cStringIO
        outputStream = cStringIO.StringIO()
        img.SaveStream( wx.OutputStream(outputStream), ConstantTable.getEnum( 'bitmap_type', file_format ) )
        data = outputStream.getvalue()
        outputStream.close()
               
        return data