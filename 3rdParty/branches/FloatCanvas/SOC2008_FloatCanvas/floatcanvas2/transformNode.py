from node import Node
from transform import LinearTransform
import numpy


class NodeWithTransform(Node):
    def __init__(self, *args, **keys):
        Node.__init__(self, *args, **keys)
        self.transform = LinearTransform()

    def _getLocalTransform(self):
        return self.transform

    def _setLocalTransform(self, transform):
        self.transform = transform

    def _getWorldTransform(self):
        transform = self.localTransform
        node = self.parent
        while node:
            transform = node.localTransform * transform
            node = node.parent
        return transform

    def _setWorldTransform(self, transform):
        if self.parent:
            self.transform = self.parent.worldTransform.inverse * transform
        else:
            self.transform = transform

    def _getPosition(self):
        return self.worldTransform.position

    def _setPosition(self, position):
        wt = self.worldTransform
        wt.position = position
        self.worldTransform = wt

    worldTransform = property( _getWorldTransform, _setWorldTransform )
    localTransform = property( _getLocalTransform, _setLocalTransform )

    position = pos = translation = property( _getPosition, _setPosition )


class NodeWithBounds(NodeWithTransform):
    pass
    #boundingBox = property( _getAABB, _setAABB )

class RenderableNode( NodeWithBounds ):
    pass
