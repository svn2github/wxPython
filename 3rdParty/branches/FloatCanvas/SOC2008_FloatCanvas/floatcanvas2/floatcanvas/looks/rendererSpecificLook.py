from look import Look
from ..patterns.cacher import Cacher

class RendererSpecificLook(Look):
    ''' a baseclass for looks whose implementations are renderer specific.
        the look can maintain a renderer independent description and then create
        renderer-dependent looks from it on request and caches them after
        creation.
    '''
    def __init__(self):
        self.look_cacher = Cacher()
        
    def Apply(self, renderer):
        try:
            renderer_specific_look = self._getLook(renderer)
        except KeyError:
            renderer_specific_look = self.createLook( renderer )
            self._addLook( renderer, renderer_specific_look )

        renderer_specific_look.Apply()
    
    def createLook(self, renderer):
        raise NotImplementedError()
    
    def _getLook(self, renderer):
        return self.look_cacher.get( renderer )

    def _addLook(self, renderer, renderer_specific_look):
        return self.look_cacher.add( renderer, renderer_specific_look )
    
    def __getstate__(self):
        d = self.__dict__.copy()
        del d['look_cacher']
        return d
    
    def __setstate__(self, state):
        self.__dict__ = state
        self.look_cacher = Cacher()