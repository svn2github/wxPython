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
        self.model.subscribe( self.onModelChanged, 'attribChanged' )
        
    def onModelChanged(self, evt):
        if self.model.dirty:
            self.view.rebuild()

    def DoRender(self, renderer):
        self.view.transform = self.worldTransform
        return self.view.Render( renderer )

    def Render(self, renderer):
        if self.view: self.view.rebuild()
        self.DoRender(renderer)
        #self.view.dirty = False
        # traverse children in back-front order (so front objects overdraw back ones)
        for child in reversed(self.children):
            child.Render( renderer )
        self.model.dirty = False
        self._children.dirty = False
        self.dirty = False              # we're drawn and so not dirty anymore
            