from ...math import numpy

def arrayFromImage(wx_img):
    img = wx_img

    w, h = img.GetWidth(), img.GetHeight()
    img_data = numpy.array( [ord(c) for c in img.GetDataBuffer()], dtype = 'B' ).reshape( (w, h, 3) )
    if not img.HasAlpha():
        return img_data
    else:
        data = numpy.empty( (w,h,4), 'B' )
        data[...,:3] = img_data
        data[...,3] = numpy.array( [ord(c) for c in img.GetAlphaBuffer()], dtype = 'B' ).reshape(w,h)
        return data
