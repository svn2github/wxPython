from ..nodes.camera import Viewport
from ..nodes.spatialQuery import QueryWithPrimitive

class DefaultRenderPolicy(object):
    def render(self, canvas, camera, backgroundColor):        
        from simpleCanvas import SimpleCanvas
        canvas.renderer.Clear( backgroundColor )
        camera.viewport = Viewport( canvas.screen_size )
        cam_transform = camera.viewTransform
        super(SimpleCanvas, canvas).Render( canvas.renderer, camera )
        canvas.renderer.Present()


class CullingRenderPolicy(object):
    def render(self, canvas, camera, backgroundColor):        
        canvas.renderer.Clear( backgroundColor )
        
        camera.viewport = Viewport( canvas.screen_size )
        cam_transform = camera.viewTransform
        
        # the following query could probably be cached
        view_box = camera.viewBox
        query = QueryWithPrimitive( view_box, exact = False )
        nodes_to_render = canvas.performSpatialQuery( query )
        
        self.renderedNodes = []
        for node in reversed(nodes_to_render):
            #  check whether some parent of the node is a
            #  render-to-surface node. If this is the case, don't render the
            #  child, because the parent will take care of rendering everything
            #  todo: fixme:  This should not be part of the render policy
            #                but there should rather be some method to retrieve
            #                the nodes which should be rendered (either the
            #                parent node returns the info or somehow else)
            parent = node.parent
            doRender = True
            while parent:
                if parent.render_to_surface_enabled:
                    doRender = False
                    break
                parent = parent.parent
            
            if not doRender:
                continue
            
            self.renderedNodes.append( node )
            # if we got here, render this node
            node.Render( canvas.renderer, camera, renderChildren = False )
            
        canvas.renderer.Present()
