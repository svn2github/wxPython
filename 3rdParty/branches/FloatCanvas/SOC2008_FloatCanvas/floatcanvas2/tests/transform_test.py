''' Tests the math.transform module '''

import sys
import os.path
sys.path.append( os.path.abspath( '..' ) )
sys.path.append( os.path.abspath( '../misc' ) )

import unittest
from floatcanvas.math import numpy

from floatcanvas.math import LinearTransform, LinearTransform2D, ArbitraryTransform, MercatorTransform, ThreeDProjectionTransform
import loadWorldData as worldData


class TestNode(unittest.TestCase):
    def setUp(self):
        self.coords2d = numpy.array( [ (0,0), (2,0), (2,2), (0,2) ] )
        self.coords3d = numpy.array( [ (0,0,0), (2,0,0), (2,2,0), (0,2,0) ] )
    
    
    def testLinear(self):
        t = LinearTransform2D()
        self.assert_( t.translation.tolist() == t.position.tolist() == t.pos.tolist() == [0,0], t.pos )
        self.assert_( t.scale.tolist() == [1,1], t.scale )
        t.pos = (5, 5)
        self.assert_( t.translation.tolist() == t.position.tolist() == t.pos.tolist() == [5,5], t.pos )
        self.assert_( t.scale.tolist() == [1,1], t.scale )
        t.scale = (2, 3)
        self.assert_( t.scale.tolist() == [2,3], t.scale )
        self.assert_( t.translation.tolist() == t.position.tolist() == t.pos.tolist() == [5,5], t.pos )
        self.assert_( t.matrix.tolist() == [ [2,0,5], [0,3,5], [0,0,1] ], t.matrix )

        tc = t( self.coords2d )
        self.assert_( tc.tolist() == [ [5,5], [9,5], [9,11], [5,11] ], tc )

    def testRotation(self):
        t = LinearTransform2D()
        self.assert_( t.rotation == 0, t.rotation )
        t.rotation = 45
        self.assert_( t.rotation == 45, t.rotation )
        
        t = LinearTransform2D()
        t.rotation = 45
        t.scale = (2, 1)
        self.assert_( t.rotation == 45, t.rotation )
        self.assert_( t.scale.tolist() == [2, 1], (t.scale, t.matrix) )

    def testArbitrary(self):
        def double(x):
            return x * 2
        t = ArbitraryTransform( double )
        tc = t( self.coords2d )
        self.assert_( tc.tolist() == [ [0,0], [4,0], [4,4], [0,4] ], tc )        

    def testMercator(self):
        t = MercatorTransform(0)
        tc = t( self.coords2d )

    def testMercatorInverse(self):
        t = MercatorTransform( 0, 100 )
        coords = numpy.array( [ (1,1), (0,0), (0.5, 0.8) ] )
        tc = t( coords )
        ttc = t.inverse( tc )
        self.assert_( (ttc == coords).all(), ( tc, ttc, coords ) )
        
    def test3D(self):
        t = ThreeDProjectionTransform( 800, 600, 90, 1, 100 )
        tc = t( self.coords3d )

    def testConcat(self):
        t1 = LinearTransform2D()
        t1.pos = (5, 3)
        t2 = LinearTransform2D()
        t2.pos = (5, 3)
        self.assert_( (t1 * t2).pos.tolist() == [10,6] )

    def testConcatDifferentKinds(self):
        tl = LinearTransform2D()
        tl.pos = (5, 3)
        tm = MercatorTransform(0)
        transformed = tl( tm( [[0,0]] ) )
        self.assert_( transformed.tolist() == [[5,3]], transformed )


    def testInverse(self):
        t = LinearTransform2D()
        t.pos = (5, 3)
        t.scale = (2,2)

        self.assert_( numpy.allclose( t.inverse.matrix, [ [0.5,0,-2.5], [0,0.5,-1.5], [0,0,1] ]), t.inverse.matrix )

    def testTranspose(self):
        t = LinearTransform2D()        
        t.pos = (5, 3)

        self.assert_( numpy.allclose( t.transpose.matrix, [ [1,0,0], [0,1,0], [5,3,1] ]), t.transpose.matrix )


    def testSpeed(self):
        # run world_test to generate world2.dat if not present

        tl = LinearTransform2D()
        tl.scale = (2,3)
        tl.pos = (5,5)

        tm = MercatorTransform(0)
        tas = ArbitraryTransform( lambda x: x**2 - 3*x + 2 )

        def benchmark(kind, transform):
            import time
            iterations = 100
            start = time.time()
            for i in range(0,iterations):
                result = transform( worldData.points )
                assert len(result) == len(worldData.points)
            print '(%s transform) Transformed %d points in avg. %.2f milliseconds' % ( kind, len(worldData.points), (time.time() - start) / iterations * 1000 )
            
        print
        benchmark( 'linear', tl )
        benchmark( 'mercator', tm )
        benchmark( 'arbitrary_simple', tas )
    

if __name__ == '__main__':
    unittest.main()
