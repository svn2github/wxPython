from transformNode import NodeWithBounds

class RenderableNode(NodeWithBounds):
    def __init__(self, *args, **keys):
        NodeWithBounds.__init__(self, *args, **keys)


class DefaultRenderableNode(RenderableNode):
    def __init__(self, model, view, *args, **keys):
        RenderableNode.__init__(self, *args, **keys)
        self.model = model
        self.view = view

    def DoRender(self, renderer):
        return self.view.Render( renderer, self.model, self.worldTransform )

    def Render(self, renderer):
        self.DoRender(renderer)
        # traverse children in back-front order (so front objects overdraw back ones)
        for child in reversed(self.children):
            child.Render( renderer )