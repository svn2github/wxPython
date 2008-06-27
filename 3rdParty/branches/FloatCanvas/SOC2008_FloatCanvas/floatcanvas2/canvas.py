from camera import Camera
from node import Node

class Canvas(Node):
    def __init__(self, *args, **keys):
        Node.__init__(self, *args, **keys)

class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, *args, **keys):
        Canvas.__init__(self, *args, **keys)
        
        self.camera = Camera()
