from node import Node
from transform import LinearTransform2D, CompoundTransform
from patterns.partial import partial


class NodeWithTransform(Node):
    def __init__(self, transform, *args, **keys):
        self.transform = transform
        #try:
        #    transform = keys['transform']
        #except KeyError:
        #    self.transform = LinearTransform2D()
        #else:
        #    self.transform = transform
        #    del keys['transform']
        #    
        Node.__init__(self, *args, **keys)
        

    def _getLocalTransform(self):
        return self._transform

    def _setLocalTransform(self, transform):
        self._transform = transform

    def _getWorldTransform(self):
        # try to concatenate all transforms. This is very useful when you have
        # like 100 linear transforms in a row, then these can be "compressed"
        # into exactly 1 transform. In turn the coordinates of the object are
        # only transformed once instead of multiple times.
        # todo: instead of concattenating them here already we might think
        #  about just returning the whole transformation chain and then letting
        #  the caller deal with it instead (for example a renderer). This way
        #  we'd get independent of Linear/Compound/otherTransformType issues.
        # iterative instead of recursive
        transform = self.localTransform
        node = self.parent
        while node:
            try:
                transform = node.localTransform * transform
            except TypeError:
                transform = CompoundTransform( node.localTransform, transform )
            node = node.parent
        #print transform, self.localTransform, self.parent.localTransform, self.parent.localTransform * self.localTransform
        return transform

    def _setWorldTransform(self, transform):
        if self.parent:
            self.transform = self.parent.worldTransform.inverse * transform
        else:
            self.transform = transform


    worldTransform = property( _getWorldTransform, _setWorldTransform )
    localTransform = transform = property( _getLocalTransform, _setLocalTransform )

    # these work only for linear transforms and are forwarded here for simple
    # access
    def _getPosition(which, self):
        return getattr(self, which).position

    def _setPosition(which, self, position):
        t = getattr(self, which)
        t.position = position
        setattr(self, which, t)

    def _getScale(which, self):
        return getattr(self, which).scale

    def _setScale(which, self, scale):
        t = getattr(self, which)
        t.scale = scale
        setattr(self, which, t)

    def _getRotation(which, self):
        return getattr(self, which).rotation

    def _setRotation(which, self, rotation):
        t = getattr(self, which)
        t.rotation = rotation
        setattr(self, which, t)

    position = pos = translation = localPosition = localPos = localTranslation = property( partial(_getPosition, 'localTransform'), partial(_setPosition, 'localTransform') )
    scale = localScale = property( partial(_getScale, 'localTransform'), partial(_setScale, 'localTransform') )
    rotation = localRotation = property( partial(_getRotation, 'localTransform'), partial(_setRotation, 'localTransform') )

    worldPosition = worldPos = worldTranslation = property( partial(_getPosition, 'worldTransform'), partial(_setPosition, 'worldTransform') )
    worldScale = property( partial(_getScale, 'worldTransform'), partial(_setScale, 'worldTransform') )
    worldRotation = property( partial(_getRotation, 'worldTransform'), partial(_setRotation, 'worldTransform') )


class NodeWithBounds(NodeWithTransform):
    pass
    #boundingBox = property( _getAABB, _setAABB )
