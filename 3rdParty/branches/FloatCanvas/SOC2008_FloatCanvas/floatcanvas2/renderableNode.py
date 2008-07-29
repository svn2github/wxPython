from transformNode import NodeWithBounds

class RenderableNode(NodeWithBounds):
    pass
    #def __init__(self, *args, **keys):
    #    NodeWithBounds.__init__(self, *args, **keys)


class DefaultRenderableNode(RenderableNode):
    def __init__(self, model, view, *args, **keys):
        RenderableNode.__init__(self, *args, **keys)
        self.model = model
        self.view = view
        self._debugDrawBoundingBoxes = False
        #self.model.subscribe( self.onModelChanged, 'attribChanged' )
        self.subscribe( self.onSelfDirty, 'attribChanged' )        
           
    def onSelfDirty(self, evt):
        if not self.view:
            return
                
        #self.view.transform = self.worldTransform
        self._update_view_transform()
        
        if self.model.dirty:
            self.view.rebuild()
        
    def DoRender(self, renderer, camera):
        return self.view.Render( renderer, camera )

    def Render(self, renderer, camera, renderChildren = True):
        self.DoRender(renderer, camera)
        #self.view.dirty = False
        # traverse children in back-front order (so front objects overdraw back ones)
        if renderChildren:
            for child in reversed(self.children):
                child.Render( renderer, camera )
            self.recursiveDirty = False          # we're drawn and so not dirty anymore
        else:
            self.recursiveDirty = False
        
        if self._debugDrawBoundingBoxes and self.view:
            self._drawDebugBoundingBoxes(renderer, camera)
            
    def intersection(self, primitive):
        return self.view.intersection(primitive)
            
    def _drawDebugBoundingBoxes(self, renderer, camera):
        from look import OutlineLook
        from models import Rectangle
        from views import DefaultRectangleRenderer
        # set look
        outline = OutlineLook( 'black' )
        outline.Apply( renderer )
        # local bbox
        model = Rectangle( self.localBoundingBox.Size )
        view = DefaultRectangleRenderer(renderer, model)
        view.transform = self.worldTransform
        view.Render(camera)
        # global bbox
        #model = Rectangle( self.boundingBox.Size )
        #view = DefaultRectangleRenderer( renderer, model )
        #view.transform.position = self.boundingBox.center
        #view.transform.rotation = camera.viewTransform.inverse.rotation
        ##view.transform.scale = camera.viewTransform.inverse.scale
        #print self.boundingBox
        #view.transform = view.transform
        #view.Render( camera )
        
    def _update_view_transform(self):
        # todo: fixme
        if not hasattr(self, 'xxx'):
            self.view.transform = self.worldTransform
        else:
            if (self.worldTransform.matrix != self.xxx.matrix).any():
                self.view.transform = self.worldTransform
            
        self.xxx = self.worldTransform
        
    def _getBoundingBox(self):
        self._update_view_transform()
        return self.view.boundingBox
    
    boundingBox = property( _getBoundingBox )
    
    def _getLocalBoundingBox(self):
        return self.view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )