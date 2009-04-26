from node import Node
from ..math import LinearTransform2D, CompoundTransform
from ..patterns.partial import partial


class NodeWithTransform(Node):
    ''' A node with a transform property.
    '''
    def __init__(self, transform, name = '', parent = None, children = []):
        self.transform = transform
        #try:
        #    transform = keys['transform']
        #except KeyError:
        #    self.transform = LinearTransform2D()
        #else:
        #    self.transform = transform
        #    del keys['transform']
        #    
        Node.__init__(self, name, parent, children)
        

    def _getLocalTransform(self):
        ''' Returns the local transform '''
        return self._transform

    def _setLocalTransform(self, transform):
        self._transform = transform

    def _getWorldTransform(self):
        ''' Returns the world transform (which is the transform of all
            ancestors) combined with the local transform.
        
          Tries to concatenate all transforms. This is very useful when you have
          like 100 linear transforms in a row, then these can be "compressed"
          into exactly 1 transform. In turn the coordinates of the object are
          only transformed once instead of multiple times.
          Todo: instead of concattenating them here already we might think
           about just returning the whole transformation chain and then letting
           the caller deal with it instead (for example a renderer). This way
           we'd get independent of Linear/Compound/otherTransformType issues.
          Iterative instead of recursive.
        '''
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
        ''' Sets the world transfomr, only works if the parent's world transform
            has an inverse '''
        if self.parent:
            self.transform = self.parent.worldTransform.inverse * transform
        else:
            self.transform = transform


    worldTransform = property( _getWorldTransform, _setWorldTransform )
    localTransform = transform = property( _getLocalTransform, _setLocalTransform )

    # these work only for linear transforms and are forwarded here for simple
    # access
    def _getPosition(which, self):
        ''' Gets the position of the transform and thus node '''
        return getattr(self, which).position

    def _setPosition(which, self, position):
        ''' Sets the position of the transform and thus node '''
        t = getattr(self, which)
        t.position = position
        setattr(self, which, t)

    def _getScale(which, self):
        ''' Gets the scale of the transform and thus node '''
        return getattr(self, which).scale

    def _setScale(which, self, scale):
        ''' Sets the scale of the transform and thus node '''
        t = getattr(self, which)
        t.scale = scale
        setattr(self, which, t)

    def _getRotation(which, self):
        ''' Gets the rotation of the transform and thus node '''
        return getattr(self, which).rotation

    def _setRotation(which, self, rotation):
        ''' Sets the rotation of the transform and thus node '''
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
    ''' A node with spatial bounds.
        Base class for other nodes which should implement the intersection
        function if they want to support exact spatial queries.
        Registers itself to its root node (usually the canvas) so it can
        insert this node into the rtree.
    '''
    def intersection(self, primitive):
        ''' implement in derived class '''
        raise NotImplementedError()
    
    def _getParentInternal(self):
        return NodeWithTransform._getParentInternal(self)
    
    def _setParentInternal(self, value):
        ''' Track parent changes. When a parent changes this means the root node
            can change.
            Registers itself to the root node (usually the canvas) so it can
            insert this node into the rtree.
        '''
        oldparent = self._parent        
        if not oldparent is None:
            root = self.root
            def unregisterNode(node):
                root._unregisterBoundedNode(node)
                for child in node.children:
                    unregisterNode(child)
            unregisterNode(self)

        result = NodeWithTransform._setParentInternal(self, value)
        
        if not self._parent is None:
            try:
                rbn = self.root._registerBoundedNode
            except AttributeError:
                pass
            else:
                rbn(self)

        return result

    _parent = property( _getParentInternal, _setParentInternal )
    #boundingBox = property( _getAABB, _setAABB )
