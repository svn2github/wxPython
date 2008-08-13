from transformNode import NodeWithBounds

class RenderableNode(NodeWithBounds):
    pass
    #def __init__(self, *args, **keys):
    #    NodeWithBounds.__init__(self, *args, **keys)


class BasicRenderableNode(RenderableNode):
    def __init__(self, model, view, *args, **keys):
        RenderableNode.__init__(self, *args, **keys)
        self.model = model
        self.view = view
        self._debugDrawBoundingBoxes = False
        self.shown = True
        #self.model.subscribe( self.onModelChanged, 'attribChanged' )
        self.subscribe( self.onSelfDirty, 'attribChanged' )        
           
    def onSelfDirty(self, evt):
        if not self.view:
            return
                
        #self.view.transform = self.worldTransform
        self._update_view_transform()
        
        if self.model.dirty:
            self.view.rebuild()
        
    def DoRender(self, renderer, camera):
        if self.view is None:
            return 
        return self.view.Render( renderer, camera )

    def Render(self, renderer, camera, renderChildren = True):
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
        return self.view.intersection(primitive)
            
    def _drawDebugBoundingBoxes(self, renderer, camera):
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
        # todo: fixme
        
        if not hasattr(self, 'xxx'):
            self.view.transform = self.worldTransform
        else:
            if (self.worldTransform.matrix != self.xxx.matrix).any():
                self.view.transform = self.worldTransform
            
        self.xxx = self.worldTransform
        
    def _getBoundingBox(self):
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
        return self.view.localBoundingBox
    
    localBoundingBox = property( _getLocalBoundingBox )
    
    def _getBoundingBoxRecursive(self):
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
    
    
    
from ..math.transform import LinearTransform2D
from ..nodes.camera import Camera, Viewport

class DefaultRenderableNode(BasicRenderableNode):
    def __init__(self, renderer, render_to_surface_enabled, surface_size, model, view, *args, **keys):
        BasicRenderableNode.__init__(self, model, view, *args, **keys)
        self.renderer = renderer
        self.render_to_surface_enabled = render_to_surface_enabled
        self.render_view = None
        if render_to_surface_enabled:            
            self.surface = renderer.CreateRenderSurface( surface_size, hasAlpha = True )
            self.camera = Camera( LinearTransform2D(), name = 'render to surface cam' )
            self.camera.viewport = Viewport( self.surface.size )
            self.regenerate = True
        
    def Render(self, renderer, camera, renderChildren = True):
        if not self.render_to_surface_enabled:
            return super(DefaultRenderableNode, self).Render( renderer, camera, renderChildren )
        
        renderToSurface = self.shouldRenderToSurface(renderer, camera, renderChildren)
        
        if renderToSurface or (self.render_view is None):
            print 'Rendering to surface ...'
            self.surface.Activate()
            self.surface.Clear( background_color = (0,0,0,0) )

            padding = 0.05
            self.camera.zoomToExtents( self.boundingBoxRecursive, padding_percent = padding, maintain_aspect_ratio = False)
            extra_scale = (1 + padding) / self.camera.viewTransform.scale

            super(DefaultRenderableNode, self).Render( renderer, self.camera, True )

            self.surface.Deactivate()
            print '... done'

            #self.render_object = renderer.CreateBitmap( self.surface.bitmap, True )
            from ..views.bitmapRenderer import DefaultBitmapRenderer
            from ..models.bitmap import Bitmap
            bitmap_model = Bitmap( self.surface.bitmap )
            self.render_view = DefaultBitmapRenderer( renderer, bitmap_model, look = None )
            #self.render_object = renderer.CreateBitmap( self.surface.bitmap )
            #self.render_object.transform = self.transform
            self.initial_transform = LinearTransform2D( matrix = self.worldTransform.matrix.copy() )

            #f = file( 'renderSurface_test.png', 'wb' )
            #f.write( self.surface.getData('png') )
            #f.close()
            self.regenerate = False
            

        #self.render_view.transform = self.worldTransform * self.initial_transform.inverse * self.camera.transform
        self.render_view.transform = LinearTransform2D( matrix = self.worldTransform.matrix.copy() ) * self.initial_transform.inverse * self.camera.transform
        self.render_view.Render( camera )


    def shouldRenderToSurface(self, renderer, camera, renderChildren):
        return self.regenerate