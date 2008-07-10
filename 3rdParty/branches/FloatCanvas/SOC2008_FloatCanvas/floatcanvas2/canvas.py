from camera import Camera
from node import Node
from gcrenderer import GCRenderer
from patterns.factory import FactoryUsingDict

class Canvas(Node):
    def __init__(self, *args, **keys):
        Node.__init__(self, *args, **keys)


class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, *args, **keys):
        Canvas.__init__(self, *args, **keys)
        
        self.camera = Camera()
        self.renderer = GCRenderer( window = window, dc = dc, native_window = native_window, native_dc = native_dc, wx_renderer = wx_renderer )
        
        self._setupNodeFactory()

    def _setupNodeFactory(self):
        self.nodeFactory = FactoryUsingDict()
        self.create = self.nodeFactory.create
        self.registerNode = self.nodeFactory.register
        self.unregisterNode = self.nodeFactory.unregister
        self.isNodeRegistered = self.nodeFactory.is_registered

        from renderableNode import DefaultRenderableNode

        from models import Rectangle
        from views import DefaultView, DefaultRectangleRenderer
        from look import DefaultLook, NoLook
        from patterns.partial import partial

        kinds = [ 'Rectangle' ]
        for kind in kinds:
            def create(modelType, primitiveRendererType, *args, **keys):
                model = modelType( *args )
                primitiveRenderer = primitiveRendererType()

                try:
                    keys_look = keys['look']
                except KeyError:
                    look = NoLook
                else:
                    
                    if isinstance(keys_look, (tuple, list)):
                        look = DefaultLook(*keys_look)
                    else:
                        look = keys_look
                    del keys['look']
                        
                view = DefaultView( look, primitiveRenderer ) 
                node = DefaultRenderableNode( model, view, **keys )

                return node

            self.registerNode( kind, create, locals()[kind], locals()[ 'Default%sRenderer' % kind ] )

            setattr( self, 'create%s' % kind, partial( create, locals()[kind], locals()[ 'Default%sRenderer' % kind ] ) )
        


