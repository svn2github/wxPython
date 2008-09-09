''' Tests bounding boxes with NodeWithBounds and various transformations '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )

import unittest
from floatcanvas.math import numpy
from floatcanvas.canvas import FloatCanvas
from floatcanvas.looks import SolidColourLook

import wx

class TestNode(unittest.TestCase):    
    def testRectangleBounds(self):
        app = wx.App(0)
        frame = wx.Frame( None, wx.ID_ANY, 'FloatCanvas2 demo', size = (800, 600) )
        frame.Show()
            
        canvas = FloatCanvas( window = frame )
    
        r1 = canvas.create( 'Rectangle', (100, 100), look = SolidColourLook( line_colour = 'blue', fill_colour = 'red' )  )
        self.assert_( r1.localBoundingBox.Size == (100, 100), r1.localBoundingBox.Size )
        self.assert_( r1.localBoundingBox.center == (0, 0), r1.localBoundingBox.center )
        self.assert_( r1.boundingBox.Size == (100, 100), r1.boundingBox.Size )
        self.assert_( r1.boundingBox.center == (0, 0), r1.boundingBox.center )
        
        r1.transform.position = (50, 50)
        #r1.view.transform = r1.transform
        #r1.view.rebuild()
        self.assert_( r1.localBoundingBox.Size == (100, 100), r1.localBoundingBox.Size )
        self.assert_( r1.localBoundingBox.center == (0, 0), r1.localBoundingBox.center )
        self.assert_( r1.boundingBox.Size == (100, 100), r1.boundingBox.Size )
        self.assert_( r1.boundingBox.center == (50, 50), r1.boundingBox.center )
        
        r1.transform.scale = (2, 1)
        #r1.view.transform = r1.transform
        self.assert_( r1.localBoundingBox.Size == (100, 100), r1.localBoundingBox.Size )
        self.assert_( r1.localBoundingBox.center == (0, 0), r1.localBoundingBox.center )
        self.assert_( r1.boundingBox.Size == (200, 100), r1.boundingBox.Size )
        self.assert_( r1.boundingBox.center == (50, 50), r1.boundingBox.center )

        r1.transform.rotation = 45
        #r1.view.transform = r1.transform
        self.assert_( r1.localBoundingBox.Size == (100, 100), r1.localBoundingBox.Size )
        self.assert_( r1.localBoundingBox.center == (0, 0), r1.localBoundingBox.center )
        self.assert_( (abs(r1.boundingBox.Size - (141.42, 141.42)) < (0.1, 0.1)).all(), r1.boundingBox.Size )
        self.assert_( r1.boundingBox.center == (50, 50), r1.boundingBox.center )
        
        # todo: recursiveBoundingBox tests

        frame.Close()
        
if __name__ == '__main__':
    unittest.main()
