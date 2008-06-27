import sys
import os.path
sys.path.append( os.path.abspath( '../..' ) )

import unittest
import numpy
from floatcanvas2.transform import LinearTransform, ArbitraryTransform, MercatorTransform, ThreeDProjectionTransform

class TestNode(unittest.TestCase):
    def setUp(self):
        self.coords2d = numpy.array( [ (0,0), (2,0), (2,2), (0,2) ] )
        self.coords3d = numpy.array( [ (0,0,0), (2,0,0), (2,2,0), (0,2,0) ] )
    
    
    def testLinear(self):
        t = LinearTransform()
        self.assert_( t.translation.tolist() == t.position.tolist() == t.pos.tolist() == [0,0], t.pos )
        self.assert_( t.scale.tolist() == [1,1], t.scale )
        t.pos = (5, 5)
        self.assert_( t.translation.tolist() == t.position.tolist() == t.pos.tolist() == [5,5], t.pos )
        self.assert_( t.scale.tolist() == [1,1], t.scale )
        t.scale = (2, 3)
        self.assert_( t.scale.tolist() == [2,3], t.scale )
        self.assert_( t.translation.tolist() == t.position.tolist() == t.pos.tolist() == [5,5], t.pos )
        self.assert_( t.matrix.tolist() == [ [2,0,0], [0,3,0], [5,5,1] ], t.matrix )

        tc = t.transform( self.coords2d )
        self.assert_( tc.tolist() == [ [5,5], [9,5], [9,11], [5,11] ], tc )

    def testArbitrary(self):
        def double(x):
            return x * 2
        t = ArbitraryTransform( double )
        tc = t.transform( self.coords2d )
        self.assert_( tc.tolist() == [ [0,0], [4,0], [4,4], [0,4] ], tc )        

    def testMercator(self):
        t = MercatorTransform(0)
        tc = t.transform( self.coords2d )
    
    def test3D(self):
        t = ThreeDProjectionTransform( 800, 600, 90, 1, 100 )
        tc = t.transform( self.coords3d )

    def testConcat(self):
        t1 = LinearTransform()
        t1.pos = (5, 3)
        t2 = LinearTransform()
        t2.pos = (5, 3)
        self.assert_( (t1 * t2).pos.tolist() == [10,6] )

    def testInverse(self):
        t = LinearTransform()
        t.pos = (5, 3)
        t.scale = (2,2)

        self.assert_( numpy.allclose( t.inverse.matrix, [ [0.5,0,0], [0,0.5,0], [-2.5,-1.5,1] ]), t.inverse.matrix )

    def testSpeed(self):
        # run world_test to generate world2.dat if not present

        tl = LinearTransform()
        tl.scale = (2,3)
        tl.pos = (5,5)

        tm = MercatorTransform(0)

        import worldData

        def doTransform():
            tl.transform( worldData.points )
            tm.transform( worldData.points )

        import time
        iterations = 100
        start = time.time()
        for i in range(0,iterations):
            doTransform()
        print (time.time() - start) / iterations / 2

if __name__ == '__main__':
    unittest.main()
