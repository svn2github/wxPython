from look import Look

class NoLook(Look):
    ''' a look which does nothing '''
    def Apply(renderer):
        pass
    Apply = staticmethod(Apply)
