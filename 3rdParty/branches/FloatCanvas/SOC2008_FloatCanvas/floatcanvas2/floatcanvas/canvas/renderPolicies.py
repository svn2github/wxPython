''' module with two default render policies. Render policies control the exact
    rendering of the nodes on the canvas
'''

from ..nodes.spatialQuery import QueryWithPrimitive
from ..math.boundingBox import BoundingBox

class DefaultRenderPolicy(object):
    ''' This is the simplest possible rendering policy. It just clears the
        framebuffer, setups the camera, renders the canvas (and its children)
        and finally presents the result.
    '''
    def render(self, canvas, camera, backgroundColor):        
        from simpleCanvas import SimpleCanvas
        canvas.renderer.BeginRendering()
        canvas.renderer.Clear( backgroundColor )
        camera.viewport.size = canvas.screen_size
        cam_transform = camera.viewTransform

        bb = BoundingBox( ( (-1e10,-1e10), (1e10, 1e10) ) )
        query = QueryWithPrimitive( bb, exact = False )
        nodes_to_render = canvas.performSpatialQuery( query )

        self.renderedNodes = []
        for node in reversed(nodes_to_render):
            node.Render( canvas.renderer, camera, renderChildren = False )
        canvas.renderer.EndRendering()
        canvas.renderer.Present()


class CullingRenderPolicy(object):
    ''' This rendering policy is more complex. It performs a spatial query to
        determine all nodes within the cameras viewBox. If there are lots of
        nodes and the camera is only viewing a small subset of them, this speeds
        up things considerably.
    '''
    def render(self, canvas, camera, backgroundColor):        
        canvas.renderer.BeginRendering()
        canvas.renderer.Clear( backgroundColor )
        
        camera.viewport.size = canvas.screen_size
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
                if hasattr( parent, 'render_to_surface' ) and parent.render_to_surface:
                    doRender = False
                    break
                parent = parent.parent
            
            if not doRender:
                continue
            
            self.renderedNodes.append( node )
            # if we got here, render this node
            node.Render( canvas.renderer, camera, renderChildren = False )
            
        canvas.renderer.EndRendering()
        canvas.renderer.Present()
