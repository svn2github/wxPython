''' A canvas which provides default implementations for various things.
    This is basically the most important one of all the canvasses.
'''

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

class SimpleCanvas(Canvas):
    ''' I provide an various methods for a functional canvas.
        This includes registries so I can create according nodes/views/
        primitive renderers when given a model.
        I also provide a bunch of default models (and know how to map them
        to their views).
        I provide a default camera.
        Rendering and updates can be customized with policies.
        Other things I do include: zooming, screen shots, hit-testing, adapter
        registry. 
    '''

    def __init__(self, renderer, max_update_delay = 0.2, *args, **keys):
        ''' Inits this canvas.
            Things setupped: background color, default camera, node factory,
            model/view/primitve renderer registries, adapter registry and
            render/update policies.
        '''
        
        if 'name' not in keys:
            keys['name'] = 'unnamed canvas'

        self.renderer = renderer

        if 'backgroundColor' in keys:
            self.backgroundColor = keys['backgroundColor']
            del keys['backgroundColor']
        else:
            self.backgroundColor = None
        
        if 'renderPolicy' in keys:
            self.renderPolicy = keys['renderPolicy']
            del keys['renderPolicy']
        else:
            #self.renderPolicy = DefaultRenderPolicy()
            self.renderPolicy = CullingRenderPolicy()

        Canvas.__init__(self, self.renderer, False, None, None, None, None, observables.ObservableLinearTransform2D(), *args, **keys)
               
        self.camera = observables.ObservableCamera( observables.ObservableLinearTransform2D(), name = 'default camera' )
        self.addChild( self.camera )
        
        self.model_kinds = [ 'Rectangle', 'RoundedRectangle', 'Circle', 'Ellipse', 'Arc', 'Text', 'Line', 'LineLength', 'Lines', 'LinesList', 'LineSegments', 'LineSegmentsSeparate', 'Bitmap', 'CubicSpline', 'QuadraticSpline', 'Polygon', 'PolygonList', 'Arrow', 'AngleArrow' ]
        self.primitive_kinds = [ 'Rectangle', 'RoundedRectangle', 'Ellipse', 'Arc', 'Text', 'LinesList', 'LineSegmentsSeparate', 'Bitmap', 'CubicSpline', 'QuadraticSpline', 'PolygonList', 'Arrow' ]

        self._setupRegistries()
        self._setupNodeFactory()
        self._setupAdapters()

        if 'updatePolicy' in keys:
            self.updatePolicy = keys['updatePolicy']
            del keys['updatePolicy']
        else:
            self.updatePolicy = DefaultUpdatePolicy( self, max_update_delay )

        
        self.subscribe( self.onDirty, 'attribChanged' )


    def _setupRegistries(self):
        ''' Setups the registries. First one is the adapter registry which
            has all the information how models can be adapted to different
            interfaces.
            The other registries know how to map a model interface to a node()
            view/primitive renderer.
            They're fed with the default objects (all kinds of models, primitive
            renderers, ...)
            Finally, there's the serialization registry where you can register
            serializers for nodes.
        '''
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
                primitiveRenderer = primitiveRendererConstructor()
                primitiveRenderer = observables.ObservableBaseRenderer( self.renderer, look, model, primitiveRenderer, scaled )
                return observables.ObservableDefaultView( look, primitiveRenderer )
            self.viewRegistry.register( modelInterface, createDefaultView )
            
        for model_kind in self.model_kinds:
            modelInterface = getattr(models, 'I%s' % model_kind)
            def createDefaultRenderableNode(model, transform, look, scaled, name, render_to_surface, surface_size, filter):
                viewConstructor, model = self.viewRegistry.getViewConstructor( model )
                view = viewConstructor( model = model, look = look, scaled = scaled )
                renderNode = observables.ObservableDefaultRenderableNode( self.renderer, render_to_surface, surface_size, model, view, filter, transform, name = name )
                return renderNode
            self.renderNodeRegistry.register( modelInterface, createDefaultRenderableNode )        


        # create serialization registries
        self.serializerRegistry = FactoryUsingDict()
        self.unserializerRegistry = FactoryUsingDict()

        def createNativeSerializer():
            # import those two here, because they might need to import the simpleCanvas module itself
            # so importing here avoids a circular dependency
            from ..serialization.serializer import Serializer
            from ..serialization import defaultSerializers
            serializer = Serializer()
            defaultSerializers.registerDefaultSerializers( serializer.nodeSerializerRegistry )
            return serializer

        # register our native serializer and unserializer here
        self.serializerRegistry.register( 'fcsf', createNativeSerializer )
        self.unserializerRegistry.register( 'fcsf', createNativeSerializer )
        
        def createSvgSerializer():
            # import those two here, because they might need to import the simpleCanvas module itself
            # so importing here avoids a circular dependency
            from ..serialization.svg import SVGExporter
            from ..serialization.svg import defaultSVGSerializers
            serializer = SVGExporter( self.adapterRegistry )
            defaultSVGSerializers.registerDefaultSVGSerializers( serializer.elementCreatorRegistry )
            defaultSVGSerializers.registerDefaultNodeSerializers( serializer.nodeSerializerRegistry )

            # register the viewNodel-from-model connections to the svg exporter
            for model_kind in self.model_kinds:
                modelInterface = getattr(models, 'I%s' % model_kind)
                def createViewModel(model, look):
                    viewModelConstructor, model = self.primitiveRendererRegistry.getRendererConstructor( model )
                    viewModel = viewModelConstructor()
                    return viewModel, model
                serializer.viewModelCreatorRegistry.register( modelInterface, createViewModel )

            return serializer

        # register svg exporter, no importer defined        
        self.serializerRegistry.register( 'svg', createSvgSerializer )
        
        
    def _setupAdapters(self):
        ''' Internal. Feeds the adapter registries with the default model adapters '''
        for (from_interface, to_interface, adapter) in defaultAdapters:
            self.adapterRegistry.register( from_interface, to_interface, adapter )


    def create(self, *args, **keys):
        ''' Creates a node from a model. 
            Forwarded from nodeFactory.
        '''            
        return self.nodeFactory.create( *args, **keys )

    def registerNode(self, model_kind, create, modelType):
        ''' registers a node constructor for a model type.
            Forwarded from nodeFactory.
        '''
        setattr( self, 'create%s' % model_kind, partial( create, modelType ) )
        return self.nodeFactory.register( model_kind, create, modelType )

    def unregisterNode(self, *args, **keys):
        ''' unregisters a node constructor for a model type.
            Forwarded from nodeFactory.
        '''
        return self.nodeFactory.unregister( *args, **keys )

    def isNodeRegistered(self, *args, **keys):
        ''' is a node constructor for a model type registered?
            Forwarded from nodeFactory.
        '''
        return self.nodeFactory.is_registered( *args, **keys )
    
    def createFromModel(self, model, **keys):
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
                     'filter'               : None,
                     'parent'               : self,
                   }
        
        def get_keyword(dikt, name):
            return dikt.pop( name, keywords[name] )

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

        filter = get_keyword(keys, 'filter')

        if not model is None:
            look = get_keyword(keys, 'look')
            if look is None:
                raise ValueError( 'You need to supply a look! Use look.NoLook or "nolook" if you want none.')
            if look == 'nolook':
                look = NoLook
            if isinstance(look, (tuple, list)):
                look = observables.ObservableSolidColourLook(*look)

            renderNodeConstructor, model = self.renderNodeRegistry.getRenderNodeConstructor( model )
            renderNode = renderNodeConstructor( model, transform = transform, look = look, name = keys.get('name', '<unnamed node>'), scaled = scaled, render_to_surface = render_to_surface, surface_size = surface_size, filter = filter )
        else:
            renderNode = observables.ObservableDefaultRenderableNode( self.renderer, render_to_surface, surface_size, None, None, filter, transform = transform, name = keys.get('name', '<unnamed node>') )

        parent.addChild( renderNode, where = where )

        return renderNode        
        
    def _setupNodeFactory(self):
        ''' Internal. Sets up the node factory. The keyword argument for the
            create method is done here, as well as adding the createRectangle,
            create* methods to self.
        '''
        self.nodeFactory = FactoryUsingDict()        
               
        def create(modelType, *args, **keys):                                       
            model = modelType( *args )
            return self.createFromModel( model, **keys )
                
        for model_kind in self.model_kinds:
            modelType = getattr(observables, 'Observable%s' % model_kind)
            self.registerNode( model_kind, create, modelType )
        
        # the group node is a special one, it doesn't need any model
        self.registerNode( 'Group', self.createFromModel, None )

    def onDirty(self, evt):
        ''' If we're dirty, tell the update policy '''
        if self.dirty:
            self.updatePolicy.onDirty()

    def DoRender(self, renderer, camera):
        ''' The canvas itself doesn't have to render anything '''
        pass
    
    def Render(self, backgroundColor = None, camera = None, renderChildren = True):
        ''' Render all objects on the canvas with camera. By default the default
            camera is used.
            Calls the render policy.
        '''
        backgroundColor = backgroundColor or self.backgroundColor or 'green'
        if camera is None:
            camera = self.camera
        self.renderPolicy.render(self, camera, backgroundColor)
        camera.dirty = False
        camera.transform.dirty = False
        self.dirty = False
        self._children.dirty = False
        
    def zoomToExtents(self, boundingBox = None, padding_percent = 0.05, maintain_aspect_ratio = True):
        ''' Tells the default camera to fit the entire canvas nodes on the
            screen.
        '''
        if boundingBox is None:
            boundingBox = self.boundingBoxRecursive #self.rtree.boundingBox
            
        self.camera.zoomToExtents( boundingBox, padding_percent, maintain_aspect_ratio )
        
    def zoom(self, factor, center = None, centerCoords = 'world', alignment = 'cc'):
        ''' Zooms and possibly recenters the default camera on the canvas. The
            center coordinates can be given in 'world' and 'pixel' coordinates.
            Todo: Make alignment work. This specifies how to zoom (for example
            should the left upper corner stay the same and the rest is zoomed).
            Todo: Make the world/pixel a property of the coordinate. Then we can
                  do something like center.world() which retrieves the
                  coordinate in world units, no matter if it was in pixel
                  or world coordinates before.
        '''
        self.camera.zoom *= factor
        
        if not center is None:
            if centerCoords == 'pixel':
                center = self.pointToWorld( center )
            self.camera.position = center
        
        
    def pointToWorld(self, screen_pnt):
        ''' Transform a point on screen to world coordinates (if possible) '''
        return self.camera.viewTransform.inverse( (screen_pnt,) )[0]

    def hitTest( self, screen_pnt, exact = True, order = True ):
        ''' Performs a hit test given a point on screen.
            For the meaning of the exact parameter, see the performSpatialQuery
            function.
        '''
        world_pnt = self.pointToWorld( screen_pnt )
        query = QueryWithPrimitive( primitive = boundingBox.fromPoint( world_pnt ), exact = exact )
        pickedNodes = self.performSpatialQuery( query, order = order )
        
        return pickedNodes


    def getScreenshot(self, file_format):
        ''' Returns the rendered picture as a string with file_format, where
            file format can be something like 'png', 'jpg' or 'raw' or any other
            kind of supported image format.
        '''
        return self.renderer.getScreenshot( file_format )
    
    def saveScreenshot(self, filename):
        ''' Saves the rendered picture as a file to disk '''
        import os.path        
        extension = os.path.splitext(filename)[1][1:]
        data = self.getScreenshot( extension )
        f = file( filename, 'wb' )
        f.write( data )
        f.close()
        
        
    def _getScreenSize(self):
        return self.renderer.framebuffer.size
    
    def _setScreenSize(self, size):
        self.renderer.framebuffer.size = size
        
    screen_size = property( _getScreenSize, _setScreenSize )
    
    
    def serialize(self, format):
        serializer = self.serializerRegistry.create( format )
        return serializer.serialize( self, self.camera )
    
    def unserialize(self, data, format):
        unserializer = self.unserializerRegistry.create( format )
        return unserializer.unserialize( self, data )
           
    def serializeToFile(self, filename, format = None):
        if format is None:  # auto-detect by filename extension
            import os.path        
            format = os.path.splitext( filename )[1][1:].lower()
            
        data = self.serialize( format )
        
        f = file( filename, 'wb' )
        f.write( data )
        f.close()        
        return data
     
    def unserializeFromFile(self, filename, format = None):
        if format is None:  # auto-detect by filename extension
            import os.path        
            format = os.path.splitext( filename )[1][1:].lower()

        f = file( filename, 'rb' )
        data = f.read()
        f.close()        
        return self.unserialize( data, format )
    
    def destroy(self):
        self.updatePolicy.stop()

    # todo: need to revisit this, maybe allow NodesWithBounds to return None 
    def _getBoundingBox(self):
        return boundingBox.BoundingBox( [ (0,0), (0,0) ] )
    
    boundingBox = property( _getBoundingBox )
    
    def _getLocalBoundingBox(self):
        return boundingBox.BoundingBox( [ (0,0), (0,0) ] )
    
    localBoundingBox = property( _getLocalBoundingBox )
    
    