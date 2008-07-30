class Cacher(object):
    def __init__(self):
        self.entries = {}

    def add(self, key, value):
        self.entries[key] = value

    def get(self, key):
        return self.entries[key]
