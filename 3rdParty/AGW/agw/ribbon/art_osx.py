"""
L{RibbonOSXArtProvider} is responsible for drawing all the components of the ribbon
interface using an AUI-compatible appearance on Mac, because as of now there is no
customized version of the ribbon art provider to provide a more or less native look
on the Mac platform.


Description
===========

This allows a ribbon bar to have a pluggable look-and-feel, while retaining the same
underlying behaviour. As a single art provider is used for all ribbon components, a
ribbon bar usually has a consistent (though unique) appearance.

By default, a L{RibbonBar} uses an instance of a class called L{RibbonDefaultArtProvider},
which resolves to L{RibbonAUIArtProvider}, L{RibbonMSWArtProvider}, or L{RibbonOSXArtProvider}
- whichever is most appropriate to the current platform. These art providers are all
slightly configurable with regard to colours and fonts, but for larger modifications,
you can derive from one of these classes, or write a completely new art provider class.

Call L{RibbonBar.SetArtProvider} to change the art provider being used.


See Also
========

L{RibbonBar}
"""

import wx
from art_aui import RibbonAUIArtProvider

class RibbonOSXArtProvider(RibbonAUIArtProvider):

    pass

