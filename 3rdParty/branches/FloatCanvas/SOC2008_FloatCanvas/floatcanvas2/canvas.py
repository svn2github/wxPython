from camera import Camera
from node import Node
from gcrenderer import GCRenderer
from patterns.factory import FactoryUsingDict
from renderableNode import DefaultRenderableNode

class Canvas(DefaultRenderableNode):
    pass
    #def __init__(self, *args, **keys):
    #    Node.__init__(self, *args, **keys)


class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, *args, **keys):
        Canvas.__init__(self, None, None, *args, **keys)
        
        self.camera = Camera()
        self.renderer = GCRenderer( window = window, dc = dc, native_window = native_window, native_dc = native_dc, wx_renderer = wx_renderer )
        
        self._setupNodeFactory()

    def _setupNodeFactory(self):
        self.nodeFactory = FactoryUsingDict()
        self.create = self.nodeFactory.create
        self.registerNode = self.nodeFactory.register
        self.unregisterNode = self.nodeFactory.unregister
        self.isNodeRegistered = self.nodeFactory.is_registered

        import models
        import views
        from views import DefaultView, DefaultRectangleRenderer
        from look import SolidColourLook, NoLook
        from patterns.partial import partial
        import transform as transformModule

        kinds = [ 'Rectangle' ]
        
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
        
        for kind in kinds:
            def create(modelType, primitiveRendererType, *args, **keys):
                model = modelType( *args )
                primitiveRenderer = primitiveRendererType()
                                
                look = get_keyword(keys, 'look')
                if look is None:
                    raise ValueError( 'You need to supply a look! Use look.NoLook or "nolook" if you want none.')
                if look == 'nolook':
                    look = NoLook
                if isinstance(look, (tuple, list)):
                    look = SolidColourLook(*look)
                                        
                where = get_keyword(keys, 'where')
                transform = get_keyword(keys, 'transform')
                if transform is None:
                    transform = transformModule.LinearTransform2D()
                elif isinstance( transform, basestring ):
                    transform = getattr(transformModule, transform)()

                pos = get_keyword(keys, 'pos') or get_keyword(keys, 'position')
                if pos is not None:
                    # assume linear transform
                    transform.position = pos
                    
                rotation = get_keyword(keys, 'rotation')
                if rotation is not None:
                    # assume linear transform
                    transform.rotation = rotation
                
                scale = get_keyword(keys, 'scale')
                if rotation is not None:
                    # assume linear transform
                    transform.scale = scale

                view = DefaultView( look, primitiveRenderer ) 
                node = DefaultRenderableNode( model, view, transform = transform )

                self.addChild( node, where = where )

                return node

            modelType = getattr(models, kind)
            primitiveRendererType = getattr(views, 'Default%sRenderer' % kind)

            self.registerNode( kind, create, modelType, primitiveRendererType )
            setattr( self, 'create%s' % kind, partial( create, modelType, primitiveRendererType ) )
        

    def DoRender(self, renderer):
        pass
    
    def Render(self):
        super(SimpleCanvas, self).Render(self.renderer)

