import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import unittest
import wx
from floatcanvas2.gcrenderer import GCRenderer

class TestNode(unittest.TestCase):
    def setUp(self):
        self.app = wx.App(0)
        self.frame = wx.Frame(None, wx.ID_ANY, 'GC Renderer Test', size = (800,600))
        self.frame.Show()

    def tearDown(self):
        self.frame.Close()

    def testSome(self):
        # creation phase
        renderer = GCRenderer( window = self.frame )

        black_brush = renderer.CreateBrush( 'plain', 'black' )
        red_brush = renderer.CreateBrush( 'plain', 'red' )

        black_pen = renderer.CreatePen( wx.Colour(0,0,0,255), width = 5 )
        red_pen = renderer.CreatePen( wx.Colour(255,0,0,50), width = 10 )
        red_pen.Activate()

        bmp = wx.BitmapFromImage( wx.Image( 'toucan.png' ) )
        bmp = renderer.CreateBitmap( bmp )
        
        font = renderer.CreateFont( 'blue', 14, wx.FONTFAMILY_DEFAULT , wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, True )
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
        bmp.Draw( 200, 200, 40, 40)

        import time
        time.sleep(5)
        
        
        
    
if __name__ == '__main__':
    unittest.main()
