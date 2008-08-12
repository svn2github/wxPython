import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )
sys.path.append( os.path.abspath( '../misc' ) )

import wx
import floatcanvas as fc
#from loadWorldData import points as mapPoints

def convertImageToBuffer(img):
    from floatcanvas.math import numpy
    w, h = img.GetWidth(), img.GetHeight()
    img_data = numpy.array( img.GetDataBuffer(), dtype = 'c' ).reshape( (w, h, 3) )
    if not img.HasAlpha():
        return img_data
    else:
        data = numpy.empty( (w,h,4), 'c' )
        data[...,:3] = img_data
        data[...,3] = numpy.array( img.GetAlphaBuffer(), dtype = 'c' ).reshape(w,h)
        return data
    
def start():
    #  setup very basic window
    app = wx.App(0)
    frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
    frame.Show()
        
    canvas = fc.FloatCanvas( window = frame )
    #canvas.dirty = False
    
    toucanImg = wx.Image( '../data/toucan.png' )
    toucanData = convertImageToBuffer( toucanImg )
    toucanBitmap = wx.BitmapFromImage( toucanImg.AdjustChannels( 0, 2, 0, 1 ) )

    # setup a small list of primitives we want to test
    # the default python syntax for specifying these is more then unpretty
    # so write them down as plain text and parse them
    primitives = '''
        Rectangle             (100, 100)
        Circle                125
        Ellipse               (100, 150)
        RoundedRectangle      (100, 100), 30
        Text                  'wxPython'
        Line                  (0,0), (100,0)
        LineLength            100
        Lines                 [ (0,0), (20, 30), (90, 70), (10, -20) ]
        LineSegments          [ (0,0), (20, 90), (40, 30), (90,  35) ]
        LineSegmentsSeparate  [ (0,0), (40, 30) ], [ (20, 90), (90,35) ]
        Bitmap                toucanData
        Bitmap                toucanBitmap
        Bitmap                toucanData, False
        Arc                   75, 4.5, 1.5, False
        CubicSpline           [ (0,0), (90, 70), (90, 20), (0, 50) ]
        QuadraticSpline       [ (0,0), (20, 50), (80, 0) ]
        Arrow                 (0,0), (40, -20), (20, 10)
        AngleArrow            (0,0), 50, 20, (30, 10)
        # todo: Polygon, PolygonList, LinesList
    '''
    
    # parse the list, generate a list of (kind, args) tuples    
    items = []
    for line in primitives.splitlines():
        line = line.strip()
        if (not line) or line.startswith('#'):
            continue
        kind, args = line.split(None, 1)
        items.append( (kind.strip(), eval('(%s,)' % args)) )
    
    # now actually create the primitives from the (kind, args) tuples
    no_primitives = 100
    i = 0
    while i < no_primitives:
        for kind, sizes in items:
            if kind == 'Text':
                semiTransparentGradientLook = fc.RadialGradientFillLook( (0,0), (0,255,0,128), (0,0), 150, (255,0,255,200) )
                look = fc.TextLook( size = 15, faceName = 'Arial', background_fill_look = semiTransparentGradientLook )
            elif kind == 'Circle':
                look = fc.OutlineLook( line_colour = 'blue', width = 10, style = 'user_dash', dashes = [1,1] )
            else:
                look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
                
            r = canvas.create( kind,  name = 'r%d' % i, pos = (i * 100, 0), look = look, *sizes )
            #r._debugDrawBoundingBoxes = True

            if kind == 'Bitmap' and len(sizes) > 1 and sizes[1] == False:
                r.scale = (100, 100)
            
            i += 1
            if i >= no_primitives:
                break

    #pts = canvas.create( 'Points', mapPoints, name = 'Map', pos = (0, 0), look = ( 'blue', 'red' ), transform = 'Mercator'  )

    # the default cam, looking at 0, 0
    canvas.camera.position = (0, 0)
    canvas.camera.zoom = (1.0, 1.0)
    
    def print_culled_nodes():
        try:
            print 'rendered %d nodes' % ( len(canvas.renderPolicy.renderedNodes), )
            #print r.boundingBox
            #for node in canvas.renderPolicy.renderedNodes:
            #    print node.name
        except AttributeError:
            pass
    
    import math
    animate = True
    if animate:
        import time
        for i in range(0, 600):
            #canvas.camera.rotation = i
            zoom = 0.2 + abs( math.sin(i / 100.0) ) / 5
            canvas.camera.position = (i * 5, 0)
            canvas.camera.zoom = ( zoom, zoom )
            canvas.Render( backgroundColor = 'white' )
            print_culled_nodes()
            #time.sleep(0.01)
        
    wx.CallLater( 1000, print_culled_nodes )
    
    app.MainLoop()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('start()', 'profiling_data_cProfile')
    start()
