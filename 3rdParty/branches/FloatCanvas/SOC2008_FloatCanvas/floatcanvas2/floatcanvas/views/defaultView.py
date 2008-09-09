class DefaultView(object):
    ''' The default view holds a look and a primitive_renderer. Those two
        define how an object will be rendereed.
    '''
    def __init__(self, look, primitive_renderer):
        self.look = look
        self.primitive_renderer = primitive_renderer

    def Render(self, renderer, camera):
        self.look.Apply(renderer)
        self.primitive_renderer.Render(camera)
        self.look.dirty = False
        self.transform.dirty = False
        self.dirty = False
        
    def rebuild(self):
        self.primitive_renderer.rebuild()
        
    def intersection(self, primitive):
        return self.primitive_renderer.intersection(primitive)
        
    def _getTransform(self):
        return self.primitive_renderer.transform
    
    def _setTransform(self, transform):
        self.primitive_renderer.transform = transform

    transform = property( _getTransform, _setTransform )

    def _getBoundingBox(self):
        return self.primitive_renderer.boundingBox
    
    boundingBox = property( _getBoundingBox )
    
    def _getLocalBoundingBox(self):
        return self.primitive_renderer.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )