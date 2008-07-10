from transformNode import NodeWithBounds

class RenderableNode(NodeWithBounds):
    def __init__(self, *args, **keys):
        NodeWithBounds.__init__(self, *args, **keys)


class DefaultRenderableNode(RenderableNode):
    def __init__(self, model, view, *args, **keys):
        RenderableNode.__init__(self, *args, **keys)
        self.model = model
        self.view = view

    def Render(self, renderer):
        return self.view.Render( renderer, self.model )
