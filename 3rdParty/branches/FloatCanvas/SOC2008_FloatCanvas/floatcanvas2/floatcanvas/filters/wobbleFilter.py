from helpers import renderBitmap
from blur import gaussian_blur
from ..nodes.renderableNode import NodeToSurfaceRenderer
from ..math import numpy

class PixelizeFilter(object):
    def __init__(self, block_size, surface_size, method = 'fftreal'):
        self.block_size = block_size
        self.surface_size = surface_size
        self.method = method
        
    def create(self, node, node_render_func):
        self.node = node
        self.surface_renderer = NodeToSurfaceRenderer( node, self.surface_size, node_render_func )
        self.node_render_func = node_render_func
        
    def render( self, renderer, camera, renderChildren ):
        node = self.node
               
        # first render the node to the surface
        self.surface_renderer.renderNodeToSurface( padding = 0.05 )
        
        pixels = self.surface_renderer.surface.bitmapPixels
        dst = numpy.empty_like(pixels)
        
        bs = self.block_size
        # this is not the most efficient method i guess...
        for x in range( bs[0] ):
            for y in range( bs[1] ):
                src = pixels[0::bs[0], 0::bs[1], ... ]
                target = pixels[1+x::bs[0], 1+y::bs[1], ... ]
                
                dst[1+x::bs[0], 1+y::bs[1], ... ] = src[ :target.shape[0], :target.shape[1], :target.shape[2] ]

        # render the pixelized image
        self.bitmap_view = renderBitmap( dst, self.surface_renderer.camera, camera, renderer )