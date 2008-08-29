filename = 'icons.py'

import glob
from wx.tools import img2py

files = glob.glob('*.png')

open(filename, 'w').close()

for i, file in enumerate( files ) :
    append = i > 0
    img2py.img2py( file, filename, append = append, catalog = True )
