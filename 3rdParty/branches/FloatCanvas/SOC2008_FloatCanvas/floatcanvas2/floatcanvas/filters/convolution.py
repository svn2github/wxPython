import numpy.fft

def ConvolveFFT(image1, image2, MinPad=True, pad=True, FFt = None, iFFt = None):
    """ Not so simple convolution """

    from numpy import log

    #Just for comfort:
    if FFt is None:
        FFt = numpy.fft.fft2
    if iFFt is None:
        iFFt = numpy.fft.ifft2

    #The size of the images:
    r1,c1 = image1.shape
    r2,c2 = image2.shape

    #MinPad results simpler padding,smaller images:
    if MinPad:
        r = r1+r2
        c = c1+c2
    else:
        #if the Numerical Recipies says so:
        r = 2*max(r1,r2)
        c = 2*max(c1,c2)
    
    #For nice FFT, we need the power of 2:
    if pad:
        pr2 = int(log(r)/log(2.0) + 1.0 )
        pc2 = int(log(c)/log(2.0) + 1.0 )
        rOrig = r
        cOrig = c
        r = 2**pr2
        c = 2**pc2
    #end of if pad

    #numpy fft has the padding built in, which can save us some steps
    #here. The thing is the s(hape) parameter:
    # fftimage = FFt(image1,s=(r,c)) * FFt(image2,s=(r,c))
    fftimage = FFt(image1, s=(r,c))*FFt(image2[::-1,::-1],s=(r,c))

    if pad:
        return (iFFt(fftimage))[:rOrig,:cOrig].real
    else:
        return (iFFt(fftimage)).real

from functools import partial
ConvolveFFTReal = partial( ConvolveFFT, FFt = numpy.fft.rfft2, iFFt = numpy.fft.irfft2 )


import numpy
def ConvolveDirect(image, kernel):
    # todo: center kernel around pixel, right now pixel is the upper left corner
    img_width, img_height, img_components = image.shape
    kernel_width, kernel_height = kernel.shape

    result_size = ( img_height + kernel_height, img_width + kernel_width )
    result = numpy.empty( result_size + (img_components,) )
    
    image = image.reshape( (img_height, img_width, img_components) )
    for y in range(kernel_height):
        for x in range(kernel_width):
            result[x:x+img_height,y:y+img_width] += image * kernel[x,y]

    return result.reshape( (img_width + kernel_width, img_height + kernel_height, img_components) )


cache = []

def Convolve(image, kernel, method):
    if method == 'fft' or method == 'fftreal':
        img_width, img_height, img_components = image.shape
        kernel_width, kernel_height = kernel.shape
    
        result_size = ( img_height + kernel_height, img_width + kernel_width )
        result = numpy.empty( result_size + (img_components,) )        
        
        if method == 'fft':
            func = ConvolveFFT
        else:
            func = ConvolveFFTReal
            
        for i in range(0,img_components):
            result[...,i] = func( image.reshape( (img_height, img_width, img_components) )[...,i], kernel, True, True )
            
        return result.reshape( (img_width + kernel_width, img_height + kernel_height, img_components) )
    elif method == 'fft2':
        img_width, img_height, img_components = image.shape    
        result = filter( image.reshape( (img_height, img_width, img_components) ), kernel, cache )            
        return result.reshape( (img_width, img_height, img_components) )
    elif method == 'direct':
        return ConvolveDirect( image, kernel )
    else:
        raise ValueError(method)


# taken from http://www.connellybarnes.com/code/python/filterfft
def filter(I, K, cache=None):
  """
  Filter image I with kernel K.

  Image color values outside I are set equal to the nearest border color on I.

  To filter many images of the same size with the same kernel more efficiently, use:

    >>> cache = []
    >>> filter(I1, K, cache)
    >>> filter(I2, K, cache)
    ...

  An even width filter is aligned by centering the filter window around each given
  output pixel and then rounding down the window extents in the x and y directions.
  """
  def roundup_pow2(x):
    y = 1
    while y < x:
      y *= 2
    return y

  I = numpy.asarray(I)
  K = numpy.asarray(K)

  if len(I.shape) == 3:
    s = I.shape[0:2]
    L = []
    ans = numpy.concatenate([filter(I[:,:,i], K, L).reshape(s+(1,))
                             for i in range(I.shape[2])], 2)
    return ans
  if len(K.shape) != 2:
    raise ValueError('kernel is not a 2D array')
  if len(I.shape) != 2:
    raise ValueError('image is not a 2D or 3D array')

  s = (roundup_pow2(K.shape[0] + I.shape[0] - 1),
       roundup_pow2(K.shape[1] + I.shape[1] - 1))
  Ipad = numpy.zeros(s)
  Ipad[0:I.shape[0], 0:I.shape[1]] = I

  if cache is not None and len(cache) != 0:
    (Kpad,) = cache
  else:
    Kpad = numpy.zeros(s)
    Kpad[0:K.shape[0], 0:K.shape[1]] = numpy.flipud(numpy.fliplr(K))
    Kpad = numpy.fft.rfft2(Kpad)
    if cache is not None:
      cache[:] = [Kpad]

  Ipad[I.shape[0]:I.shape[0]+(K.shape[0]-1)//2,:I.shape[1]] = I[I.shape[0]-1,:]
  Ipad[:I.shape[0],I.shape[1]:I.shape[1]+(K.shape[1]-1)//2] = I[:,I.shape[1]-1].reshape((I.shape[0],1))

  xoff = K.shape[0]-(K.shape[0]-1)//2-1
  yoff = K.shape[1]-(K.shape[1]-1)//2-1
  Ipad[Ipad.shape[0]-xoff:,:I.shape[1]] = I[0,:]
  Ipad[:I.shape[0],Ipad.shape[1]-yoff:] = I[:,0].reshape((I.shape[0],1))

  Ipad[I.shape[0]:I.shape[0]+(K.shape[0]-1)//2,I.shape[1]:I.shape[1]+(K.shape[1]-1)//2] = I[-1,-1]
  Ipad[Ipad.shape[0]-xoff:,I.shape[1]:I.shape[1]+(K.shape[1]-1)//2] = I[0,-1]
  Ipad[I.shape[0]:I.shape[0]+(K.shape[0]-1)//2,Ipad.shape[1]-yoff:] = I[-1,0]
  Ipad[Ipad.shape[0]-xoff:,Ipad.shape[1]-yoff:] = I[0,0]

  import time
  ans = numpy.fft.irfft2(numpy.fft.rfft2(Ipad) * Kpad, Ipad.shape)

  off = ((K.shape[0]-1)//2, (K.shape[1]-1)//2)
  ans = ans[off[0]:off[0]+I.shape[0],off[1]:off[1]+I.shape[1]]

  return ans