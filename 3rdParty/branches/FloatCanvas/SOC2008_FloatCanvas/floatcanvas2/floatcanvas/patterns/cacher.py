class Cacher(object):
    ''' A simple wrapper around a dictionary which is can be used to cache an 
        object with an associated key.
    '''
    def __init__(self):
        self.entries = {}

    def add(self, key, value):
        self.entries[key] = value

    def get(self, key):
        return self.entries[key]

    def remove(self, key):
        del self.entries[key]