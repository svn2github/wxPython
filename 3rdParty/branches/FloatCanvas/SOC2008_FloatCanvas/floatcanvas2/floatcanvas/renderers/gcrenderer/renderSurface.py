import wx
from constantTable import ConstantTable

class RenderSurface(object):
    ''' A render surface is a surface where things can be rendered to and from.
        To accomplish this task it has an associated bitmap and GC.
    '''
    _activeSurfaces = []
    
    def __init__(self, size, renderer, hasAlpha):
        self.renderer = renderer
        self.hasAlpha = hasAlpha
        self.active = False
        self._size = None
        self.size = size
           
    def _setSize(self, size):
        ''' Sets the size. If it changes, recreate the associated bitmap and GC.
        '''
        if size == self._size:
            return
        
        #print size
        self._size = size        
        
    def _getSize(self):
        return self._size
        
    size = property( _getSize, _setSize )
    
    def _getBitmap(self):
        return self._bitmap
    
    bitmap = property( _getBitmap )
        
    def BeginRendering(self):
        # recreate the bitmap if our size changed or there wasn't one created yet
        if not hasattr(self, '_bitmap') or (self._bitmap.GetSize() != self.size):
            self._bitmap = wx.EmptyBitmap(self.size[0], self.size[1], 32)
            if self.hasAlpha:
                self._bitmap.UseAlpha()

        self.dc = wx.MemoryDC( self._bitmap )
        self.gc = self.renderer.wx_renderer.CreateContext( self.dc )
        
    def EndRendering(self):
        del self.dc
        del self.gc

    def Clear(self, background_color):
        ''' Clears the surface with background_color.
            Todo: This does not work properly for surfaces which have an alpha
                    channel, because the DC Clear() methods don't affect the
                    alpha channel at all.
        '''
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
        ''' Activates this surface '''
        RenderSurface._activeSurfaces.append( self )
        self._doActivate()
    
    def Deactivate(self):
        ''' Deactivates this surface. Raises an exception if you are trying
            to deactivate the wrong surface.
        '''
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
        ''' Returns the picture of this surface as a string with file_format.
            where file format can be something like 'png', 'jpg' or 'raw' or any
            other kind of supported image format.
        '''
        if file_format == 'raw':
            if self.bitmap.HasAlpha():
                return wx.AlphaPixelData(self.bitmap).GetPixels().Get()
            else:
                return wx.NativePixelData(self.bitmap).GetPixels().Get()
        
        img = self.bitmap.ConvertToImage()        
        
        import cStringIO
        outputStream = cStringIO.StringIO()
        if file_format == 'jpg':
            file_format = 'jpeg'
        img.SaveStream( wx.OutputStream(outputStream), ConstantTable.getEnum( 'bitmap_type', file_format ) )
        data = outputStream.getvalue()
        outputStream.close()
              
        return data
    
    def _getBitmapPixels(self):
        from ...math import numpy
        comps = 3
        if self.bitmap.HasAlpha():
            comps = 4
       
        from arrayFromImage import arrayFromImage
        img = self.bitmap.ConvertToImage()

        return arrayFromImage( img )
        
    bitmapPixels = property( _getBitmapPixels )