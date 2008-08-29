from helpers import renderBitmap
from blur import gaussian_blur
from ..nodes.renderableNode import NodeToSurfaceRenderer

class ThreeDFilter(object):
    ''' todo: doesn't look good '''    
    def __init__(self, sigma, kernel_size, offset, scale, surface_size, shadow_colour = (0,0,0,255), method = 'fftreal'):
        self.sigma = sigma
        self.kernel_size = kernel_size
        self.offset = offset
        self.scale = scale
        self.shadow_colour = shadow_colour
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
        #pixels[...,0:3] = self.shadow_colour[0:3]
        pixels[...,3] *= self.shadow_colour[3] / 255.0
        
        # blur it
        blurred_image = gaussian_blur( pixels, self.sigma, self.kernel_size, self.method )
                
        # render the node on top of it
        self.node_render_func( renderer, camera, renderChildren )

        # render the blurred image
        self.bitmap_view = renderBitmap( blurred_image, self.surface_renderer.camera, camera, renderer, scale = self.scale, offset = self.offset )
        
        
    def _getLocalBoundingBox(self):
        ''' Returns the bounding box in the local frame '''
        return self.bitmap_view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )