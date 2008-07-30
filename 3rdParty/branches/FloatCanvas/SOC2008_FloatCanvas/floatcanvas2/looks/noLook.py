from look import Look

class NoLook(Look):    
    def Apply(renderer):
        pass
    Apply = staticmethod(Apply)
