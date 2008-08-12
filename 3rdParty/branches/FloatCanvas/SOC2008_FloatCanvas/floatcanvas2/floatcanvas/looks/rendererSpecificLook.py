from look import Look
from ..patterns.cacher import Cacher

class RendererSpecificLook(Look):    
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