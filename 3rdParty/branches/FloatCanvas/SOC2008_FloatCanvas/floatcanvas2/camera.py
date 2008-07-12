from transformNode import NodeWithTransform

class Camera(NodeWithTransform):
    def __init__(self, zoom = (1.0, 1.0), *args, **keys):
        NodeWithTransform.__init__( self, *args, **keys )
        self.zoom = zoom

    zoom = NodeWithTransform.scale
