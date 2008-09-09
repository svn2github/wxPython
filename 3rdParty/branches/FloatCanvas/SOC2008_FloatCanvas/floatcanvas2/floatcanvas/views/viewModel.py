class ViewModel(object):
    def __init__( self, kind, **keys ):
        self.kind = kind
        self.__dict__.update( keys )
        self.elements = keys
