import numpy
from convolution import Convolve

# taken from http://www.connellybarnes.com/code/python/filterfft
def gaussian(sigma=0.5, shape=None):
  """
  Gaussian kernel numpy array with given sigma and shape.

  The shape argument defaults to ceil(6*sigma).
  """
  sigma = max(abs(sigma), 1e-10)
  if shape is None:
    shape = max(int(6*sigma+0.5), 1)
  if not isinstance(shape, tuple):
    shape = (shape, shape)
  x = numpy.arange(-(shape[0]-1)/2.0, (shape[0]-1)/2.0+1e-8)
  y = numpy.arange(-(shape[1]-1)/2.0, (shape[1]-1)/2.0+1e-8)
  Kx = numpy.exp(-x**2/(2*sigma**2))
  Ky = numpy.exp(-y**2/(2*sigma**2))
  ans = numpy.outer(Kx, Ky) / (2.0*numpy.pi*sigma**2)
  return ans/sum(sum(ans))


def gaussian_blur(image, sigma, gauss_shape, method = 'fftreal'):
    kernel = gaussian( sigma, gauss_shape )    
    return Convolve(image, kernel, method)