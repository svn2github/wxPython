from node import Node

class Camera(Node):
    def __init__(self, name = '', parent = None, children = [], zoom = (1.0, 1.0)):
        Node.__init__( self, name, parent, children )

        self.zoom = zoom
