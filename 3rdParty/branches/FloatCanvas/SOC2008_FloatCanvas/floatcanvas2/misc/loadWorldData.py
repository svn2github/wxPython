import pickle
f = open('../data/world_numpy.dat', 'rb')
data = pickle.load(f)
points, lineLengths = data
f.close()