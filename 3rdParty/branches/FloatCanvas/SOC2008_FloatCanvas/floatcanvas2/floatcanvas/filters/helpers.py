from ..math import LinearTransform2D

def renderBitmap( pixels, surface_renderer_cam, world_camera, renderer, offset = (0,0), scale = (1,1) ):
    from ..views import BaseRenderer, DefaultBitmapRenderer
    from ..models.bitmap import Bitmap
    bitmap_model = Bitmap( pixels )
    render_view = BaseRenderer( renderer, look = None, model = bitmap_model, primitiveRenderer = DefaultBitmapRenderer() )
           
    # create the offset transform
    offsetTransform = LinearTransform2D()
    offsetTransform.translation = offset

    scaleTransform = LinearTransform2D()
    scaleTransform.scale = scale 

    render_view.transform = offsetTransform * surface_renderer_cam.transform * scaleTransform
        
    render_view.Render( world_camera )
    return render_view