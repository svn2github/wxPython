import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import unittest
import wx
from floatcanvas2.gcrenderer import GCRenderer

import numpy
import math
class WorldData(object):
    def __init__(self, filename):
        self.load(filename)

    def load(self, filename):
        f = open(filename, 'r')
        self.points = points = []

        lastStart = 0
        i = 0
        self.lineLengths = lineLengths = []
        for line in f:
            if line.startswith('#'):
                if (i - lastStart) > 0:
                    lineLengths.append(i - lastStart)
                    lastStart = i
                continue
            long, lat = line.split()
            points.append( ( float(long), float(lat) ) )
            i += 1

        self.points = numpy.array( points, dtype = 'float' )
        def radians(x):
            return x * (numpy.pi/180.0)
        self.points = radians(self.points)
        self.save()
        self.transform()

    def save(self):
        import pickle

        f = open( './world2.dat', 'wb' )
        pickle.dump( ( self.points, self.lineLengths ), f, pickle.HIGHEST_PROTOCOL )
        f.close()

        f = open( './worldData.py', 'w' )
        f.write( "import pickle\nf = open('world2.dat', 'rb')\ndata = pickle.load(f)\npoints, lineLengths = data\nf.close()" )
        f.close()


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

        self.world = WorldData( '../../data/world.dat' )
        self.frame = wx.Frame(None, wx.ID_ANY, 'GC Renderer Test', size = (800,600))
        self.frame.Show()        

    def tearDown(self):
        self.frame.Close()

    def testWorldData(self):
        # creation phase
        renderer = GCRenderer( window = self.frame )

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
