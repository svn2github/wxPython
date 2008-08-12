"""
A Panel that includes the FloatCanvas and Navigation controls

"""

import wx
import floatCanvas
from ..timeMachine import Resources
import guiMode
from ..patterns.partial import partial


class GUIModeDescription(object):
    def __init__(self, name, guiMode, bitmap):
        self.name = name
        self.guiMode = guiMode
        self.bitmap = bitmap


class NavCanvas(floatCanvas.FloatCanvas):
    """
    NavCanvas.py

    This is a high level window that encloses the FloatCanvas in a panel
    and adds a Navigation toolbar.

    """

    def __init__(self,
                   parent,
                   id = wx.ID_ANY,
                   size = wx.DefaultSize,
                   **kwargs): # The rest just get passed into FloatCanvas
        
        self.mainPanel = wx.Panel(parent, id, size=size)

        modes = [ ( 'Pointer',  guiMode.GUIModeMouse(),   Resources.getPointerBitmap() ),
                  ( 'Zoom In',  guiMode.GUIModeZoomIn(),  Resources.getMagPlusBitmap() ),
                  ( 'Zoom Out', guiMode.GUIModeZoomOut(), Resources.getMagMinusBitmap() ),
                  ( 'Pan',      guiMode.GUIModeMove(),    Resources.getHandBitmap() ),
                ]
        
        self.mode_descriptions = [ GUIModeDescription(*mode_info) for mode_info in modes ]
        self.name_to_mode_description = dict( [ (mode_descr.name, mode_descr) for mode_descr in self.mode_descriptions ] )
        
        self.canvasPanel = canvasPanel = wx.Panel( self.mainPanel, wx.ID_ANY )
        
        floatCanvas.FloatCanvas.__init__( self, canvasPanel, **kwargs )

        self.BuildToolbar()
        ## Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add( self.ToolBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4 )
        box.Add( canvasPanel, 1, wx.GROW )
        self.mainPanel.SetSizerAndFit(box)

        self.active_mode = 'Pointer'

    def _setActiveMode(self, mode):
        try:
            mode = self.name_to_mode_description[mode].guiMode
        except KeyError:
            pass
        
        try:
            lastMode = self.active_mode
        except AttributeError:
            pass
        else:
            lastMode.Deactivate()
                
        self._activeMode = mode
        self._activeMode.Activate( self )
    
    def _getActiveMode(self):
        return self._activeMode
    
    active_mode = property( _getActiveMode, _setActiveMode )

    def BuildToolbar(self):
        """
        This is here so it can be over-ridden in a ssubclass, to add extra tools, etc
        """
        tb = wx.ToolBar(self.mainPanel)
        self.ToolBar = tb
        tb.SetToolBitmapSize((24,24))
        self.AddToolbarModeButtons(tb, self.mode_descriptions )
        self.AddToolbarZoomButton(tb)
        tb.Realize()

    def setMode(self, mode, evt):
        self.active_mode = mode

    def AddToolbarModeButtons(self, tb, mode_descriptions):
            
        for mode_descr in mode_descriptions:
            tool = tb.AddRadioTool( wx.ID_ANY, shortHelp = mode_descr.name, bitmap = mode_descr.bitmap )
            self.mainPanel.Bind( wx.EVT_TOOL, partial( self.setMode, mode_descr.name ), tool )

    def AddToolbarZoomButton(self, tb):
        tb.AddSeparator()

        def ZoomToFit(Event):
            self.zoomToExtents()
            self.canvasPanel.SetFocus() # Otherwise the focus stays on the Button, and wheel events are lost.

        self.ZoomButton = wx.Button(tb, label="Zoom To Fit")
        tb.AddControl(self.ZoomButton)
        self.ZoomButton.Bind(wx.EVT_BUTTON, ZoomToFit)