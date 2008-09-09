import cPickle as pickle
from ..patterns.factory import FactoryUsingDict

class Serializer(object):
    serialization_protocol_version = '0.9'
    
    def __init__(self):
        self.nodeSerializerRegistry = FactoryUsingDict()
    
    def getSerializer(self, node):
        return self.nodeSerializerRegistry.create( type(node) )
    
    def serializeNode(self, node):
        nodeSerializer = self.getSerializer( node )
        data = nodeSerializer.serialize( node, self )
        return (nodeSerializer, data )
    
    def unserializeNode(self, data):
        nodeSerializer, nodeData = data
        return nodeSerializer.unserialize( nodeData, self )

    def serialize(self, rootNode, camera, serializeChildren = True):
        data = ( self.serialization_protocol_version, type(rootNode) )
        data = data + self.serializeNode( rootNode )
        
        return pickle.dumps( data, protocol = pickle.HIGHEST_PROTOCOL )

    def unserialize(self, canvas, data):
        self.canvas = canvas
        unpickled = pickle.loads( data )
        version = unpickled[0]        
        if version != self.serialization_protocol_version:
            raise ValueError( 'Cannot unserialize the data stream, file format version mismatch. The data has version %s, I can only unserialize data with version %s' % ( self.serialization_protocol_version, self.serialization_protocol_version ) )
        return self.unserializeNode( unpickled[2:] )

    def save(self, filename, rootNode, serializeChildren = True):
        data = self.serialize( rootNode, serializeChildren )
        f = file( filename, 'wb' )
        f.write( data )
        f.close()

    def load(self, filename, canvas):
        f = file( filename, 'rb' )
        data = f.read()
        f.close()

        return self.unserialize( canvas, data )