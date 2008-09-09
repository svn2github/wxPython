import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )
sys.path.append( os.path.abspath( '../misc' ) )

import wx
from floatcanvas.math import numpy

def convertImageToBuffer(img):
    from floatcanvas.math import numpy
    w, h = img.GetWidth(), img.GetHeight()
    img_data = numpy.array( [ord(c) for c in img.GetDataBuffer()], dtype = 'u8' ).reshape( (w, h, 3) )
    if not img.HasAlpha():
        return img_data
    else:
        data = numpy.empty( (w,h,4), 'u8' )
        data[...,:3] = img_data
        data[...,3] = numpy.array( [ord(c) for c in img.GetAlphaBuffer()], dtype = 'u8' ).reshape(w,h)
        return data


def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (1200, 600) )    
    frame.Show()

    dc = wx.ClientDC( frame )
    toucanImg = wx.Image( '../data/toucan.png' )
    import time
    start = time.clock()
    toucanImg = toucanImg.Blur( 5 )
    print 'YYY', time.clock() - start
    toucanData = convertImageToBuffer( toucanImg )
    toucanData = numpy.ascontiguousarray( toucanData, dtype = 'B' )

    def bufferToBitmap( data ):
        w, h, comps = data.shape
        if comps == 4:
            return wx.BitmapFromBufferRGBA( w, h, data )
        elif comps == 3:
            return wx.BitmapFromBuffer( w, h, data )
        else:
            raise

    w, h, components = toucanData.shape
    dc.DrawBitmap( bufferToBitmap( toucanData ), 0, 0, False )

    import floatcanvas.filters
    for i in range(1,4):
        import time
        start = time.clock()
        drunkenToucanData = floatcanvas.filters.gaussian_blur( toucanData, 20, gauss_shape = i )
        print time.clock() - start
        drunkenToucanData = numpy.asarray( drunkenToucanData, dtype = 'B' )
        dc.DrawBitmap( bufferToBitmap( drunkenToucanData ), (i%6) * 200 - 200, i//6 * 200 + 200, False )
    
    app.MainLoop()

    
if __name__ == '__main__':
    start()
