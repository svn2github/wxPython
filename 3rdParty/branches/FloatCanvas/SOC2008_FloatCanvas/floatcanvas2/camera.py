from transformNode import NodeWithTransform

class Camera(NodeWithTransform):
    def __init__(self, transform, zoom = (1.0, 1.0), *args, **keys):
        NodeWithTransform.__init__( self, transform, *args, **keys )
        self.zoom = zoom
        
    def _getZoom(self):
        return ( 1.0 / self.scale[0], 1.0 / self.scale[1] )
            
    def _setZoom(self, value):
        self.scale = ( 1.0 / value[0], 1.0 / value[1] )

    zoom = property( _getZoom, _setZoom )
