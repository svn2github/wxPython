from canvas import Canvas
import observables
from ..patterns.adapter import AdapterRegistry
from ..patterns.factory import FactoryUsingDict
from registries import PrimitiveRendererRegistry, ViewRegistry, RenderNodeRegistry
from .. import models, views
from ..models import defaultAdapters
from ..looks import NoLook
from ..patterns.partial import partial
from updatePolicies import DefaultUpdatePolicy
from renderPolicies import CullingRenderPolicy, DefaultRenderPolicy
from ..math import boundingBox
from ..nodes.spatialQuery import QueryWithPrimitive
from ..nodes import EnumerateNodesVisitor


class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, renderer, max_update_delay = 0.2, *args, **keys):
        if 'name' not in keys:
            keys['name'] = 'unnamed canvas'

        self.renderer = renderer

        Canvas.__init__(self, self.renderer, False, None, None, None, observables.ObservableLinearTransform2D(), *args, **keys)
               
        self.camera = observables.ObservableCamera( observables.ObservableLinearTransform2D() )
        self.addChild( self.camera )
        
        self.model_kinds = [ 'Rectangle', 'RoundedRectangle', 'Circle', 'Ellipse', 'Arc', 'Text', 'Line', 'LineLength', 'Lines', 'LinesList', 'LineSegments', 'LineSegmentsSeparate', 'Bitmap', 'CubicSpline', 'QuadraticSpline', 'Polygon', 'PolygonList', 'Arrow', 'AngleArrow' ]
        self.primitive_kinds = [ 'Rectangle', 'RoundedRectangle', 'Ellipse', 'Arc', 'Text', 'LinesList', 'LineSegmentsSeparate', 'Bitmap', 'CubicSpline', 'QuadraticSpline', 'PolygonList', 'Arrow' ]

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
            primitiveRendererType = getattr(views, 'Default%sRenderer' % primitive_kind)
            modelInterface = primitiveRendererType.can_render
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
            def createDefaultRenderableNode(model, transform, look, scaled, name, render_to_surface, surface_size):
                viewConstructor, model = self.viewRegistry.getViewConstructor( model )
                view = viewConstructor( model = model, look = look, scaled = scaled )
                renderNode = observables.ObservableDefaultRenderableNode( self.renderer, render_to_surface, surface_size, model, view, transform, name = name )
                return renderNode
            self.renderNodeRegistry.register( modelInterface, createDefaultRenderableNode )
        
        
    def _setupAdapters(self):
        for (from_interface, to_interface, adapter) in defaultAdapters:
            self.adapterRegistry.register( from_interface, to_interface, adapter )


    def create(self, *args, **keys):
        return self.nodeFactory.create( *args, **keys )

    def registerNode(self, model_kind, create, modelType):
        setattr( self, 'create%s' % model_kind, partial( create, modelType ) )
        return self.nodeFactory.register( model_kind, create, modelType )

    def unregisterNode(self, *args, **keys):
        return self.nodeFactory.unregister( *args, **keys )

    def isNodeRegistered(self, *args, **keys):
        return self.nodeFactory.is_registered( *args, **keys )
        
    def _setupNodeFactory(self):
        self.nodeFactory = FactoryUsingDict()        
       
        keywords = { 'transform'            : None,
                     'pos'                  : None,
                     'position'             : None,
                     'rotation'             : None,
                     'scale'                : None,
                     'look'                 : None,
                     'where'                : 'back',
                     'scaled'               : True,
                     'render_to_surface'    : False,
                     'surface_size'         : (500, 500),
                     'parent'               : self,
                   }
        
        def get_keyword(dikt, name):
            result = dikt.get( name, keywords[name] )
            try:
                del dikt[name]
            except KeyError:
                pass
            return result
        
        def create(modelType, *args, **keys):                                       
            # node  & nodeWithTransform properties
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
            parent = get_keyword(keys, 'parent')


            # renderable node properties
            render_to_surface = get_keyword(keys, 'render_to_surface')
            surface_size = get_keyword(keys, 'surface_size')

            if not modelType is None:
                model = modelType( *args )

                look = get_keyword(keys, 'look')
                if look is None:
                    raise ValueError( 'You need to supply a look! Use look.NoLook or "nolook" if you want none.')
                if look == 'nolook':
                    look = NoLook
                if isinstance(look, (tuple, list)):
                    look = observables.ObservableSolidColourLook(*look)
    
    
                renderNodeConstructor, model = self.renderNodeRegistry.getRenderNodeConstructor( model )
                renderNode = renderNodeConstructor( model, transform = transform, look = look, name = keys.get('name', '<unnamed node>'), scaled = scaled, render_to_surface = render_to_surface, surface_size = surface_size )
            else:
                renderNode = observables.ObservableDefaultRenderableNode( self.renderer, render_to_surface, surface_size, None, None, transform = transform, name = keys.get('name', '<unnamed node>') )

            parent.addChild( renderNode, where = where )

            return renderNode
        
        
        for model_kind in self.model_kinds:
            modelType = getattr(observables, 'Observable%s' % model_kind)
            self.registerNode( model_kind, create, modelType )
        
        self.registerNode( 'Group', create, None )

    def onDirty(self, evt):
        if self.dirty:
            self.updatePolicy.onDirty()

    def DoRender(self, renderer, camera):
        pass
    
    def Render(self, backgroundColor = None, camera = None, renderChildren = True):
        if camera is None:
            camera = self.camera
        self.renderPolicy.render(self, camera, backgroundColor)
        camera.dirty = False
        camera.transform.dirty = False
        self.dirty = False
        self._children.dirty = False
        
    def zoomToExtents(self, boundingBox = None, padding_percent = 0.05, maintain_aspect_ratio = True):
        if boundingBox is None:
            boundingBox = self.boundingBoxRecursive #self.rtree.boundingBox
            
        self.camera.zoomToExtents( boundingBox, padding_percent, maintain_aspect_ratio )
        
    def zoom(self, factor, center = None, centerCoords = 'world', alignment = 'cc'):
        self.camera.zoom *= factor
        
        if not center is None:
            if centerCoords == 'pixel':
                center = self.pointToWorld( center )
            self.camera.position = center
        
        
    def pointToWorld(self, screen_pnt):
        return self.camera.viewTransform.inverse( (screen_pnt,) )

    def hitTest( self, screen_pnt, exact = True ):
        world_pnt = self.pointToWorld( screen_pnt )
        query = QueryWithPrimitive( primitive = boundingBox.fromPoint( world_pnt ), exact = exact )
        pickedNodes = self.performSpatialQuery( query )
        
        # now sort the picked nodes by their (render) order, nodes that appear
        # on top are first in the returned list
        env = EnumerateNodesVisitor()
        env.visit(self)        
        pickedNodes.sort( key = lambda node: env.getPosition(node) )
        
        return pickedNodes


    def getScreenshot(self, file_format):
        return self.renderer.getScreenshot( file_format )
    
    def saveScreenshot(self, filename):
        import os.path        
        extension = os.path.splitext(filename)[1][1:]
        data = self.getScreenshot( extension )
        f = file( filename, 'wb' )
        f.write( data )
        f.close()
        
        
        
    def _getBoundingBox(self):
        return boundingBox.BoundingBox( [ (0,0), (0,0) ] )
    
    boundingBox = property( _getBoundingBox )
    
    def _getLocalBoundingBox(self):
        return boundingBox.BoundingBox( [ (0,0), (0,0) ] )
    
    localBoundingBox = property( _getLocalBoundingBox )
    
    
    def _getScreenSize(self):
        return self.renderer.framebuffer.size
    
    def _setScreenSize(self, size):
        self.renderer.framebuffer.size = size
        
    screen_size = property( _getScreenSize, _setScreenSize )