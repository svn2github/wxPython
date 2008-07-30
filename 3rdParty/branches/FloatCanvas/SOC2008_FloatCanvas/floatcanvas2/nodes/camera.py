from transformNode import NodeWithTransform
import boundingBox
import numpy

class Viewport(object):
    def __init__(self, size):
        self.size = numpy.array( size )

class Camera(NodeWithTransform):
    def __init__(self, transform, zoom = (1.0, 1.0), *args, **keys):
        NodeWithTransform.__init__( self, transform, *args, **keys )
        self.zoom = zoom
        self.viewport = None
        
    def _getZoom(self):
        return ( 1.0 / self.scale[0], 1.0 / self.scale[1] )
            
    def _setZoom(self, value):
        self.scale = ( 1.0 / value[0], 1.0 / value[1] )
        
    def _getViewTransform(self):
        transform = self.transform.inverse
        transform.position += self.viewport.size / 2
        return transform
    
    def _getViewBox(self):
        size = self.viewport.size
        center = self.transform.inverse.position
        local_box = boundingBox.fromRectangleCenterSize( center, size )
        return boundingBox.fromPoints( self.transform( local_box.corners ) )

    zoom = property( _getZoom, _setZoom )
    viewTransform = property( _getViewTransform )
    viewBox = property( _getViewBox )
