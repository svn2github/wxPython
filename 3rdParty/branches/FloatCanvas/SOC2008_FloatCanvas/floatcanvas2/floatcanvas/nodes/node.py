class Node(object):
    ''' This is a node object.
    
        A node can have one or no parent node and zero to many child nodes.                
        
        Children are accessed though the children property, use the various
         add/removeChild methods to manipulate the children.
         
        The parent is accessed through the parent property and can be set/get.
        
        A root node is a node which has no parent.

        A node supports so-called node visitors which can be used to implement 
         easy and effective operations/iterations on whole trees/collections of
         nodes.
    '''
    def __init__( self, name = '', parent = None, children = [] ):
        self.name = name
        
        self._parentInternal = None
        self._children = []
        
        self.addChildren( children )
        self.parent = parent
        
    def _setParentInternal(self, parent):
        self._parentInternal = parent

    def _getParentInternal(self):
        return self._parentInternal
            
    _parent = property( _getParentInternal, _setParentInternal )

    def _getParent(self):
        return self._parent
            
    def _setParent(self, parent):
        try:
            if self._parent is not None:
                self._parent._children.remove(self)
        except ValueError:
            pass
        
        if parent:
            parent._children.append( self )

        self._parent = parent
    
    parent = property( _getParent, _setParent )
    
    # Make children read-only. otherwise we'd have to use a custom class derived
    # from list which observes any changes made to it, so the node can react
    # accordingly. This sounds too complicated though. So for 'write' access
    # use the addChild/removeChild/addChildren/removeChildren and
    # removeAllChildren methods
    def _getChildren(self):
        return self._children[:]

    children = property( _getChildren )

        
    def addChild( self, child, where = 'back' ):
        ''' Adds a child to this node
            where can be be 'front', 'back' or an integer index
        '''
        if child._parent is not None:
            child._parent.removeChild( child )

        child._parent = self

        if where == 'back':
            self._children.append( child )
        elif where == 'front':
            self._children.insert( 0, child )
        else:
            try:
                self._children.insert( where, child )
            except TypeError:
                msg = "the where parameter has to be one of 'front', 'back' or \
                      an integer index. You supplied %s (%s)"
                raise IndexError( msg % ( where, type(where) ) )

        
        
    def addChildren( self, children, where = 'back' ):
        ''' Adds a sequence of children to this node. This is better than
            calling node.addChild() from a loop, especially for many nodes.
            where can be be 'front', 'back' or an integer index
        '''
        for child in children:
            if child._parent is not None:
                child._parent.removeChild( child )

            child._parent = self

        if where == 'back':
            self._children.extend( children )
        elif where == 'front':
            self._children[0:] = children
        else:
            try:
                self._children[where:where] = children
            except TypeError:
                msg = "the where parameter has to be one of 'front', 'back' or \
                      an integer index. You supplied %s (%s)"
                raise IndexError( msg % ( where, type(where) ) )

            #child._parent = self
            
        
        
    def removeChild( self, child ):
        ''' Remove a child from this node '''
        child._parent = None
        self._children.remove( child )
        
    def removeChildAt( self, childIndex ):
        ''' Remove the child at index childIndex from this node '''
        child = self._children[ childIndex ]
        child._parent = None
        del self._children[childIndex]

    def removeChildren( self, children ):
        ''' Remove a sequence of children from this node '''
        for child in children:
            self.removeChild( child )

    def removeAllChildren( self ):
        ''' Remove all children from this node '''
        self.removeChildren( self._children[:] )

    def moveFrontBack( self, where = 'front' ):
        ''' Moves this node to the front of its parent node (if there is one)
            where can either be 'front', 'back' or the sibling node in front of it
        '''
        parent = self.parent
        parent.removeChild( self )
        parent.addChild( self, where )
                        
    def _getRoot(self):
        ''' Returns the root (the topmost) node of this node.
            Note: Could be recursively implemented, but if the tree gets very
                  deep I am concerned about stack overflows, that's why this is
                  iterative rather than recursive
        '''
        if self._parent is None:
            return self
        
        parent = self._parent
        while parent._parent is not None:
            parent = parent._parent
        
        return parent        
        
    # root is read-only
    root = property(_getRoot)
    
    def visit(self, visitor, visitChildren = True):
        ''' This is the function which provides an interface for the node
            visitors. It should usually not be called directly. Use a
            NodeVisitor instead.
        '''
        if not visitor.preVisit(self):
            return False
        
        if visitChildren:
            if not visitor.visit( self.children ):
                return False
    
        return visitor.postVisit(self)
    
    def __repr__(self):
        return '%s (name: %s)' % ( object.__repr__(self), self.name )
