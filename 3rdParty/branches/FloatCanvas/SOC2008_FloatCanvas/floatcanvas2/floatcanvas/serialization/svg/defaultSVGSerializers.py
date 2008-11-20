def escape(s):
    replacements = { '<' : '&lt;',
                     '>' : '&gt;',
                     '&' : '&amp;'
                   }
    
    result = str(s)
    for orig, new in replacements.items():
        result = result.replace(orig, new)
    return result
        

def serialize_transform(transform):
    if transform is not None:
        elems = ' '.join( [ str(n) for n in transform.matrix[ :-1, ... ].transpose().flat ] )
        return 'matrix( %s )' % (elems,)
    else:
        return ''


class SVGElement(object):
    def __init__(self, tag, children = [], content = '', **attributes):
        self.tag = tag
        self.attributes = attributes
        self.children = children
        self.content = content
        
    def getCode(self, identation_level = 0):                                 
        tab_size = 4
        identation_str = ' ' * tab_size * identation_level
        attrCode = ' '.join( [ '%s="%s"' % ( name, escape(value) ) for name, value in self.attributes.items() ] )
        if attrCode:
            attrCode = ' ' + attrCode

        if not self.children and not self.content:
            code = '<%s %s />' % ( self.tag, attrCode )
        else:            
            childrenCode = '\n'.join( child.getCode(identation_level + 1) for child in self.children )#
            if self.content:
                code = '<%s%s>%s%s</%s>' % ( self.tag, attrCode, escape(self.content), childrenCode, self.tag )
            else:
                code = '<%s%s>\n%s%s</%s>' % ( self.tag, attrCode, childrenCode, identation_str, self.tag )

        return identation_str + code + '\n'    
        

from ...math import numpy

