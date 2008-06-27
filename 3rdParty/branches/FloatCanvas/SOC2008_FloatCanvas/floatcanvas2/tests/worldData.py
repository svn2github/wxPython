import pickle
f = open('world2.dat', 'rb')
data = pickle.load(f)
points, lineLengths = data
f.close()