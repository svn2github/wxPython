from transformNode import NodeWithBounds

class RenderableNode(NodeWithBounds):
    ''' Base class for a node that can be rendered '''
    pass


class BasicRenderableNode(RenderableNode):
    ''' A basic renderable node. It has a model and according view and uses them
         to render itself and to get the bounding information.
        Todo: clean up the dirty marking.
    '''

    def __init__(self, model, view, transform, show = True, name = '', parent = None, children = []):
        RenderableNode.__init__(self, transform, name, parent, children)
        self.model = model
        self.view = view
        self._debugDrawBoundingBoxes = False
        self.shown = show
        if self.model:
            # we can set this here to False, because the view of it has already been built
            self.model.dirty = False
        #self.model.subscribe( self.onModelChanged, 'attribChanged' )
        self.subscribe( self.onSelfDirty, 'attribChanged' )        
           
    def onSelfDirty(self, evt):
        ''' If we're dirty, update what's necessary. '''
        if not self.view:
            return
                
        #self.view.transform = self.worldTransform
        self._update_view_transform()
        
        if self.model.dirty:
            self.view.rebuild()
            self.model.dirty = False
        
    def DoRender(self, renderer, camera):
        ''' Render ourselves. '''
        if self.view is None:
            return 
        return self.view.Render( renderer, camera )

    def Render(self, renderer, camera, renderChildren = True):
        ''' Render ourselves and probably our children. '''
        if not self.shown:
            return False
        
        self.DoRender(renderer, camera)
        if self.view: self.view.dirty = False
        if self.model: self.model.dirty = False
        self.dirty = False
        # traverse children in back-front order (so front objects overdraw back ones)
        if renderChildren:
            for child in reversed(self.children):
                try:
                    render = child.Render
                except AttributeError:
                    pass
                else:
                    render( renderer, camera )

        if self.view: self.view.dirty = False
        if self.model: self.model.dirty = False
        self.dirty = False
        self._children.dirty = False
        self.transform.dirty = False
        
        if self._debugDrawBoundingBoxes and self.view:
            self._drawDebugBoundingBoxes(renderer, camera)
            
    def intersection(self, primitive):
        ''' Tests whether we intersect with the given primitive. This is used
             by exact spatial queries.
        '''
        if not self.view:
            return False
        return self.view.intersection( primitive )
            
    def _drawDebugBoundingBoxes(self, renderer, camera):
        ''' Internal function to visualize the bounding boxes. '''
        from look import OutlineLook
        from models import Rectangle
        from views import DefaultRectangleRenderer
        # set look
        outline = OutlineLook( 'black' )
        outline.Apply( renderer )
        # local bbox
        model = Rectangle( self.localBoundingBox.Size )
        view = DefaultRectangleRenderer(renderer, model)
        view.transform = self.worldTransform
        view.Render(camera)
        # global bbox
        #model = Rectangle( self.boundingBox.Size )
        #view = DefaultRectangleRenderer( renderer, model )
        #view.transform.position = self.boundingBox.center
        #view.transform.rotation = camera.viewTransform.inverse.rotation
        ##view.transform.scale = camera.viewTransform.inverse.scale
        #print self.boundingBox
        #view.transform = view.transform
        #view.Render( camera )
        
    def _update_view_transform(self):
        ''' updates the transform of our view with our own transform.
            Todo: fixme
        '''
        
        if not hasattr(self, 'xxx'):
            self.view.transform = self.worldTransform
        else:
            if (self.worldTransform.matrix != self.xxx.matrix).any():
                self.view.transform = self.worldTransform
            
        self.xxx = self.worldTransform
        
    def _getBoundingBox(self):
        ''' returns our bounding box in world space. If we don't have a view
            then consider the bounding box of our children as our own bounding
            box.
            Todo: Check whether the no-view handling should be moved into a
            class of its own or if this should be moved to the
            recursiveBoundingBox property.
        '''
        if self.view is None:
            if not self.children:
                raise ValueError('A renderable node either has to have a view or children')
            
            childBB = self.children[0].boundingBoxRecursive
            for child in self.children[1:]:
                childBB.Merge( child.boundingBoxRecursive )

            return childBB

        self._update_view_transform()
        return self.view.boundingBox
    
    boundingBox = property( _getBoundingBox )
    
    def _getLocalBoundingBox(self):
        ''' Returns the bounding box in the local frame '''
        return self.view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )
    
    def _getBoundingBoxRecursive(self):
        ''' Returns the bounding box of this node including the bounding boxes
            of all children.
        '''
        bb = self.boundingBox
        for child in self.children:
            try:
                childBB = child.boundingBoxRecursive
            except AttributeError:
                pass
            else:
                bb.Merge( childBB )
            
        return bb       
    
    boundingBoxRecursive = property( _getBoundingBoxRecursive )

    def _getLook(self):
        return self.view.look

    def _setLook(self, look):
        self.view.look = look

    look = property( _getLook, _setLook )
    