class DefaultConverters(object):
    def convertRectangle(viewModel):
        return SVGElement( 'rect',                          
                           x      = viewModel.corner[0],
                           y      = viewModel.corner[1],
                           width  = viewModel.size[0],
                           height = viewModel.size[1]
                          )

    def convertRoundedRectangle(viewModel):
        return SVGElement( 'rect',                          
                           x      = viewModel.corner[0],
                           y      = viewModel.corner[1],
                           width  = viewModel.size[0],
                           height = viewModel.size[1],
                           rx     = viewModel.radius,
                           ry     = viewModel.radius
                          )

    def convertEllipse(viewModel):
        radius = viewModel.size / 2
        center = viewModel.corner + radius
        return SVGElement( 'ellipse',                          
                           cx      = center[0],
                           cy      = center[1],
                           rx      = radius[0],
                           ry      = radius[1]
                          )    

    def convertLinesList(viewModel):
        lines = []
        try:
            if viewModel.close:
                tag = 'polygon'
        except AttributeError:
            tag = 'polyline'
            
        for polyline in viewModel.lines_list:
            elem = SVGElement( tag,                          
                               points = ','.join( [ str(p) for p in list(polyline.flat) ] )
                              )
            lines.append( elem )
            
        return SVGElement( 'g', children = lines )
    
    def convertLineSegmentsSeparate(viewModel):
        lines = []
        for start, end in zip( viewModel.startPoints, viewModel.endPoints ):
            elem = SVGElement( 'line',                          
                               x1 = start[0],
                               y1 = start[1],
                               x2 = end[0],
                               y2 = end[1]
                              )
            lines.append( elem )
            
        return SVGElement( 'g', children = lines )
    
    def convertPolygonList(viewModel):
        polies = []
        for poly in viewModel.lines_list:
            elem = SVGElement( 'polygon',                          
                               points = ','.join( [ str(p) for p in list(poly.flat) ] )
                              )
            polies.append( elem )
            
        return SVGElement( 'g', children = polies )
    
    def convertBitmap(viewModel):
        import wx
        
        pixels = viewModel.pixels
        # convert pixels to png
        if isinstance( pixels, wx.Bitmap ):
            bitmap = pixels
            w, h = bitmap.GetWidth(), bitmap.GetHeight()
        elif isinstance( pixels, wx.Image ):
            bitmap = wx.BitmapFromImage( pixels )
            w, h = bitmap.GetWidth(), bitmap.GetHeight()
        else:
            w, h, components = pixels.shape
    
            if components == 3:
                bitmap = wx.BitmapFromBuffer(w, h, pixels)
            elif components == 4:                
                bitmap = wx.BitmapFromBufferRGBA(w, h, pixels)
            else:
                raise ValueError( 'pixels must be a 2d-array where each pixel has either 3 (RGB) or 4 (RGBA) components' )
        
        if not viewModel.use_real_size:
            w, h = 1, 1
            
        wximg = wx.ImageFromBitmap( bitmap )
        
        import cStringIO
        outputStream = cStringIO.StringIO()
        wximg.SaveStream( wx.OutputStream(outputStream), wx.BITMAP_TYPE_PNG )
        data = outputStream.getvalue()
        outputStream.close()
        
        import base64
        base64data = base64.b64encode( data )        
    
            
        elem = SVGElement( 'image', x = -w / 2.0, y = -h / 2.0, width = w, height = h )
        elem.attributes['xlink:href'] = 'data:image/png;base64,%s' % base64data
        
        return elem
    
    def convertArc(viewModel):
        from math import sin, cos
        center = viewModel.center
        radius = viewModel.radius
        cs = cos( viewModel.startAngle )
        ss = sin( viewModel.startAngle )
        ce = cos( viewModel.endAngle )
        se = sin( viewModel.endAngle )
        startPoint = center + radius * numpy.array( ( cs, ss ) )
        endPoint   = center + radius * numpy.array( ( ce, se ) )
        rotX = 0
        sweep_flag = viewModel.clockwise
        large_arc_flag = 0
        #if viewModel.clockwise:
        #    if viewModel.endAngle > viewModel.startAngle:
        #        large_arc_flag = 0
        #else:
        #    if viewModel.endAngle < viewModel.startAngle:
        #        large_arc_flag = 0

        path = 'M%f,%f A%f,%f %d %d %d %f,%f' % ( startPoint[0], startPoint[1], radius, radius, rotX, large_arc_flag, sweep_flag, endPoint[0], endPoint[1] )
        return SVGElement( 'path', d = path )    

    def convertQuadraticSpline(viewModel):
        p = viewModel.controlPoints
        path = 'm%f,%f q%f,%f %f,%f' % ( p[0][0], p[1][0], p[1][0], p[1][1], p[2][0], p[2][1] )
        return SVGElement( 'path', d = path )


    def convertCubicSpline(viewModel):
        p = viewModel.controlPoints
        path = 'm%f,%f c%f,%f %f,%f %f,%f' % ( p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1], p[3][0], p[3][1] )
        return SVGElement( 'path', d = path )
                           
    def convertText(viewModel):
        tspan = SVGElement( 'tspan', style = "baseline-shift:-25%", content = viewModel.text )
        return SVGElement( 'text', style = "text-anchor: middle", children = [tspan] )

    def convertCompositeObject(viewModel):
        subobjects = []
        for model in viewModel.subobjects:
            # todo: remove this hack and replace with real registry lookup
            subobject = getattr( DefaultConverters, 'convert%s' % model.kind ).im_func( model )
            subobjects.append( subobject  )
        return SVGElement( 'g', children = subobjects )
    
    globals()['zzz'] = convertCompositeObject
    
    def convertArrow(viewModel):
        return globals()['zzz'](viewModel)




class ChildrenSerializer(object):
    def serializeChildren(node, serializer):
        return [ serializer.serializeNode(child) for child in reversed(node.children) ]

    serializeChildren = staticmethod( serializeChildren )


class NodeSerializer(object):
    def serialize(node, serializer):        
        childrenData = ChildrenSerializer.serializeChildren( node, serializer )
        # no own data
        if node.name:
            descr_elem = SVGElement( 'descr', children = [], content = node.name )
            childrenData.insert( 0, descr_elem )
        return SVGElement( 'g', descr = node.name, children = childrenData )

    serialize = staticmethod( serialize )


