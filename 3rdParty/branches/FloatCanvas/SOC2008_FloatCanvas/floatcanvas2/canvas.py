import observables
from gcrenderer import GCRenderer
from patterns.factory import FactoryUsingDict
from rtree import RTree
from sceneQuery import QueryWithPrimitive
import models
import views

class Canvas(observables.ObservableDefaultRenderableNode):
    def __init__(self, *args, **keys):
        observables.ObservableDefaultRenderableNode.__init__(self, *args, **keys)
        self.rtree = RTree()
        
    def _registerBoundedNode(self, node):
        self.rtree.addChild(node)

    def _unregisterBoundedNode(self, node):
        self.rtree.removeChild(node)

    def performSpatialQuery( self, query ):
        return self.rtree.performSpatialQuery( query )


class DefaultUpdatePolicy(object):
    def __init__(self, canvas, interval):
        self.canvas = canvas
        self.interval = interval * 1000
        self.dirty = False
        import wx
        self.timer = wx.CallLater( self.interval , self.onIntervalOver )
        
    def onDirty(self):
        self.dirty = True
            
    def onIntervalOver(self):
        self.Render()
        self.timer.Restart( self.interval )
        
    def Render(self):
        if self.dirty:
            print 'RENDER'
            self.canvas.Render()
            self.dirty = False


class DefaultRenderPolicy(object):
    def render(self, canvas, camera):        
        canvas.renderer.Clear()
        from camera import Viewport
        camera.viewport = Viewport( canvas.window.GetClientSize() )
        cam_transform = camera.viewTransform
        super(SimpleCanvas, canvas).Render( canvas.renderer, camera )
        canvas.renderer.Present()

class CullingRenderPolicy(object):
    def render(self, canvas, camera):        
        canvas.renderer.Clear()
        
        from camera import Viewport
        camera.viewport = Viewport( canvas.window.GetClientSize() )
        cam_transform = camera.viewTransform
        
        # the following query could probably be cached
        view_box = camera.viewBox
        query = QueryWithPrimitive( view_box, exact = False )
        nodes_to_render = canvas.performSpatialQuery( query )
        
        self.renderedNodes = nodes_to_render
        for node in nodes_to_render:
            node.Render( canvas.renderer, camera, renderChildren = False )
            
        canvas.renderer.Present()
        
        
class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, double_buffered = True, max_update_delay = 0.2, *args, **keys):
        if 'name' not in keys:
            keys['name'] = 'unnamed canvas'
        Canvas.__init__(self, None, None, observables.ObservableLinearTransform2D(), *args, **keys)
               
        self.camera = observables.ObservableCamera( observables.ObservableLinearTransform2D() )
        self.renderer = GCRenderer( window = window, dc = dc, native_window = native_window, native_dc = native_dc, wx_renderer = wx_renderer, double_buffered = double_buffered )
        self.window = window
        
        self.model_kinds = [ 'Rectangle', 'Circle', 'Ellipse' ]
        self.primitive_kinds = [ 'Rectangle', 'Ellipse' ]

        self._setupRegistries()
        self._setupNodeFactory()
        self.updatePolicy = DefaultUpdatePolicy( self, max_update_delay )
        self.subscribe( self.onDirty, 'attribChanged' )

        #self.renderPolicy = DefaultRenderPolicy()
        self.renderPolicy = CullingRenderPolicy()
        
    def _setupRegistries(self):
        from registries import PrimitiveRendererRegistry, ViewRegistry, RenderNodeRegistry
        self.primitiveRendererRegistry = PrimitiveRendererRegistry()
        self.viewRegistry = ViewRegistry()
        self.renderNodeRegistry = RenderNodeRegistry()
        
        for primitive_kind in self.primitive_kinds:
            modelInterface = getattr(models, 'I%s' % primitive_kind)
            primitiveRendererType = getattr(views, 'Default%sRenderer' % primitive_kind)
            self.primitiveRendererRegistry.register( modelInterface, primitiveRendererType )
            
        for model_kind in self.model_kinds:
            modelInterface = getattr(models, 'I%s' % model_kind)
            def createDefaultView(model, look):
                primitiveRendererConstructor, model = self.primitiveRendererRegistry.getRendererConstructor( model )
                primitiveRenderer = primitiveRendererConstructor( self.renderer, model )
                return observables.ObservableDefaultView( look, primitiveRenderer )
            self.viewRegistry.register( modelInterface, createDefaultView )
            
        for model_kind in self.model_kinds:
            modelInterface = getattr(models, 'I%s' % model_kind)
            def createDefaultRenderableNode(model, transform, look, name):
                viewConstructor, model = self.viewRegistry.getViewConstructor( model )
                view = viewConstructor( model = model, look = look )
                renderNode = observables.ObservableDefaultRenderableNode( model, view, transform, name = name )
                return renderNode
            self.renderNodeRegistry.register( modelInterface, createDefaultRenderableNode )
        
        
    def _setupNodeFactory(self):
        self.nodeFactory = FactoryUsingDict()
        self.create = self.nodeFactory.create
        self.registerNode = self.nodeFactory.register
        self.unregisterNode = self.nodeFactory.unregister
        self.isNodeRegistered = self.nodeFactory.is_registered
        
        from look import NoLook
        from patterns.partial import partial
       
        keywords = { 'transform'    : None,
                     'pos'          : None,
                     'position'     : None,
                     'rotation'     : None,
                     'scale'        : None,
                     'look'         : None,
                     'where'        : 'back'
                   }
        
        def get_keyword(dikt, name):
            result = dikt.get( name, keywords[name] )
            try:
                del dikt[name]
            except KeyError:
                pass
            return result
        
        for model_kind in self.model_kinds:
            def create(modelType, *args, **keys):
                model = modelType( *args )
                                
                look = get_keyword(keys, 'look')
                if look is None:
                    raise ValueError( 'You need to supply a look! Use look.NoLook or "nolook" if you want none.')
                if look == 'nolook':
                    look = NoLook
                if isinstance(look, (tuple, list)):
                    look = observables.ObservableSolidColourLook(*look)
                                        
                where = get_keyword(keys, 'where')
                transform = get_keyword(keys, 'transform')
                if transform is None:
                    transform = observables.ObservableLinearTransform2D()
                elif isinstance( transform, basestring ):
                    transform = getattr(observables, transform)()
                    transform = observables.ObservableLinearTransform2D() * transform

                pos = get_keyword(keys, 'pos') or get_keyword(keys, 'position')
                if pos is not None:
                    # assume linear transform
                    transform.position = pos
                    
                rotation = get_keyword(keys, 'rotation')
                if rotation is not None:
                    # assume linear transform
                    transform.rotation = rotation
                
                scale = get_keyword(keys, 'scale')
                if scale is not None:
                    # assume linear transform
                    transform.scale = scale

                renderNodeConstructor, model = self.renderNodeRegistry.getRenderNodeConstructor( model )
                renderNode = renderNodeConstructor( model, transform = transform, look = look, name = keys.get('name', '<unnamed node>') )

                self.addChild( renderNode, where = where )

                return renderNode

            modelType = getattr(observables, 'Observable%s' % model_kind)

            self.registerNode( model_kind, create, modelType )
            setattr( self, 'create%s' % model_kind, partial( create, modelType ) )
        

    def onDirty(self, evt):
        if self.dirty:
            self.updatePolicy.onDirty()

    def DoRender(self, renderer, camera):
        pass
    
    def Render(self, camera = None, renderChildren = True):
        if camera is None:
            camera = self.camera
        self.renderPolicy.render(self, camera)
