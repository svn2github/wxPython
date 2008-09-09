from ..models import IArrow
from ..math import numpy
from viewModel import ViewModel
from viewModelInterfaces import IArrowViewModel

class DefaultArrowRenderer(object):
    can_render = IArrow
    implements_interfaces = IArrowViewModel
    
    def getCoords(self, model):
        tip = model.endPoint
        arrow_dir = model.endPoint - model.startPoint
        arrow_dir = arrow_dir / numpy.sqrt( numpy.dot( arrow_dir, arrow_dir ) )   # normalize
        head_base = tip - arrow_dir * model.headSize[0]
        
        # get vector ortohogonal to arrow_dir
        orthogonal_vec = numpy.array( (arrow_dir[1], -arrow_dir[0]) )
        left = head_base + orthogonal_vec * model.headSize[1]
        right = head_base - orthogonal_vec * model.headSize[1]

        return [ model.startPoint, head_base, tip, left, right ]
           
    def getViewModel(self, model, coords):
        # ,- line -, ,-- head --,
        #
        #           + \
        #           |   \
        # ---------base  +    <-- tip
        #           |   /
        #           + /
        start, head_base, tip, left, right = coords
        
        line = ViewModel( 'LinesList', lines_list = [ numpy.array( (start, head_base) ) ] )
        head = ViewModel( 'LinesList', lines_list = [ numpy.array( (tip, right, left) ) ], close = True )
        
        return ViewModel( 'CompositeObject', subobjects = [line, head] )

