import numpy
import math

class WorldDataConverter(object):
    def __init__(self, in_filename, out_filename):
        self.load(in_filename)
        self.save(out_filename)

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

    def save(self, filename):
        import pickle

        f = open( filename, 'wb' )
        pickle.dump( ( self.points, self.lineLengths ), f, pickle.HIGHEST_PROTOCOL )
        f.close()

        #f = open( './loadWorldData.py', 'w' )
        #f.write( "import pickle\nf = open('%s', 'rb')\ndata = pickle.load(f)\npoints, lineLengths = data\nf.close()" % filename )
        #f.close()

if __name__ == '__main__':
    WorldDataConverter( '../data/world.dat', '../data/world_numpy.dat' )
