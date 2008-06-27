class ITransform(object):
    def transform(self, coords):
        pass


import numpy
class LinearTransform(object):
    #implements(ITransform)
    def __init__(self, dimension = (3,3), matrix = None ):
        if not matrix is None:
            self.matrix = matrix
        else:
            self.matrix = numpy.eye( *dimension )     # identity matrix

    # a bit messy, it basically appends 1s to the coordinates and later removes them again
    def transform(self, coords):
        return numpy.dot( numpy.column_stack( (coords, numpy.ones(len(coords))) ), self.matrix )[ ..., :-1 ]

    def _getTranslation(self):
        return self.matrix[-1][:-1]

    def _setTranslation(self, translation):
        self.matrix[-1][:-1] = translation

    # can probably be rewritten 
    def _getScale(self):
        return numpy.array( [ numpy.sqrt( numpy.vdot( row[:-1], row[:-1] ) ) for row in self.matrix[:-1] ] )

    def _setScale(self, scale):
        current_scale = self.scale
        for row in self.matrix[:-1]:
            row[:-1] *= scale / current_scale

    def _getInverse(self):
        return LinearTransform( matrix = numpy.linalg.inv( self.matrix ) )

    def __mul__(self, otherLinear):
        return LinearTransform( matrix = numpy.dot( self.matrix, otherLinear.matrix ) )

    translation = property( _getTranslation, _setTranslation )
    position = pos = translation
    scale = property( _getScale, _setScale )
    inverse = property( _getInverse )


class ArbitraryTransform(object):
    #implements(ITransform)
    def __init__(self, func = lambda x: x):
        self.func = func

    def transform(self, coords):
        return self.func(coords) 

    def __mul__(self, otherArbitrary):
        return ArbitraryTransform( lambda x: self.func( otherArbitrary(x) ) )


class MercatorTransform(object):
    def __init__(self, longitudeCenter = 0):
        self.longitudeCenter = longitudeCenter
    
    def transform(self, coords):
        def mercator_lat(lat):
            return -numpy.log( numpy.tan( numpy.pi / 4 + lat / 2 ) ) + 3

        result = numpy.array( coords )
        result[::,::2] -= self.longitudeCenter
        result[::,1::2] = mercator_lat( result[::,1::2] )


class ThreeDProjectionTransform(LinearTransform):
    def __init__(self, width, height, fov, znear, zfar):
        LinearTransform.__init__( self, (4,4) )

        self.matrix = m = numpy.zeros( (4,4) )

        aspect = float(width) / height
        right = znear * numpy.tan ( fov / 2 * numpy.pi / 180.0 )
        top = right / aspect

        m[0][0] = 2 * znear / right / 2
        m[1][1] = 2 * znear / top / 2
        m[2][2] = -( zfar + znear ) / ( zfar - znear )

        m[2][3] = -zfar * znear / ( zfar - znear )
        m[3][2] = -1
