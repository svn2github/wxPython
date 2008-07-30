from look import Look
from ..patterns.cacher import Cacher

class RendererSpecificLook(Look):    
    def __init__(self):
        self.look_cacher = Cacher()
        
    def Apply(self, renderer):
        try:
            renderer_specific_look = self.look_cacher.get( renderer )
        except KeyError:
            renderer_specific_look = self.createLook( renderer )
            self.look_cacher.add( renderer, renderer_specific_look )

        renderer_specific_look.Apply()
    
    def createLook(self, renderer):
        raise NotImplementedError()
