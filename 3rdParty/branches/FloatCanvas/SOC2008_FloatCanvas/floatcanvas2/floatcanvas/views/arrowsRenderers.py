from baseRenderer import BaseRenderer
from ..models import IArrow
from ..math import numpy


class DefaultArrowRenderer(BaseRenderer):
    can_render = IArrow
    
    def doCalcCoords(self, model):
        tip = model.endPoint
        arrow_dir = model.endPoint - model.startPoint
        arrow_dir = arrow_dir / numpy.sqrt( numpy.dot( arrow_dir, arrow_dir ) )   # normalize
        head_base = tip - arrow_dir * model.headSize[0]
        
        # get vector ortohogonal to arrow_dir
        orthogonal_vec = numpy.array( (arrow_dir[1], -arrow_dir[0]) )
        left = head_base + orthogonal_vec * model.headSize[1]
        right = head_base - orthogonal_vec * model.headSize[1]

        return [ model.startPoint, head_base, tip, left, right ]
           
    def doCreate(self, renderer, coords):
        # ,- line -, ,-- head --,
        #
        #           + \
        #           |   \
        # ---------base  +    <-- tip
        #           |   /
        #           + /
        start, head_base, tip, left, right = coords
        
        line = renderer.CreateLinesList( [(start, head_base)] )
        head = renderer.CreateLinesList( [(tip, right, left)], True )
        
        return renderer.CreateCompositeRenderObject( [line, head] )