class NodeWithTransformSerializer(object):
    def serialize(node, serializer):        
        element = NodeSerializer.serialize( node, serializer )
        element.attributes['transform'] = serialize_transform(node.localTransform)
        return element

    serialize = staticmethod( serialize )


class CameraSerializer(object):
    def serialize(node, serializer):        
        element = NodeWithTransformSerializer.serialize( node, serializer )#
        # node.viewport
        return element

    serialize = staticmethod( serialize )
    

class DefaultRenderableNodeSerializer(object):
    # this one takes a shortcut and doesn't serialize the view properly
    # instead it just remembers the model data and look and rebuilds everything
    # when loaded (of course the canvas registry setup should be the same when
    # loading and saving, so the same views are created).
    # If one was to properly do this, the view would have to be saved by itself
    # so it could be restored later.
    
    def parseLook(cls, look, element):
        # line -- line_colour, width = 1, style = 'solid', cap = 'round', join = 'round', dashes = None, stipple = None
        # fill -- solid -- colour
        #      -- radial -- origin, colour_origin, center_circle_end, radius, colour_end
        #      -- linear -- origin, colour_origin, end, colour_end
        # font -- size, family = 'default', style = 'normal', weight = 'normal', underlined = False, faceName = '', colour = 'black'
        # fillmode        

      
        def format_color_attrib( attrib_name, colour, dikt, attrib_name_opacity = None ):
            if attrib_name_opacity is None:
                attrib_name_opacity = '%s-opacity' % attrib_name

            if colour is None:
                dikt[ attrib_name_opacity ] = 0
                return
            
            if isinstance( colour, basestring ):    # if colour is a string
                dikt[ attrib_name ] = colour
                return
            
            elements = ','.join( [ str(e) for e in colour[0:3] ] )
            dikt[ attrib_name ] = 'rgb( %s )' % elements
            dikt[ attrib_name_opacity ] = colour[3] / 255.0
        
        ## font
        try:
            font_look = look.font_look
        except AttributeError:
            font_look = None
        # 'font-family'
        # 'font-style'        # 	normal | italic | oblique
        # 'font-weight'       #   normal | bold | bolder | lighter | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900
        # 'font-size'
        # fill="blue" stroke="red" stroke-width="1"
        if font_look:
            font_attrs = element.attributes
            font_attrs['font-family'] = font_look.family
            font_attrs['font-style'] = { 'slant' : 'oblique' }.get( font_look.style.lower(), font_look.style )
            font_attrs['font-weight'] = { 'light' : 'lighter' }.get( font_look.weight.lower(), font_look.weight )
            font_attrs['font-size'] = font_look.size
            if font_look.underlined:
                font_attrs['text-decoration'] = 'underline'
            format_color_attrib( 'fill', font_look.colour, font_attrs )
            return


        ## OUTLINES
        try:
            line_look = look.line_look
        except AttributeError:
            line_look = None
        line_attrs = element.attributes
        #'stroke' = line_look.line_colour[0:3]
        #'stroke-opacity' = line_look.line_colour[3]
        #'stroke-width' = line_look.width
        #'stroke-linecap' = line_look.cap            # 	butt | round | square
        #'stroke-linejoin' = line_look.join          # 	miter | round | bevel 
        #'stroke-dasharray' = line_look.dashes
        # todo: stipples
        if line_look is not None:
            format_color_attrib( 'stroke', line_look.line_colour, line_attrs )
            line_attrs[ 'stroke-width' ] = line_look.width
    
            cap_translation = { 'round' : 'round', 'butt' : 'butt', 'projecting' : 'square' }
            line_attrs[ 'stroke-linecap' ] = cap_translation[ line_look.cap ]
            line_attrs[ 'stroke-linejoin' ] = line_look.join
            
            dashes = line_look.dashes
            if line_look.style == 'dot':
                dashes = [1,1]
            elif line_look.style == 'long_dash':            
                dashes = [1.5,0.5]
                
            if dashes is not None:
                line_attrs[ 'stroke-dasharray' ] = ','.join( [str(d * 10) for d in dashes] )
                line_attrs[ 'stroke-linecap' ] = 'butt'
        
        ## FILL LOOKS
        # 'fill-rule' = 'evenodd'
        # 'fill' = fill_look.colour[0:3]
        # 'fill-opacity' = fill_look.colour[3]

        try:
            fill_look = look.fill_look
        except AttributeError:
            pass
        else:
            # todo: remove this name hack
            type_name = type(fill_look).__name__
            fill_attrs = { 'fill-rule' : 'evenodd' }
    
            if 'Solid' in type_name:
                format_color_attrib( 'fill', fill_look.colour, element.attributes )
            elif 'Gradient' in type_name:            
                stop1Elem = SVGElement( 'stop', offset = "0%" )
                format_color_attrib( 'stop-color', fill_look.colour_origin, stop1Elem.attributes, 'stop-opacity' )
                stop2Elem = SVGElement( 'stop', offset = "99.9999%" )
                format_color_attrib( 'stop-color', fill_look.colour_end, stop2Elem.attributes, 'stop-opacity' )
                stop3Elem = SVGElement( 'stop', offset = "100%" )
                stop3Elem.attributes['stop-opacity'] = 0
                
                id = cls.getUniqueId()
                
                if 'Linear' in type_name:
                    gradElem = SVGElement( 'linearGradient', [stop1Elem, stop2Elem, stop3Elem], id = id, spreadMethod = 'repeat',
                                            x1 = fill_look.origin[0], y1 = fill_look.origin[1],
                                            x2 = fill_look.end[0], y2 = fill_look.end[1],
                                          )
                elif 'Radial' in type_name:
                    gradElem = SVGElement( 'radialGradient', [stop1Elem, stop2Elem, stop3Elem], id = id, spreadMethod = 'pad',
                                            fx = fill_look.origin[0], fy = fill_look.origin[1], r = fill_look.radius,
                                            cx = fill_look.center_circle_end[0], cy = fill_look.center_circle_end[1],
                                          )
                else:
                    raise NotImplementedError()
                
                gradElem.attributes['gradientUnits'] = 'userSpaceOnUse'
                #gradElem.attributes['spreadMethod'] = 'pad'
                
                defsElement = SVGElement( 'defs', [gradElem] )
                element.children.insert( 1, defsElement )
                element.attributes['fill'] = 'url(#%s)' % id
            elif fill_look is None:
                element.attributes['fill-opacity'] = 0
            else:
                raise NotImplementedError(type_name)  
        
        # linear gradient
        # <linearGradient id="MyGradient">
        #     <stop offset="5%" stop-color="#F60" />
        #     <stop offset="95%" stop-color="#FF6" />
        # </linearGradient>        
        # 'spreadMethod' = 'repeat'      # pad | reflect | repeat
        # 'x1' = fill_look.origin[0]
        # 'y1' = fill_look.origin[1]
        # 'x2' = fill_look.end[0]
        # 'y2' = fill_look.end[1]      
        # stop offset="0%" stop-color = fill_look.colour_origin[0:3] stop-opacity = fill_look.colour_origin[3]
        # stop offset="100%" stop-color = fill_look.colour_end[0:3] stop-opacity = fill_look.colour_end[3]

        # radial gradient
        # <radialGradient id="MyGradient" gradientUnits="userSpaceOnUse"
        #              cx="400" cy="200" r="300" fx="400" fy="200">
        #    <stop offset="0%" stop-color="red" />
        #    <stop offset="50%" stop-color="blue" />
        #    <stop offset="100%" stop-color="red" />
        # </radialGradient>
        # 'spreadMethod' = 'reflect'      # pad | reflect | repeat
        # 'cx' = fill_look.center_circle_end[0]
        # 'cy' = fill_look.center_circle_end[1]
        # 'r' = fill_look.radius
        # 'fx' = fill_look.origin[0]
        # 'fy' = fill_look.origin[1]
        # stop offset="0%" stop-color = fill_look.colour_origin[0:3] stop-opacity = fill_look.colour_origin[3]
        # stop offset="100%" stop-color = fill_look.colour_end[0:3] stop-opacity = fill_look.colour_end[3]



    def serialize(cls, node, serializer):        
        #try:
        #    surface_size = node.surface.size
        #except AttributeError:
        #    surface_size = None

        #try:
        #    look = node.view.look
        #except AttributeError:
        #    look = None
        element = NodeWithTransformSerializer.serialize( node, serializer )
        if node.model is None:
            return element
        
        modelElement = serializer.convertModelToSVGElement( node.model, node.localTransform )
        element.attributes['transform'] = serialize_transform( modelElement.attributes['transform'] )
        del modelElement.attributes['transform']
        element.children.append( modelElement )
        #modelElement.children.remove( element )
        #print [c.tag for c in modelElement.children]

        #wrapperElement = SVGElement( 'g', children = [element], transform = element.attributes['transform'] )
        #modelElement.parent = element.parent
        #modelElement.children = modelElement.children + element.children
        
        if not node.shown:
            # or should we use the 'display' prop here?
            element.attributes['visibility'] = 'hidden'
            
        if node.view.look:
            cls.parseLook( node.view.look, element )
        
        return element       
        #node.render_to_surface, surface_size )


    serialize = classmethod( serialize )
    parseLook = classmethod( parseLook )
    
    
    currentId = 0
    def getUniqueId(cls):
        result = cls.currentId
        cls.currentId += 1
        return 'generatedId%d' % result
        
    getUniqueId = classmethod( getUniqueId )
    
    
