from canvas import Canvas
import observables
from ..renderers import GCRenderer
from ..patterns.adapter import AdapterRegistry
from ..patterns.factory import FactoryUsingDict
from registries import PrimitiveRendererRegistry, ViewRegistry, RenderNodeRegistry
from .. import models, views
from ..models import defaultAdapters
from ..looks import NoLook
from ..patterns.partial import partial
from updatePolicies import DefaultUpdatePolicy
from renderPolicies import CullingRenderPolicy, DefaultRenderPolicy


class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, double_buffered = True, max_update_delay = 0.2, *args, **keys):
        if 'name' not in keys:
            keys['name'] = 'unnamed canvas'
        Canvas.__init__(self, None, None, observables.ObservableLinearTransform2D(), *args, **keys)
               
        self.camera = observables.ObservableCamera( observables.ObservableLinearTransform2D() )
        self.renderer = GCRenderer( window = window, dc = dc, native_window = native_window, native_dc = native_dc, wx_renderer = wx_renderer, double_buffered = double_buffered )
        self.window = window
        
        self.model_kinds = [ 'Rectangle', 'Circle', 'Ellipse', 'Text' ]
        self.primitive_kinds = [ 'Rectangle', 'Ellipse', 'Text' ]

        self._setupRegistries()
        self._setupNodeFactory()
        self._setupAdapters()
        self.updatePolicy = DefaultUpdatePolicy( self, max_update_delay )
        self.subscribe( self.onDirty, 'attribChanged' )

        #self.renderPolicy = DefaultRenderPolicy()
        self.renderPolicy = CullingRenderPolicy()
        
    def _setupRegistries(self):
        
        self.adapterRegistry = adapterRegistry = AdapterRegistry()
        
        self.primitiveRendererRegistry = PrimitiveRendererRegistry( adapterRegistry )
        self.viewRegistry = ViewRegistry( adapterRegistry )
        self.renderNodeRegistry = RenderNodeRegistry( adapterRegistry )
        
        for primitive_kind in self.primitive_kinds:
            modelInterface = getattr(models, 'I%s' % primitive_kind)
            primitiveRendererType = getattr(views, 'Default%sRenderer' % primitive_kind)
            self.primitiveRendererRegistry.register( modelInterface, primitiveRendererType )
            
        for model_kind in self.model_kinds:
            modelInterface = getattr(models, 'I%s' % model_kind)
            def createDefaultView(model, look, scaled):
                primitiveRendererConstructor, model = self.primitiveRendererRegistry.getRendererConstructor( model )
                primitiveRenderer = primitiveRendererConstructor( self.renderer, model, look, scaled )
                return observables.ObservableDefaultView( look, primitiveRenderer )
            self.viewRegistry.register( modelInterface, createDefaultView )
            
        for model_kind in self.model_kinds:
            modelInterface = getattr(models, 'I%s' % model_kind)
            def createDefaultRenderableNode(model, transform, look, scaled, name):
                viewConstructor, model = self.viewRegistry.getViewConstructor( model )
                view = viewConstructor( model = model, look = look, scaled = scaled )
                renderNode = observables.ObservableDefaultRenderableNode( model, view, transform, name = name )
                return renderNode
            self.renderNodeRegistry.register( modelInterface, createDefaultRenderableNode )
        
        
    def _setupAdapters(self):
        for (from_interface, to_interface, adapter) in defaultAdapters:
            self.adapterRegistry.register( from_interface, to_interface, adapter )

        
    def _setupNodeFactory(self):
        self.nodeFactory = FactoryUsingDict()
        self.create = self.nodeFactory.create
        self.registerNode = self.nodeFactory.register
        self.unregisterNode = self.nodeFactory.unregister
        self.isNodeRegistered = self.nodeFactory.is_registered
        
       
        keywords = { 'transform'    : None,
                     'pos'          : None,
                     'position'     : None,
                     'rotation'     : None,
                     'scale'        : None,
                     'look'         : None,
                     'where'        : 'back',
                     'scaled'       : True,
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

                scaled = get_keyword(keys, 'scaled')

                renderNodeConstructor, model = self.renderNodeRegistry.getRenderNodeConstructor( model )
                renderNode = renderNodeConstructor( model, transform = transform, look = look, name = keys.get('name', '<unnamed node>'), scaled = scaled )

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
