try:
    import numpy
except ImportError:
    print "Please install the python module 'numpy' before using FloatCanvas!"
    raise

# for people who like structured namespaces
import events
import gcrenderer
import canvas
import look
import models
import node
import nodeVisitor
import renderableNode
import renderer

# for people who like flat namespaces
#from events import None
from gcrenderer import GCRenderer
from canvas import Canvas, SimpleCanvas
from look import Look, DefaultLook, SolidColourLook, OutlineLook, RadialGradientLook, LinearGradientLook
from models import IRectangle, ICircle, IEllipse, ILine, IPolygon, IPoints, ISpline, IText, \
                   Rectangle, Circle, Ellipse, Line, Polygon, Points, Spline, Text, \
                   DefaultModelEventSender
from node import Node
from nodeVisitor import NodeVisitor, TextTreeFormatVisitor, GetNodesAsFlatListVisitor, FindNodesByNamesVisitor
from renderableNode import RenderableNode

# backwards compatability
import timeMachine
from timeMachine import NavCanvas, FloatCanvas, Resources
