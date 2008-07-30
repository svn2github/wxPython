try:
    import numpy
except ImportError:
    print "Please install the python module 'numpy' before using FloatCanvas!"
    raise

# for people who like structured namespaces
import canvas
import events
import looks
import math
import models
import nodes
import renderers
import views

# for people who like flat namespaces
from canvas import *
from events import *
from looks import *
from math import *
from models import *
from nodes import *
from renderers import *
from views import *
