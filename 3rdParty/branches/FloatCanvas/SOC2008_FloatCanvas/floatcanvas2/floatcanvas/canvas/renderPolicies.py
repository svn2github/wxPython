from ..nodes.camera import Viewport
from ..nodes.spatialQuery import QueryWithPrimitive

class DefaultRenderPolicy(object):
    def render(self, canvas, camera):        
        from simpleCanvas import SimpleCanvas
        canvas.renderer.Clear()
        camera.viewport = Viewport( canvas.window.GetClientSize() )
        cam_transform = camera.viewTransform
        super(SimpleCanvas, canvas).Render( canvas.renderer, camera )
        canvas.renderer.Present()


class CullingRenderPolicy(object):
    def render(self, canvas, camera):        
        canvas.renderer.Clear()
        
        camera.viewport = Viewport( canvas.window.GetClientSize() )
        cam_transform = camera.viewTransform
        
        # the following query could probably be cached
        view_box = camera.viewBox
        query = QueryWithPrimitive( view_box, exact = False )
        nodes_to_render = canvas.performSpatialQuery( query )
        
        self.renderedNodes = nodes_to_render
        for node in reversed(nodes_to_render):
            node.Render( canvas.renderer, camera, renderChildren = False )
            
        canvas.renderer.Present()
