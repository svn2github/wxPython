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
    # headFilled
    pass

class IAngleArrow(object):
    # startPoint, angle prop
    # length
    # headSize
    # headFilled
    pass

# fc1 objects:
# Polygon, Line, Spline, PointSet, Point, SquarePoint, Rectangle, Ellipse, Circle, Text, ScaledTextBox, Bitmap, Arc, Arrow, ArrowLine, DotGrid, PieChart
# remaining: Arrow, ArrowLine, PieChart, DotGrid, scaled variants
# actually implemented: Line, Rectangle, Ellipse, Circle, Text, Bitmap, Arc, Spline, 
# actually missing: Polygon, 