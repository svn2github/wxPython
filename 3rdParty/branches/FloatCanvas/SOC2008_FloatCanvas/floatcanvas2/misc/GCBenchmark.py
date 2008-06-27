#!/usr/bin/env python

"""

An attempt at an AlphaLine class using NavCanvas and GraphicsContext

"""

import numpy as N
import sys, wx
import math
import time


def getCirclePoint(t, no_segments, radius, centerX, centerY):
    phi = float(t) / no_segments * 2 * math.pi
    x = math.sin(phi) * radius + centerX
    y = math.cos(phi) * radius + centerY
    return (x,y)

# from http://article.gmane.org/gmane.comp.python.wxpython/52824/match=screenshot 
def TakeScreenShot(rect):
    """ Takes a screenshot of the screen at give pos & size (rect). """

    #Create a DC for the whole screen area
    dcScreen = wx.ScreenDC()

    #Create a Bitmap that will later on hold the screenshot image
    #Note that the Bitmap must have a size big enough to hold the screenshot
    #-1 means using the current default colour depth
    bmp = wx.EmptyBitmap(rect.width, rect.height)

    #Create a memory DC that will be used for actually taking the screenshot
    memDC = wx.MemoryDC()

    #Tell the memory DC to use our Bitmap
    #all drawing action on the memory DC will go to the Bitmap now
    memDC.SelectObject(bmp)

    #Blit (in this case copy) the actual screen on the memory DC
    #and thus the Bitmap
    memDC.Blit( 0, #Copy to this X coordinate
        0, #Copy to this Y coordinate
        rect.width, #Copy this width
        rect.height, #Copy this height
        dcScreen, #From where do we copy?
        rect.x, #What's the X offset in the original DC?
        rect.y  #What's the Y offset in the original DC?
        )

    # draw a white circle in there
    memDC.SetBrush(wx.WHITE_BRUSH )
    memDC.DrawEllipse( rect.x, rect.y, rect.width, rect.height )

    #Select the Bitmap out of the memory DC by selecting a new
    #uninitialized Bitmap
    memDC.SelectObject(wx.NullBitmap)

    return bmp

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (1000, 800)
        kwargs['pos'] = (50,50)
        wx.Frame.__init__(self, *args, **kwargs)

        self.Bind( wx.EVT_PAINT, self.OnPaint )

        return None

    def OnPaint(self, evt):
        self.dc = wx.PaintDC(self)
        self.GC = wx.GraphicsContext.Create(self.dc)

        print 'Starting benchmark...'
        print
        print 'Python platform  : %s' % sys.platform
        try:
            print 'Windows version  : %s' % (sys.getwindowsversion(),)
        except AttributeError:
            pass
        print 'Python version   : %s' % sys.version
        print 'wxPython version : %s' % wx.version()
        print

        self.BenchmarkBitmaps( 200 )

        self.BenchmarkLines(    10, 1000, 50 )
        self.BenchmarkLines( 10000, 1000, 50 )

        self.BenchmarkLines(    10, 1000,  5 )
        self.BenchmarkLines( 10000, 1000,  5 )

        self.Close()

    def BenchmarkBitmaps(self, iterations):
        print 'Benchmark bitmap ( iterations=%d )' % ( iterations, )
        print '-' * 60
        print

        dc = self.dc
        GC = self.GC
        
        bmp = TakeScreenShot( wx.Rect(0,0,500,500) )
        mask = wx.Mask(bmp, wx.WHITE)
        bmp.SetMask( mask )

        # bmp tests
        def measure(func):
            start = time.time()
            for i in range(iterations):
                func(i)                
            difference = time.time() - start
            dc.Clear()
            return difference

        def DrawBitmapTransparent(i):
            GC.DrawBitmap( bmp, i/5.0, i/5.0, bmp.GetWidth() * 1.2, bmp.GetHeight() * 1.1 )

        def DrawBitmapDC(i):
            dc.DrawBitmap( bmp, i/5.0, i/5.0, False )

        def DrawBitmapTransparentDC(i):
            dc.DrawBitmap( bmp, i/5.0, i/5.0, True )

        def do_tests(descr, tests):
            print '\t%ss tests:' % descr
            print '\t' + '-' * 30
            for test in tests:
                print '\tTest %s took %.2f seconds' % (test.__name__, measure(test))
            print

        do_tests( 'GC Bitmap', [ DrawBitmapTransparent ] )
        do_tests( 'DC Bitmap', [ DrawBitmapDC, DrawBitmapTransparentDC ] )

        
    def BenchmarkLines(self, no_segments_per_circle, no_circles, circle_radius):
        print 'Benchmark lines ( segments=%d circles=%d radius=%d )' % (no_segments_per_circle, no_circles, circle_radius)
        print '-' * 60
        print

        dc = self.dc
        GC = self.GC

        ##FIXME: I sure hope there is a better way to create a color!
        c = wx.Color()
        c.SetFromName( 'Red' )
        r,g,b = c.Get()
        c1 = wx.Color(r, g, b, 5)
        c2 = wx.Color(r, g, b, 25)

        no_segments = no_segments_per_circle
        centerX, centerY = 0, 0
        radius = circle_radius
        vertices = [ getCirclePoint(x, no_segments, radius, centerX, centerY) for x in range(no_segments+1) ]

        def CreatePath():
            Path = GC.CreatePath()

            Path.MoveToPoint( *vertices[0] )
            for v in vertices[1:]:
                Path.AddLineToPoint(*v)

            return Path

        start = time.time()
        Path = CreatePath()
        print '\tPath creation time %.2f' % (time.time() - start,)
        print

        #GC.DrawLines( vertices )

        GC.SetPen( wx.Pen( 'Black' ) )
        Brush = GC.CreateRadialGradientBrush(10, 10, 0, 0, radius, c1, c2)

        

        iterations = no_circles
        radius = 200
        centerX, centerY = 500, 400
        transforms = []

        for i in range(0, iterations):
            offsetX, offsetY = getCirclePoint(i, iterations, radius, centerX, centerY)
            t = float(i+1) / iterations
            transform = GC.CreateMatrix( t * 1.7, t, t * 0.8, t * 2.3, offsetX, offsetY )
            #transform = GC.CreateMatrix( 1,0, 0,1, 0,0 )
            transforms.append( transform )


        def measure(func):
            start = time.time()
            for i, transform in enumerate(transforms):
                func(transform)
            difference = time.time() - start

            dc.SetDeviceOrigin( 0, 0 )
            dc.SetUserScale(1,1)
            dc.Clear()
            
            return difference


        def DrawPath(transform):
            GC.SetTransform( transform )
            GC.DrawPath( Path )

        def DrawLines(transform):
            GC.SetTransform( transform )
            GC.DrawLines(vertices)

        def StrokePath(transform):
            GC.SetTransform( transform )
            GC.StrokePath(Path)

        def StrokeLines(transform):
            GC.SetTransform( transform )
            GC.StrokeLines(vertices)

        def FillPath(transform):
            GC.SetTransform( transform )
            GC.FillPath(Path)

        def do_tests(descr, tests):
            print '\t%ss tests:' % descr
            print '\t' + '-' * 30
            for test in tests:
                print '\tTest %s took %.2f seconds' % (test.__name__, measure(test))
            print


        do_tests( 'GC Lines-only', [ DrawPath, DrawLines, StrokePath, StrokeLines ] )
        GC.SetBrush(Brush)
        do_tests( 'GC Fill', [ DrawPath, DrawLines, FillPath ] )

        def DrawLines(transform):
            transform = transform.Get()
            dc.SetUserScale( math.hypot(*transform[:2]), math.hypot(*transform[2:4]) )
            dc.SetDeviceOrigin( *transform[4:] )
            dc.DrawLines(vertices)

        def DrawPolygon(transform):
            transform = transform.Get()
            dc.SetUserScale( math.hypot(*transform[:2]), math.hypot(*transform[2:4]) )
            dc.SetDeviceOrigin( *transform[4:] )
            dc.DrawPolygon(vertices)

        dc.SetPen( wx.BLACK_PEN )
        dc.SetBrush( wx.NullBrush )
        do_tests( 'DC Lines-only', [ DrawLines ] )
        dc.SetBrush( wx.RED_BRUSH )
        do_tests( 'DC Fill', [ DrawPolygon ] )


        
    
A = wx.App(0)
F = MyFrame(None, wx.ID_ANY, 'GC Benchmark')
F.Show()
A.MainLoop()
