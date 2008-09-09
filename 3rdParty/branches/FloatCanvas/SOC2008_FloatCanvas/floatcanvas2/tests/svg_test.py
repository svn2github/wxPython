import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.nodes import Node, TextTreeFormatVisitor, FindNodesByNamesVisitor, GetNodesAsFlatListVisitor
from floatcanvas.nodes import NodeWithTransform
from floatcanvas import NodeWithTransform, MercatorTransform, LinearAndArbitraryCompoundTransform, LinearTransform2D
from floatcanvas.canvas.observables import ObservableRectangle, ObservableDefaultRenderableNode
from floatcanvas.serialization import Serializer, defaultSerializers
import floatcanvas as fc
import wx

class TestNode(unittest.TestCase):
    def testExportRenderableNodeWithModelAndView(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
        r = canvas.create( 'Rectangle', (100, 100), look = look  )

        canvas.serialize( 'svg' )
        canvas.serializeToFile( 'rectangle.svg' )


    def testExportLots(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        look = fc.SolidColourLook( line_colour = 'blue', fill_colour = 'red' )
        rects = []
        for i in range(0, 100):
            r = canvas.create( 'Rectangle', (100, 100), pos = (i * 50, 0), look = look, name = 'rectangle %d' % i  )
            rects.append(r)
            
        rects[5].shown = False
        rects[6].shown = False

        canvas.serializeToFile( 'test_lots.svg' )
        

    def testLooks(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )

        looks = \
        [
            # some looks
            fc.RadialGradientLook( 'red', (0,0), 'red', (0,0), 50, 'yellow' ),
            fc.LinearGradientLook( 'purple', (0,0), 'white', (50,50), 'pink' ),
            fc.OutlineLook( line_colour = 'blue', width = 10, style = 'user_dash', dashes = [1,1] ),
            fc.SolidColourLook( line_colour = 'green', fill_colour = 'red' ),        
    
            # no lines and some transparent colors
            fc.RadialGradientLook( None, (0,0), (0,255,255,128), (0,0), 50, (255,255,255,0) ),
            fc.LinearGradientLook( None, (-50,-50), (0,0,255,255), (50,50), (128,128,255,0) ),
            fc.SolidColourLook( line_colour = None, fill_colour = 'red' ),        
            fc.SolidColourLook( line_colour = 'green', fill_colour = None ),
            
            # some more exotic lines
            fc.RadialGradientLook( 'pink', (0,0), (0,255,0,128), (0,0), 150, (255,0,255,200), line_style = 'dot', line_width = 10, line_cap = 'butt', line_join = 'bevel' ),
            fc.LinearGradientLook( 'red', (-5,-5), 'orange', (5,5), 'blue', line_style = 'long_dash', line_width = 5 ),
            fc.SolidColourLook( line_colour = 'green', fill_colour = 'red', line_style = 'solid', line_width = 13, line_cap = 'projecting', line_join = 'miter' ),        
            fc.SolidColourLook( line_colour = 'black', fill_colour = 'red', line_style = 'solid', line_width = 13, line_cap = 'projecting', line_join = 'round' ),        
        ]
        
        thingy = [ (0,50), (50,0), (-50,0), (0, -50) ]
        
        # create 1000 rectangles
        for i in range(0, len(looks)):
            look = looks[ i % len(looks) ]
            r = canvas.create( 'Rectangle', (100, 100), name = 'r%d' % i, pos = (i * 110, 0), look = look  )
            rr = canvas.create( 'RoundedRectangle', (100, 100), 30, name = 'rr%d' % i, pos = (i * 110, 200), look = look  )
            c = canvas.create( 'Circle', 50, name = 'c%d' % i, pos = (i * 110, 400), look = look  )
            e = canvas.create( 'Ellipse', (100, 75), name = 'e%d' % i, pos = (i * 110, 600), look = look  )
            l = canvas.create( 'Lines', thingy, name = 'l%d' % i, pos = (i * 110, 800), look = look  )
            p = canvas.create( 'Polygon', thingy, name = 'r%d' % i, pos = (i * 110, 1000), look = look  )
            a = canvas.create( 'Arc', 50, 0, 2.14, False, name = 'a%d' % i, pos = (i * 110, 1200), look = look  )
            #r._debugDrawBoundingBoxes = True
    
        # the default cam, looking at 0, 0
        canvas.camera.position = (600, 500)
        canvas.camera.zoom = (0.4, 0.4)
        
        canvas.zoomToExtents()
        
        canvas.serializeToFile( 'test_look.svg' )
        
    def testPrimitives(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = fc.FloatCanvas( window = frame )
    
        toucanImg = wx.Image( '../data/toucan.png' )
        toucanData = fc.arrayFromImage( toucanImg )
        toucanBitmap = wx.BitmapFromImage( toucanImg.AdjustChannels( 0, 2, 0, 1 ) )
    
        # setup a small list of primitives we want to test
        # the default python syntax for specifying these is more then unpretty
        # so write them down as plain text and parse them
        primitives = '''
            Rectangle             (100, 100)
            Circle                62.5
            Ellipse               (100, 150)
            RoundedRectangle      (100, 100), 30
            Text                  'wxPython'
            Line                  (0,0), (100,0)
            LineLength            100
            Lines                 [ (0,0), (20, 30), (90, 70), (10, -20) ]
            LinesList             [ [(146, 399), (163, 403), (170, 393), (169, 391), (166, 386), (170, 381), (170, 371), (170, 355), (169, 346), (167, 335), (170, 329), (170, 320), (170, 310), (171, 301), (173, 290), (178, 289), (182, 287), (188, 286), (190, 286), (192, 291), (194, 296), (195, 305), (194, 307), (191, 312), (190, 316), (190, 321), (192, 331), (193, 338), (196, 341), (197, 346), (199, 352), (198, 360), (197, 366), (197, 373), (196, 380), (197, 383), (196, 387), (192, 389), (191, 392), (190, 396), (189, 400), (194, 401), (201, 402), (208, 403), (213, 402), (216, 401), (219, 397), (219, 393), (216, 390), (215, 385), (215, 379), (213, 373), (213, 365), (212, 360), (210, 353), (210, 347), (212, 338), (213, 329), (214, 319), (215, 311), (215, 306), (216, 296), (218, 290), (221, 283), (225, 282), (233, 284), (238, 287), (243, 290), (250, 291), (255, 294), (261, 293), (265, 291), (271, 291), (273, 289), (278, 287), (279, 285), (281, 280), (284, 278), (284, 276), (287, 277), (289, 283), (291, 286), (294, 291), (296, 295), (299, 300), (301, 304), (304, 320), (305, 327), (306, 332), (307, 341), (306, 349), (303, 354), (301, 364), (301, 371), (297, 375), (292, 384), (291, 386), (302, 393), (324, 391), (333, 387), (328, 375), (329, 367), (329, 353), (330, 341), (331, 328), (336, 319), (338, 310), (341, 304), (341, 285), (341, 278), (343, 269), (344, 262), (346, 259), (346, 251), (349, 259), (349, 264), (349, 273), (349, 280), (349, 288), (349, 295), (349, 298), (354, 293), (356, 286), (354, 279), (352, 268), (352, 257), (351, 249), (350, 234), (351, 211), (352, 197), (354, 185), (353, 171), (351, 154), (348, 147), (342, 137), (339, 132), (330, 122), (327, 120), (314, 116), (304, 117), (293, 118), (284, 118), (281, 122), (275, 128), (265, 129), (257, 131), (244, 133), (239, 134), (228, 136), (221, 137), (214, 138), (209, 135), (201, 132), (192, 130), (184, 131), (175, 129), (170, 131), (159, 134), (157, 134), (160, 130), (170, 125), (176, 114), (176, 102), (173, 103), (172, 108), (171, 111), (163, 115), (156, 116), (149, 117), (142, 116), (136, 115), (129, 115), (124, 115), (120, 115), (115, 117), (113, 120), (109, 122), (102, 122), (100, 121), (95, 121), (89, 115), (87, 110), (82, 109), (84, 118), (89, 123), (93, 129), (100, 130), (108, 132), (110, 133), (110, 136), (107, 138), (105, 140), (95, 138), (86, 141), (79, 149), (77, 155), (81, 162), (90, 165), (97, 167), (99, 171), (109, 171), (107, 161), (111, 156), (113, 170), (115, 185), (118, 208), (117, 223), (121, 239), (128, 251), (133, 259), (136, 266), (139, 276), (143, 290), (148, 310), (151, 332), (155, 348), (156, 353), (153, 366), (149, 379), (147, 394), (146, 399)], [(156, 141), (165, 135), (169, 131), (176, 130), (187, 134), (191, 140), (191, 146), (186, 150), (179, 155), (175, 157), (168, 157), (163, 157), (159, 157), (158, 164), (159, 175), (159, 181), (157, 191), (154, 197), (153, 205), (153, 210), (152, 212), (147, 215), (146, 218), (143, 220), (132, 220), (125, 217), (119, 209), (116, 196), (115, 185), (114, 172), (114, 167), (112, 161), (109, 165), (107, 170), (99, 171), (97, 167), (89, 164), (81, 162), (77, 155), (81, 148), (87, 140), (96, 138), (105, 141), (110, 136), (111, 126), (113, 129), (118, 117), (128, 114), (137, 115), (146, 114), (155, 115), (158, 121), (157, 128), (156, 134), (157, 136), (156, 136)] ]
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
            Polygon               [ (0,0), (20, 30), (90, 70), (10, -20) ]
            PolygonList           [ [ (0,5), (50, 50), (5,0) ], [ (0,-5), (50, -50), (5,0) ], [ (0,-5), (-50, -50), (-5,0) ], [ (0,5), (-50, 50), (-5,0) ] ]
            # todo: none
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
        canvas.camera.position = (1000, 0)
        canvas.camera.zoom = (0.35, 0.35)
        
        canvas.serializeToFile( 'test_primitives.svg' )
        
        
if __name__ == '__main__':
    unittest.main()
