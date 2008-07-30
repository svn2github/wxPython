import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )
sys.path.append( os.path.abspath( '../misc' ) )

import unittest
import wx
from floatcanvas import GCRenderer

from floatcanvas.math import numpy
import math

class WorldData(object):
    def __init__(self):
        from loadWorldData import points, lineLengths

        self.points = points
        self.lineLengths = lineLengths

        self.transform()

    def transform(self):
        centerLong = -190        

        def mercator(x):
            return -numpy.log( numpy.tan( numpy.pi / 4 + x / 2 ) ) + 3

        self.points[::,::2] -= math.radians(centerLong)
        self.points[::,1::2] = mercator( self.points[::,1::2] )
        self.points *= 100
        #print self.points[0:3]

#        self.points[::,1::2] /= 2
#        self.points[::,1::2] += numpy.pi / 4
#        self.points[::,1::2] = numpy.tan( self.points[::,1::2] )
#        self.points[::,1::2] = numpy.log2( self.points[::,1::2] )


class TestNode(unittest.TestCase):
    def setUp(self):
        self.app = wx.App(0)

        self.world = WorldData()
        self.frame = wx.Frame(None, wx.ID_ANY, 'GC Renderer Test', size = (800,600))
        self.frame.Show()        

    def tearDown(self):
        self.frame.Close()

    def testWorldData(self):
        # creation phase
        renderer = GCRenderer( window = self.frame, double_buffered = False )

        black_pen = renderer.CreatePen( wx.Colour(0,0,0,255), width = 1 )
        black_pen.Activate()

        currentPos = 0
        for lineLength in self.world.lineLengths:
            renderer.DrawLines( self.world.points[currentPos:currentPos+lineLength] )
            currentPos += lineLength

        import time
        time.sleep(5)
        
        
        
    
if __name__ == '__main__':
    unittest.main()
