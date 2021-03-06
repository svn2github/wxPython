'''
A special canvas that includes the FloatCanvas and Navigation controls on a
panel.
'''

import wx
import floatCanvas
from ..resources import Resources, navCanvasIcons
import guiMode
from ..patterns.partial import partial

def get_bitmap(module, name, size = None):
    image = getattr( module, 'get%sImage' % name )()
    if size is not None:
        image.Rescale( size[0], size[1] )
    return wx.BitmapFromImage( image )

class GUIModeDescription(object):
    ''' Little helper to hold info about a GUIMode '''
    def __init__(self, name, guiMode, bitmap):
        self.name = name
        self.guiMode = guiMode
        self.bitmap = bitmap


class NavCanvas(floatCanvas.FloatCanvas):
    '''
    This is a high level window that encloses the FloatCanvas in a panel
    and adds a Navigation toolbar.
    '''

    def __init__(self,
                   parent,
                   id = wx.ID_ANY,
                   size = wx.DefaultSize,
                   enableSaveLoadButtons = True,
                   showStatusBar = False,
                   **kwargs): # The rest just get passed into FloatCanvas
        
        self.mainPanel = wx.Panel(parent, id, size=size)

        self.toolSize = ( 24, 24 )

        modes = [ ( 'Pointer',  guiMode.GUIModeMouse(),           get_bitmap( Resources, 'Pointer', self.toolSize ) ),
                  ( 'Zoom In',  guiMode.GUIModeZoomIn(),          get_bitmap( navCanvasIcons, 'viewmag_plus', self.toolSize ) ),
                  ( 'Zoom Out', guiMode.GUIModeZoomOut(),         get_bitmap( navCanvasIcons, 'viewmag_minus', self.toolSize ) ),
                  ( 'Pan',      guiMode.GUIModeMove(),            get_bitmap( Resources, 'Hand', self.toolSize ) ),
                  ( 'Move',     guiMode.GUIModeMoveObjects(),     get_bitmap( navCanvasIcons, 'package_games_arcade', self.toolSize ) ),
                  ( 'Rotate',     guiMode.GUIModeRotateObjects(), get_bitmap( navCanvasIcons, 'designer', self.toolSize ) ),
                  ( 'Scale',     guiMode.GUIModeScaleObjects(),   get_bitmap( navCanvasIcons, 'viewmagfit', self.toolSize ) ),
                ]
        
        self.mode_descriptions = [ GUIModeDescription(*mode_info) for mode_info in modes ]
        self.name_to_mode_description = dict( [ (mode_descr.name, mode_descr) for mode_descr in self.mode_descriptions ] )


        self.canvasPanel = canvasPanel = wx.Panel( self.mainPanel, wx.ID_ANY )
        self.enableSaveLoadButtons = enableSaveLoadButtons
        self.BuildToolbar()
        ## Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add( self.ToolBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4 )
        box.Add( canvasPanel, 1, wx.GROW )

        if showStatusBar:  
            self.statusBar = wx.StatusBar( self.mainPanel )
            box.Add( self.statusBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4 )
            
        box.SetMinSize( parent.GetClientSize() )
        self.mainPanel.SetSizerAndFit(box)

        floatCanvas.FloatCanvas.__init__( self, canvasPanel, **kwargs )

        self.active_mode = 'Pointer'
        
        self.Bind( wx.EVT_WINDOW_DESTROY, self.OnDestroy )
        if showStatusBar:
            def updateStatusBar(event):
                self.statusBar.SetStatusText("Name | %s -- Coordinates | World: %s - Screen: %s - Local: %s" % ( event.node.name, event.coords.world, event.coords.screen, event.coords.local ), 0)
            self.subscribe( updateStatusBar, 'raw_input.move' )

    def _setActiveMode(self, mode):
        ''' Takes care of switching the active gui mode. '''
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
        ''' Build up the navigation toolbar. This is here so it can be over-ridden
        in a subclass, to add extra tools, etc
        '''
        tb = wx.ToolBar(self.mainPanel)
        self.ToolBar = tb
        tb.SetToolBitmapSize( self.toolSize )
        self.AddToolbarModeButtons(tb, self.mode_descriptions )
        self.AddToolbarZoomButtons(tb)
        if self.enableSaveLoadButtons:
            self.AddToolbarSaveLoadAndExportButtons(tb)
        self.AddToolbarRefreshButton(tb)
        tb.Realize()

    def setMode(self, mode, evt):
        self.active_mode = mode
        
    def _addTool(self, bitmap, short_help, handler):
        tool = self.ToolBar.AddSimpleTool( wx.ID_ANY, get_bitmap( navCanvasIcons, bitmap, self.toolSize ), short_help )
        self.mainPanel.Bind( wx.EVT_TOOL, handler, tool )

    def AddToolbarModeButtons(self, tb, mode_descriptions):
        ''' Add a button for each gui mode to the navigation toolbar '''
        for mode_descr in mode_descriptions:
            tool = tb.AddRadioTool( wx.ID_ANY, shortHelp = mode_descr.name, bitmap = mode_descr.bitmap )
            self.mainPanel.Bind( wx.EVT_TOOL, partial( self.setMode, mode_descr.name ), tool )

    def AddToolbarZoomButtons(self, tb):
        ''' Add the zoom buttons to the toolbar '''
        tb.AddSeparator()

        def ZoomToFit(Event):
            self.zoomToExtents()

        def Zoom1(Event):
            self.camera.zoom = (1, 1)

        self._addTool( 'view_nofullscreen', 'Zoom to fit', ZoomToFit )
        self._addTool( 'viewmag_one', 'Zoom 100%', Zoom1 )
        
    def AddToolbarSaveLoadAndExportButtons(self, tb):
        ''' Add the 'Save', 'Load', 'Export SVG' and 'Export Image' buttons to the toolbar '''
        tb.AddSeparator()

        img_wildcard = 'PNG (*.png)|*.png|'    \
                       'JPEG (*.jpg)|*.jpg|'   \
                       'Bitmap (*.bmp)|*.bmp'
        fc_wildcard = 'FloatCanvas Save File (*.fcsf)|*.fcsf'
        svg_wildcard = 'Scalable Vector Graphics (SVG) (*.svg)|*.svg'

    
        def getSaveFilename(wildcard, extensions):
            dlg = wx.FileDialog( None, wildcard = wildcard, style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT )
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                for extension in extensions:
                    if filename.lower().endswith( extension ):
                        return filename
                return filename + extensions[ dlg.GetFilterIndex() ]
                

        def onOpen(event):
            dlg = wx.FileDialog( None, wildcard = fc_wildcard, style = wx.OPEN | wx.FD_FILE_MUST_EXIST )
            if dlg.ShowModal() == wx.ID_OK:
                self.unserializeFromFile( dlg.GetPath() )

        def onSave(event):
            filename = getSaveFilename( fc_wildcard, ['.fcsf'] )
            if filename:
                self.serializeToFile( filename )

        def onExportImage(event):
            filename = getSaveFilename( img_wildcard, [ '.png', '.jpg', '.bmp' ] )
            if filename:
                self.saveScreenshot( filename )

        def onExportSVG(event):
            filename = getSaveFilename( svg_wildcard, ['.svg'] )
            if filename:
                self.serializeToFile( filename )
    

        self._addTool( 'fileopen', 'Open', onOpen )
        self._addTool( 'filesaveas', 'Save', onSave )
        self._addTool( 'thumbnail', 'Export Image', onExportImage )
        self._addTool( 'kig_doc', 'Export SVG', onExportSVG )

    def AddToolbarRefreshButton(self, tb):
        ''' Add a refresh button to the gui '''
        tb.AddSeparator()
        def onRefresh(event):
            self.Render()
        self._addTool( 'tool_restart', 'Refresh', onRefresh )

    def OnDestroy(self, evt):
        self.active_mode.Deactivate()
        self._activeMode = None
