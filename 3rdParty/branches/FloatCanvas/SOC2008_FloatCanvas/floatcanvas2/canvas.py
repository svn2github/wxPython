import observables
#from camera import Camera
#from node import Node
from gcrenderer import GCRenderer
from patterns.factory import FactoryUsingDict
#from renderableNode import DefaultRenderableNode

class Canvas(observables.ObservableDefaultRenderableNode):
    pass
    #def __init__(self, *args, **keys):
    #    Node.__init__(self, *args, **keys)


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
            print 'RENDER', self.canvas._children[0].model.size, self.canvas._children[0].model
            self.canvas.Render()
            self.dirty = False


class SimpleCanvas(Canvas):
    ''' I provide an easy to use interface for a full-blown Canvas '''

    def __init__(self, window = None, dc = None, native_window = None, native_dc = None, wx_renderer = None, double_buffered = True, max_update_delay = 0.2, *args, **keys):
        if 'name' not in keys:
            keys['name'] = 'unnamed canvas'
        Canvas.__init__(self, observables.ObservableLinearTransform2D(), None, None, *args, **keys)
        
        self.camera = observables.ObservableCamera( observables.ObservableLinearTransform2D() )
        self.renderer = GCRenderer( window = window, dc = dc, native_window = native_window, native_dc = native_dc, wx_renderer = wx_renderer, double_buffered = double_buffered )
        self.window = window
        
        self._setupNodeFactory()
        self.updatePolicy = DefaultUpdatePolicy( self, max_update_delay )
        self.subscribe( self.onDirty, 'attribChanged' )

    def _setupNodeFactory(self):
        self.nodeFactory = FactoryUsingDict()
        self.create = self.nodeFactory.create
        self.registerNode = self.nodeFactory.register
        self.unregisterNode = self.nodeFactory.unregister
        self.isNodeRegistered = self.nodeFactory.is_registered

        #import models
        #import views
        #from look import SolidColourLook, NoLook            
        #import transform as transformModule
        
        from look import NoLook
        from patterns.partial import partial

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
                primitiveRenderer = primitiveRendererType( self.renderer, model )
                                
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
                if rotation is not None:
                    # assume linear transform
                    transform.scale = scale

                view = observables.ObservableDefaultView( look, primitiveRenderer ) 
                node = observables.ObservableDefaultRenderableNode( model, view, transform = transform, name = keys.get('name', '<unnamed node>') )

                self.addChild( node, where = where )

                return node

            #modelType = getattr(models, kind)
            #primitiveRendererType = getattr(views, 'Default%sRenderer' % kind)
            #
            #self.registerNode( kind, create, modelType, primitiveRendererType )
            modelType = getattr(observables, 'Observable%s' % kind)
            primitiveRendererType = getattr(observables, 'ObservableDefault%sRenderer' % kind)

            self.registerNode( kind, create, modelType, primitiveRendererType )
            setattr( self, 'create%s' % kind, partial( create, modelType, primitiveRendererType ) )
        

    def onDirty(self, evt):
        if self.dirty:
            self.updatePolicy.onDirty()

    def DoRender(self, renderer):
        pass
    
    def Render(self):
        self.renderer.Clear()
        cam_transform = self.camera.transform.inverse
        cam_transform.position += ( self.window.GetClientSize()[0] / 2, self.window.GetClientSize()[1] / 2 )
        self.transform = cam_transform
        super(SimpleCanvas, self).Render(self.renderer)
        self.renderer.Present()