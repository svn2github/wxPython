'''
This is the floatcanvas2 package.

See the Demo for what it can do, and how to use it. The Demo can be
found within the wxPython demo.

FloatCanvas2 is a high level tool for drawing different shapes with
various looks on a canvas. The user can navigate and manipulate these
objects interactively. It allows arbitrary coordinate transform to be
used.

The goal is to provide a convenient way to draw stuff on the screen
without having to deal with handling OnPaint events, converting to pixel
coordinates, knowing about wxWindows brushes, pens, and colors, etc. It
also provides virtually unlimited zooming and scrolling

It relies on NumPy, which is needed for speed and convenience. 

Bugs and Limitations: Lots: patches, fixes welcome

Copyright: Matthias Kesternich and Christopher Barker
License: Same as the version of wxPython you are using it with.

TRAC site for some docs and updates:
http://trac.paulmcnett.com/floatcanvas

SVN for latest code:
http://svn.wxwidgets.org/svn/wx/wxPython/3rdParty/FloatCanvas/

Mailing List:
http://paulmcnett.com/cgi-bin/mailman/listinfo/floatcanvas
'''

from floatcanvas import *
