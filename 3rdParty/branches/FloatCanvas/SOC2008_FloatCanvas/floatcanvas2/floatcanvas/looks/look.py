class Look(object):
    ''' base class for all looks '''
    def Apply(self, renderer):
        raise NotImplementedError()