class SimpleCanvasSerializer(object):
    def serialize(node, serializer):
        header = \
"""<?xml version="1.0"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
"""
        element = DefaultRenderableNodeSerializer.serialize( node, serializer )
        element.attributes['transform'] = serialize_transform( node.transform * serializer.camera.viewTransform )
        vp_size = serializer.camera.viewport.size
        topLevel = SVGElement( 'svg', children = [element], width = vp_size[0], height = vp_size[1], version = '1.1', xmlns = 'http://www.w3.org/2000/svg' )
        code = topLevel.getCode()
        #thisData = ( node.backgroundColor )
        return header + code


    serialize = staticmethod( serialize )





from ...views import viewModelInterfaces
def registerDefaultSVGSerializers( registry ):
    # register all default converters        
    for prop_name in dir(DefaultConverters):
        if prop_name.startswith( 'convert' ):
            kind = prop_name.replace( 'convert', '' )  # Rectangle, RoundedRectangle, ...
            viewModelInterface = getattr( viewModelInterfaces, 'I%sViewModel' % ( kind, ) )
            elementCreator = getattr( DefaultConverters, prop_name ).im_func
            registry.register( viewModelInterface, elementCreator )

def registerDefaultNodeSerializers( registry ):
    for entry in defaultSerializers:
        nodeType, serializer = entry
        registry.register( nodeType, serializer )


from ...nodes import DefaultRenderableNode, Camera, Node, NodeWithTransform
from ...canvas.navCanvas import NavCanvas
from ...canvas.simpleCanvas import SimpleCanvas
from ...canvas.floatCanvas import FloatCanvas
from ...canvas.observables import ObservableDefaultRenderableNode, ObservableCamera, ObservableNode, ObservableNodeWithTransform
from ...math import LinearTransform2D

defaultSerializers = [ 
                       (ObservableNode, NodeSerializer), (Node, NodeSerializer),
                       (ObservableNodeWithTransform, NodeWithTransformSerializer), (NodeWithTransform, NodeWithTransformSerializer),
                       (ObservableCamera, CameraSerializer), (Camera, CameraSerializer),
                       (ObservableDefaultRenderableNode, DefaultRenderableNodeSerializer), (DefaultRenderableNode, DefaultRenderableNodeSerializer),
                       (NavCanvas, SimpleCanvasSerializer), (FloatCanvas, SimpleCanvasSerializer), (SimpleCanvas, SimpleCanvasSerializer)
                     ]