class NodeToSurfaceRenderer(object):
    ''' renders a node to a bitmap
        todo: could share surfaces between nodes
    '''
    def __init__(self, node, surface_size, render):
        self.node = node
        self.renderer = node.renderer
        self.render = render
        self.surface_size = surface_size
        self._createRenderSurface( surface_size )

    def _createRenderSurface(self, surface_size):
        self.surface = self.renderer.CreateRenderSurface( surface_size, hasAlpha = True )
        self.camera = Camera( LinearTransform2D(), name = 'render to surface cam' )
        self.camera.viewport = Viewport( self.surface.size )
        
    def renderNodeToSurface(self, padding = 0.05):
        node = self.node
            
        print 'Rendering to surface ...'
        self.surface.Activate()
        self.surface.BeginRendering()
        self.surface.Clear( background_color = (0,0,0,0) )

        self.camera.zoomToExtents( node.boundingBoxRecursive, padding_percent = padding, maintain_aspect_ratio = False)
        extra_scale = (1 + padding) / self.camera.viewTransform.scale

        self.render( self.renderer, self.camera, True )

        self.surface.EndRendering()
        self.surface.Deactivate()
        print '... done'
        
        from ..views import BaseRenderer, DefaultBitmapRenderer
        from ..models.bitmap import Bitmap
        self.bitmap_model = Bitmap( self.surface.bitmap )
        self.render_view = BaseRenderer( self.renderer, look = None, model = self.bitmap_model, primitiveRenderer = DefaultBitmapRenderer() )
        self.initial_transform = LinearTransform2D( matrix = node.worldTransform.matrix.copy() )
        
    def renderSurface(self, camera):
        #self.render_view.transform = self.worldTransform * self.initial_transform.inverse * self.camera.transform
        self.render_view.transform = LinearTransform2D( matrix = self.node.worldTransform.matrix.copy() ) * self.initial_transform.inverse * self.camera.transform
        self.render_view.Render( camera )
        


from ..math.transform import LinearTransform2D
from ..nodes.camera import Camera, Viewport

# todo: change this class so it uses only filters
#       render_to_surface can be expressed as a filter
#       plus we can establish filter chains where the output of one filter
#       is fed to that of another filter (or multiple filters)
#       this allows us to create entire filter graphs
class DefaultRenderableNode(BasicRenderableNode):
    ''' The standard renderable node used in fc.
        It features render-to-surface functionality which can be used for things
        like layers.
        Set the regenerate attribute to True if you want the node to rerender
        the surface. You can also customize the shouldRenderToSurface method
        to determine when to re-render to surface.
    ''' 
    def __init__(self, renderer, render_to_surface, surface_size, filter, model, view, transform, show = True, name = '', parent = None, children = []):
        BasicRenderableNode.__init__(self, model, view, transform, show, name, parent, children)
        self.renderer = renderer
        self.surface_size = surface_size
        self.render_to_surface = render_to_surface
        self.filter = filter
        if filter:
            self.filter.create( self, self.RenderWithoutFilter )

        self.regenerate = True
        if self.render_to_surface:
            self.surface_renderer = NodeToSurfaceRenderer( self, surface_size, self.RenderDirect )
        
    def RenderDirect(self, renderer, camera, renderChildren):
        return super(DefaultRenderableNode, self).Render( renderer, camera, renderChildren )
    
    def RenderWithoutFilter(self, renderer, camera, renderChildren):
        if not self.render_to_surface:
            return self.RenderDirect( renderer, camera, renderChildren )
        
        renderToSurface = self.shouldRenderToSurface(renderer, camera, renderChildren)
        
        if renderToSurface:
            self.surface_renderer.renderNodeToSurface()
            self.regenerate = False
            
        self.surface_renderer.renderSurface( camera )

    
    def Render(self, renderer, camera, renderChildren = True):
        ''' Override the base class render method to implement the
            render-to-surface functionality.
        '''
        if self.filter:
            self.filter.render( renderer, camera, renderChildren )
        else:
            self.RenderWithoutFilter( renderer, camera, renderChildren )


    def shouldRenderToSurface(self, renderer, camera, renderChildren):
        return self.regenerate
    
    def _setRenderToSurfaceEnabled(self, value):
        if hasattr(self, '_render_to_surface_enabled') and value == self._render_to_surface:            # no change
            return
        self._render_to_surface = value
        self.regenerate = True

    def _getRenderToSurfaceEnabled(self):
        return self._render_to_surface

    render_to_surface_enabled = render_to_surface = property( _getRenderToSurfaceEnabled, _setRenderToSurfaceEnabled )
    

    def _getLocalBoundingBox(self):
        ''' Returns the bounding box in the local frame '''
        if self.filter:
            return self.filter.localBoundingBox
        return self.view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )
