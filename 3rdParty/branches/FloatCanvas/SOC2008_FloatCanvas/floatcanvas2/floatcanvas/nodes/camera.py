from transformNode import NodeWithTransform
from ..math import boundingBox, numpy

class Viewport(object):
    ''' The viewport of a camera, basically just a size '''
    def __init__(self, size):
        self.size = numpy.array( size )

class Camera(NodeWithTransform):
    ''' A camera node. It has a viewport, viewBox ( = viewport in world coords )
        and a viewTransform. 
    '''
    def __init__(self, transform, zoom = (1.0, 1.0), *args, **keys):
        NodeWithTransform.__init__( self, transform, *args, **keys )
        self.zoom = zoom
        self.viewport = None
        
    def _getZoom(self):
        ''' camera zoom is the inverse of the node's scale '''
        return numpy.array( ( 1.0 / self.scale[0], 1.0 / self.scale[1] ) )
            
    def _setZoom(self, value):
        ''' camera zoom is the inverse of the node's scale '''
        self.scale = ( 1.0 / value[0], 1.0 / value[1] )
        
    def _getViewTransform(self):
        ''' returns the view transform, (0,0) centered on screen '''
        transform = self.transform.inverse
        transform.position += self.viewport.size / 2
        return transform
    
    def _getViewBox(self):
        ''' returns the view box which is the viewport in world coords '''
        size = self.viewport.size
        local_box = boundingBox.fromRectangleCenterSize( (0,0), size )
        return boundingBox.fromPoints( self.transform( local_box.corners ) )

    zoom = property( _getZoom, _setZoom )
    viewTransform = property( _getViewTransform )
    viewBox = property( _getViewBox )


    def zoomToExtents(self, boundingBox, padding_percent = 0.05, maintain_aspect_ratio = True):
        ''' Given a bounding box this function tries to fit it into the view of
            the camera.
            padding_percent specifies how much "empty space" (padding) to
                            display around the bounding box.
            maintain_aspect_ratio If True, the aspect ratio (width / height
                        ratio) of the view is not changed. This may lead to
                        bounding box not entirely fitting into the view (?).
                        If False, the aspect ratio is altered so that bounding
                        box fits perfectly into the view (probably at the cost
                        of different scaling in x and y directions).
        '''
        self.pos = boundingBox.center
        
        if boundingBox.Size == (0,0):
            return
        
        new_zoom = (self.viewport.size / boundingBox.Size) * ( 1 - padding_percent )
        if maintain_aspect_ratio:
            old_zoom = self.zoom
            old_aspect = old_zoom[1] / old_zoom[0]

            # say new_zoom = (6, 9) and aspect ratio was 3
            # then we get p1 = (6, 27) and p2 = (3, 9)
            # so we chose p2, because it has less zoom and nothing is cut off
            possibility1 = ( new_zoom[0], new_zoom[0] * old_aspect )
            possibility2 = ( new_zoom[1] / old_aspect, new_zoom[1] )

            if possibility1[1] > new_zoom[1]:
                new_zoom = possibility2
            else:
                new_zoom = possibility1

        self.zoom = new_zoom