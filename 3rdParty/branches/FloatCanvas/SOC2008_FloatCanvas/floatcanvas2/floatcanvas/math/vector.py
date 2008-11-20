import numpy
import math

def length(v):
    return numpy.sqrt( numpy.dot( v, v ) )

def normalize(v):
    return v / length(v)

def get_angle(a, b, degrees = True):
    an, bn = normalize(a), normalize(b)
    v1 = numpy.dot( an, bn )
    v2 = numpy.cross( an, bn )

    result = numpy.arctan2( v2, v1 )
    
    if degrees:        
        result = math.degrees( result )

    return result


if __name__ == '__main__':
    print get_angle( (0,-1), (0,1) )
