class ChildrenSerializer(object):
    def serializeChildren(node, serializer):
        return [ serializer.serializeNode(child) for child in node.children ]

    def unserializeChildren(data, serializer):
        return [ serializer.unserializeNode(childData) for childData in data ]

    serializeChildren = staticmethod( serializeChildren )
    unserializeChildren = staticmethod( unserializeChildren )


class NodeSerializer(object):
    def serialize(node, serializer):        
        childrenData = ChildrenSerializer.serializeChildren( node, serializer )
        thisData = ( node.name, childrenData )
        return thisData

    def unserialize(data, serializer, node = None):
        if node is None:
            node = Node()

        node.name = data[0]
            
        childrenData = data[-1]
        children = ChildrenSerializer.unserializeChildren( childrenData, serializer )
        node.addChildren( children )
        
        return node

    serialize = staticmethod( serialize )
    unserialize = staticmethod( unserialize )


class NodeWithTransformSerializer(object):
    def serialize(node, serializer):        
        thisData = ( NodeSerializer.serialize( node, serializer ), node.transform )
        return thisData

    def unserialize(data, serializer, node = None):
        if node is None:
            node = NodeWithTransform( transform = data[1] )
            
        NodeSerializer.unserialize( data[0], serializer, node )
        node.transform = data[1]           
        
        return node

    serialize = staticmethod( serialize )
    unserialize = staticmethod( unserialize )


class CameraSerializer(object):
    def serialize(node, serializer):        
        thisData = ( NodeWithTransformSerializer.serialize( node, serializer ), node.viewport )
        return thisData

    def unserialize(data, serializer, node = None):
        if node is None:
            node = ObservableCamera( transform = LinearTransform2D() )
            
        NodeWithTransformSerializer.unserialize( data[0], serializer, node )
        node.viewport = data[1]
                    
        return node

    serialize = staticmethod( serialize )
    unserialize = staticmethod( unserialize )
    

class DefaultRenderableNodeSerializer(object):
    # this one takes a shortcut and doesn't serialize the view properly
    # instead it just remembers the model data and look and rebuilds everything
    # when loaded (of course the canvas registry setup should be the same when
    # loading and saving, so the same views are created).
    # If one was to properly do this, the view would have to be saved by itself
    # so it could be restored later.
    
    def serialize(node, serializer):        
        try:
            surface_size = node.surface.size
        except AttributeError:
            surface_size = None

        try:
            look = node.view.look
        except AttributeError:
            look = None
        thisData = ( NodeWithTransformSerializer.serialize( node, serializer ), node.model, look, node.shown, node.render_to_surface_enabled, surface_size )

        return thisData

    def unserialize(data, serializer, node = None):
        if node is None:
            node = serializer.canvas.createFromModel( model = data[1], look = data[2], shown = data[3], render_to_surface_enabled = data[3], surface_size = data[4] )
        else:
            if not isinstance(node, SimpleCanvas):
                raise NotImplementedError()
            
        NodeWithTransformSerializer.unserialize( data[0], serializer, node )

        return node

    serialize = staticmethod( serialize )
    unserialize = staticmethod( unserialize )
    
    
class SimpleCanvasSerializer(object):
    def serialize(node, serializer):
        camera_index = node.children.index( node.camera )
        thisData = ( DefaultRenderableNodeSerializer.serialize( node, serializer ), node.backgroundColor, camera_index )
        return thisData

    def unserialize(data, serializer):        
        node = canvas = serializer.canvas
        canvas.removeAllChildren()
        DefaultRenderableNodeSerializer.unserialize( data[0], serializer, canvas )
        canvas.backgroundColor, camIndex = data[-2:]
        canvas.camera = canvas.children[camIndex]
        return canvas

    serialize = staticmethod( serialize )
    unserialize = staticmethod( unserialize )




def registerDefaultSerializers( registry ):
    for entry in defaultSerializers:
        nodeType, serializer = entry
        registry.register( nodeType, serializer )


from ..nodes import DefaultRenderableNode, Camera, Node, NodeWithTransform
from ..canvas.navCanvas import NavCanvas
from ..canvas.simpleCanvas import SimpleCanvas
from ..canvas.floatCanvas import FloatCanvas
from ..canvas.observables import ObservableDefaultRenderableNode, ObservableCamera, ObservableNode, ObservableNodeWithTransform
from ..math import LinearTransform2D

defaultSerializers = [ 
                       (ObservableNode, NodeSerializer), (Node, NodeSerializer),
                       (ObservableNodeWithTransform, NodeWithTransformSerializer), (NodeWithTransform, NodeWithTransformSerializer),
                       (ObservableCamera, CameraSerializer), (Camera, CameraSerializer),
                       (ObservableDefaultRenderableNode, DefaultRenderableNodeSerializer), (DefaultRenderableNode, DefaultRenderableNodeSerializer),
                       (NavCanvas, SimpleCanvasSerializer), (FloatCanvas, SimpleCanvasSerializer), (SimpleCanvas, SimpleCanvasSerializer)
                     ]


