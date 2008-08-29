from helpers import renderBitmap
from blur import gaussian_blur
from ..nodes.renderableNode import NodeToSurfaceRenderer

class GaussianBlurFilter(object):
    def __init__(self, sigma, kernel_size, surface_size, method = 'fftreal'):
        self.sigma = sigma
        self.kernel_size = kernel_size
        self.surface_size = surface_size
        self.method = method
        
    def create(self, node, node_render_func):
        self.node = node
        self.surface_renderer = NodeToSurfaceRenderer( node, self.surface_size, node_render_func )
        self.node_render_func = node_render_func
        
    def render( self, renderer, camera, renderChildren ):
        node = self.node
        
        # first render the node to the surface
        self.surface_renderer.renderNodeToSurface( padding = 0.2 )
        
        # blur the bitmap
        blurred_image = gaussian_blur( self.surface_renderer.surface.bitmapPixels, self.sigma, self.kernel_size, self.method )
        
        # render the blurred image
        self.bitmap_view = renderBitmap( blurred_image, self.surface_renderer.camera, camera, renderer )
        
        # render the node on top of it
        #self.node_render_func( renderer, camera, renderChildren )
        
    def _getLocalBoundingBox(self):
        ''' Returns the bounding box in the local frame '''
        return self.bitmap_view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )