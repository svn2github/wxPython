from helpers import renderBitmap
from blur import gaussian_blur
from ..nodes.renderableNode import NodeToSurfaceRenderer

class GlowFilter(object):
    def __init__(self, sigma, kernel_size, surface_size, glow_colour, scale = (1.2, 1.2), offset = (0,0), method = 'fftreal'):
        self.sigma = sigma
        self.kernel_size = kernel_size
        self.scale = scale
        self.offset = offset
        self.glow_colour = glow_colour
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
        
        # get the alpha channel and set all colors to alpha to make it grey
        pixels = self.surface_renderer.surface.bitmapPixels
        pixels[...,0:3] = self.glow_colour[0:3]
        pixels[...,3] *= self.glow_colour[3] / 255.0
        
        # blur it
        blurred_image = gaussian_blur( pixels, self.sigma, self.kernel_size, self.method )        
        
        # render the glow
        self.bitmap_view = renderBitmap( blurred_image, self.surface_renderer.camera, camera, renderer, self.offset, self.scale )

        # render the node
        self.node_render_func( renderer, camera, renderChildren )

        
        
    def _getLocalBoundingBox(self):
        ''' Returns the bounding box in the local frame '''
        return self.bitmap_view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )