import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import wx
from floatcanvas import GCRenderer

class RendererTest(object):
    def run(self):
        self.app = wx.App(0)
        self.frame = wx.Frame(None, wx.ID_ANY, 'GC Renderer Test', size = (800,600))
        self.frame.Show()

        # creation phase
        renderer = GCRenderer( window = self.frame, double_buffered = False )

        renderer.Clear( 'white' )

        black_brush = renderer.CreateBrush( 'plain', 'black' )
        red_brush = renderer.CreateBrush( 'plain', 'red' )

        black_pen = renderer.CreatePen( wx.Colour(0,0,0,255), width = 5 )
        red_pen = renderer.CreatePen( wx.Colour(255,0,0,50), width = 10 )
        red_pen.Activate()

        bmp = wx.BitmapFromImage( wx.Image( '../data/toucan.png' ) )
        
        font = renderer.CreateFont( 14, 'default', 'italic', 'normal', True, 'Arial', 'blue' )
        font.Activate()

        path = renderer.CreatePath()
        vertices = [ (0, 20), (70,35), (99, 46), (235, 11), (555, 555) ]
        path.MoveToPoint( *vertices[0] )
        for v in vertices[1:]:
            path.AddLineToPoint(*v)
                
        # do drawing
        black_brush.Activate()
        red_pen.Activate()
        renderer.DrawEllipse( 100, 100, 50, 80 )
        renderer.DrawLines( [ (0,0), (200,200) ] )

        red_brush.Activate()
        black_pen.Activate()
        path.Stroke()
        
        renderer.DrawRotatedText( 'Hello World!', 50, 300, angle = 30 )
        renderer.DrawBitmap( bmp, 200, 200, 40, 40)

        renderer.Present()

        self.app.MainLoop()
        
        
    
if __name__ == '__main__':
    RendererTest().run()
