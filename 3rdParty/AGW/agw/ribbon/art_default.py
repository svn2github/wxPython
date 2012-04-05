"""
:class:`~ribbon.art_default.RibbonDefaultArtProvider` is responsible for drawing all the components of the ribbon
interface using a Windows/Mac or AUI appearance.


Description
===========

This allows a ribbon bar to have a pluggable look-and-feel, while retaining the same
underlying behaviour. As a single art provider is used for all ribbon components, a
ribbon bar usually has a consistent (though unique) appearance.

By default, a :class:`~ribbon.bar.RibbonBar` uses an instance of a class called :class:`~ribbon.art_default.RibbonDefaultArtProvider`,
which resolves to :class:`~ribbon.art_aui.RibbonAUIArtProvider`, :class:`~ribbon.art_msw.RibbonMSWArtProvider`, or :class:`~ribbon.art_osx.RibbonOSXArtProvider`
- whichever is most appropriate to the current platform. These art providers are all
slightly configurable with regard to colours and fonts, but for larger modifications,
you can derive from one of these classes, or write a completely new art provider class.

Call :meth:`RibbonBar.SetArtProvider() <ribbon.bar.RibbonBar.SetArtProvider>` to change the art provider being used.


See Also
========

:class:`~ribbon.bar.RibbonBar`
"""

import wx

from art_msw import RibbonMSWArtProvider
from art_aui import RibbonAUIArtProvider
from art_osx import RibbonOSXArtProvider

if wx.Platform == "__WXMSW__":

    class RibbonDefaultArtProvider(RibbonMSWArtProvider):
        """ Default art provider on MSW. """

        def __init__(self, set_colour_scheme=True):

            RibbonMSWArtProvider.__init__(self, set_colour_scheme)


elif wx.Platform == "__WXGTK__":

    class RibbonDefaultArtProvider(RibbonAUIArtProvider):
        """ Default art provider on GTK. """

        def __init__(self):

            RibbonAUIArtProvider.__init__(self)


else:
    # MAC has still no art provider for a ribbon, so we'll use
    # The AUI one. Waiting for a RibbonOSXArtProvider :-D

    class RibbonDefaultArtProvider(RibbonOSXArtProvider):
        """ Default art provider on Mac. """

        def __init__(self):

            RibbonOSXArtProvider.__init__(self)

    
