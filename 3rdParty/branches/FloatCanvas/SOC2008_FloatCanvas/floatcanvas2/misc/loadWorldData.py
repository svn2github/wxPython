import pickle
f = open('../data/world_numpy.dat', 'rb')
data = pickle.load(f)
points, lineLengths = data

lines = []
currentPos = 0
for lineLength in lineLengths:
    line_points = points[currentPos:currentPos + lineLength]        
    currentPos += lineLength
    lines.append( line_points )

mapPointsAsLineList = lines

f.close()
