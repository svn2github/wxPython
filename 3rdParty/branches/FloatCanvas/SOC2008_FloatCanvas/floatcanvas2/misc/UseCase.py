# FlowerBed example
#
# situation: We are a company producing plastic flowers.
#            Our designers want a tool to visualize and design the flowers
#            and place them on a flower bed for illustrative purposed.
#            In the end our database should hold the necessary production
#            parameters needed to produce the flowers.
#            The visualization consists of two layers. The front one shows all
#            the labels with flower names, the back one is the actual flower
#            layer. For the sake of using a lot of features in this example
#            it will be drawn to a bitmap.
#
# not covered:
#
# - view serialization
# - single object on multiple canvasses
# - svg
# - bitmaps
# - animation
# - groups (although a layer can be conceived a group)
#

import FloatCanvas as fc

class ModelEventSender(object):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        fc.sendEvent( fc.events.modelChanged, self )


class FlowerBedModel(ModelEventSender, fc.IRectangleData):
    def __init__(self, name):
        self.name = name
        self.color = 'brown'
        self.flowers = []
        self.size = (100, 100)


class FlowerModel(ModelEventSender):
    def __init__(self, name, no_blades = 5, blade_colour = 'red', size = 10):
        self.name = name
        self.no_blades = no_blades
        self.blade_colour = blade_colour
        self.size = size


class SimpleFlowerRenderer(object):
    def Render(self, renderer, data):
        # draw the center part an dynamically generate and apply the look
        look = fc.DefaultLook( line_colour = 'black', fill_colour = data.blade_colour )
        renderer.ApplyLook( look )
        renderer.DrawCircle( (0,0), data.size )
        # draw a line per blade
        for blade in range(data.no_blades):
            x, y = sin(no_blades / blade * 2 * PI) * size, cos(no_blades / blade * 2 * PI) * size
            renderer.DrawLine( (0,0), (x,y) )

    def GetBoundingBox(self, data):
        return (data.size, data.size)


def loadFlowerbedModel():
    ''' stub for a flowerbed loading function. should really get data from
         a database '''
    bed = FlowerBedModel( 'Example bed' )

    # add some flowers
    flowers = [ FlowerModel( 'Tulip', 3 ),
                FlowerModel( 'Rose', 4, size = 20 ),
                FlowerModel( 'Sunflower', 10, 'yellow' ),
                FlowerModel( 'BoringDefault' )
              ]
    bed.flowers = flowers

    return bed

def createViewFromModel(flowerBed, canvas):
    flowerLayer = fc.BitmapLayerNode()              # this draws all its children into a bitmap, caches it and uses it for subsequent drawing, not sure if it should really be a node
    labelLayer = fc.WindowLayerNode()

    canvas.addChild( flowerLayer, where = 0 )
    canvas.addChild( labelLayer, where = fc.FRONT )
    
    genericFlowerRenderer = SimpleFlowerRenderer()
    labelRenderer = fc.defaultRenderers.ScaledTextRenderer()
    labelLook = fc.TextLook( base_size = 10, fill_colour = 'black' )

    # create flowers and their labels and a row
    for i, flowerData in enumerate(flowerBed.flowers):
        pos_x, pos_y = i % 5, i // 5    # put 5 flowers in a row
        pos_x *= 25
        pos_y *= 25
        
        flowerNode = fc.RenderableNode( flowerData, genericFlowerRenderer, fc.NoLook )          # use fc.NoLook since the flower renderer sets its own one
        flowerNode.transformer.translation = (pos_x, pos_y)                                     # the default transformer simply applies a 3x2 matrix
        labelLayer.addChild(flowerNode)

        labelNode = fc.RenderableNode( flowerData.name, labelRenderer, labelLook )
        labelNode.transformer.translation = (pos_x, pos_y + 15)                                   # put label a bit below the flower
        flowerLayer.addChild( labelNode )

    bed = fc.Rectangle( flowerBed )
    bed.enable = True       # just show the attribute, not strictly needed here
    flowerLayer.addChild( bed, where = fc.BACK )

    
    def customTransformer(node, coordinates):
        ''' square the coordinates for lack of imagniation of something more sensible '''
        return coordinates.x ** 2, coordinates.y ** 2
        
    bed.transformer = customTransformer

    def onClickFlower1(node, evt):
        node.data.size *= 2                                                   # change the data which will in turn change the view

    flower1 = flowerLayer.getChildren()[0]
    flower1.events.Bind( fc.events.LEFT_CLICK )                               # is flower1.Bind better here instead

    return flower1

   

flowerBed = loadFlowerbedModel()

renderer = fc.GCRenderer()
canvas = fc.Canvas()

flower1 = createViewFromModel( flowerBed, canvas )

# the default cam, looking at 500, 500
myCamera = fc.DefaultCamera( target = (500, 500), zoom = (1.0, 1.0) )
# a small inset in the upper left shows a zoomed area of the default cam
detailCamera = fc.DefaultCamera( target = (500, 500), zoom = (5.0, 5.0), viewport_rect = ( (0,0), (200,200) ) )

# this will be triggered whenever the canvas wants to redraw itself
def Render(canvas, evt):
    canvas.Render( renderer, myCamera )
    canvas.Render( renderer, detailCamera )

canvas.Bind( fc.events.renderCanvas, Render )

# now change the model a bit and see if the view catches it :-)
flowerBed.flowers[0].size *= 2

# move one of the objects, this should cause the object to send a fc.events.viewChanged message. This can then be caught by some controller to change the model.
flower1.transformer.Rotate( PI/4 )
