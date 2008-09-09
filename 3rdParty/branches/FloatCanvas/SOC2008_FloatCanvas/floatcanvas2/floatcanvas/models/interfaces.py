''' An informal collection of interfaces. The comments indicate which properties
    or attributes an object implementing the interface is expected to have.
'''

class IRectangle(object):
    # size prop
    pass

class IRoundedRectangle(object):
    # size prop
    # radius prop
    pass
    

class ICircle(object):
    # radius prop
    pass

class IEllipse(object):
    # size prop
    pass

class IArc(object):
    # radius prop
    # startAngle, endAngle props
    # clockwise prop
    pass


class ICubicSpline(object):
    # points prop
    pass

class IQuadraticSpline(object):
    # points prop
    pass



class ILine(object):
    # start, end props
    pass

class ILineLength(object):
    # length prop
    pass

class ILines(object):
    # points prop
    pass

class ILinesList(object):
    # lines_list prop
    pass

class ILineSegments(object):
    # points prop
    pass

class ILineSegmentsSeparate(object):
    # startPoints prop
    # endPoints prop
    pass
    
    
class IPolygon(object):
    # points prop
    pass

class IPolygonList(object):
    # polygon_list prop
    pass


class IPoints(object):
    # points prop
    # shape prop
    # size prop
    pass


class IText(object):
    # text prop
    pass

class IBitmap(object):
    # pixels prop
    pass


class IArrow(object):
    # startPoint, endPoint props
    # headSize
    pass

class IAngleArrow(object):
    # startPoint, angle prop
    # length
    # headSize
    pass

# fc1 objects:
# Polygon, Line, Spline, PointSet, Point, SquarePoint, Rectangle, Ellipse, Circle, Text, ScaledTextBox, Bitmap, Arc, Arrow, ArrowLine, DotGrid, PieChart
# remaining: ArrowLine, PieChart, DotGrid, scaled variants
# not applicable: PointSet, Point, SquarePoint, because GC can't render a point
