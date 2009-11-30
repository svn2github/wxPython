class ScreenRelativeController(object):
    def __init__(self, camera):
        self.camera = camera
        self.nodes = []

    def addNode( self, node, paramsToControl = ('position', 'scale', 'rotation'), useOffset = True, rescaleOnResize = False ):
        offset = self.camera.transform.inverse * node.transform if useOffset else fc.LinearTransform2D()
        self.nodes.append( (node, offset, paramsToControl, rescaleOnResize) )

    def update(self):
        for (node, offset, paramsToControl, rescaleOnResize) in self.nodes:
            transform = self.camera.transform * offset
                
            if 'scale' in paramsToControl:
                node.scale = transform.scale
            if 'position' in paramsToControl:
                node.position = transform.position
            if 'rotation' in paramsToControl:
                node.rotation = transform.rotation

    def onSize(self, evt):
        for (node, offset, paramsToControl, rescaleOnResize) in self.nodes:
            if rescaleOnResize:
                offset.scale *= evt.newSize / evt.oldSize
