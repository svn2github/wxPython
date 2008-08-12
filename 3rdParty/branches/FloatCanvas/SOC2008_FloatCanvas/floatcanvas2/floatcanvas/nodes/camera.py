from transformNode import NodeWithTransform
from ..math import boundingBox, numpy

class Viewport(object):
    def __init__(self, size):
        self.size = numpy.array( size )

class Camera(NodeWithTransform):
    def __init__(self, transform, zoom = (1.0, 1.0), *args, **keys):
        NodeWithTransform.__init__( self, transform, *args, **keys )
        self.zoom = zoom
        self.viewport = None
        
    def _getZoom(self):
        return numpy.array( ( 1.0 / self.scale[0], 1.0 / self.scale[1] ) )
            
    def _setZoom(self, value):
        self.scale = ( 1.0 / value[0], 1.0 / value[1] )
        
    def _getViewTransform(self):
        transform = self.transform.inverse
        transform.position += self.viewport.size / 2
        return transform
    
    def _getViewBox(self):
        size = self.viewport.size
        local_box = boundingBox.fromRectangleCenterSize( (0,0), size )
        return boundingBox.fromPoints( self.transform( local_box.corners ) )

    zoom = property( _getZoom, _setZoom )
    viewTransform = property( _getViewTransform )
    viewBox = property( _getViewBox )


    def zoomToExtents(self, boundingBox, padding_percent = 0.05, maintain_aspect_ratio = True):
        self.pos = boundingBox.center
        
        if boundingBox.Size == (0,0):
            return
        
        new_zoom = (self.viewport.size / boundingBox.Size) * ( 1 - padding_percent )
        if maintain_aspect_ratio:
            old_zoom = self.zoom
            old_aspect = old_zoom[0] / old_zoom[1]
            if old_aspect > 1:                
                new_zoom = ( new_zoom[0], new_zoom[0] / old_aspect )
            else:
                new_zoom = ( new_zoom[1] * old_aspect, new_zoom[1] )

        self.zoom = new_zoom