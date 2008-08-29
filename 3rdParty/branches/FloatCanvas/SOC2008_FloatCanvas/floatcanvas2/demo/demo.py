# parts borrowed from the wxPython demo

import wx
import wx.aui
import wx.html

import os.path

# Try importing floatcavanvas, if not possible use the local version
try:
    import wx.lib.floatcanvas.floatcanvas2
except ImportError:
    import sys
    sys.path.append( os.path.abspath('../../') )
    import floatcanvas2
    wx.lib.floatcanvas.floatcanvas2 = floatcanvas2
    sys.modules['wx.lib.floatcanvas.floatcanvas2'] = floatcanvas2

from codePanel import DemoCodePanel
import config

class FloatCanvasDemo(object):
    def __init__(self):
        pass

    def Run(self):
        self.app = app = wx.App(0)
        frame = MainFrame( None, 'FloatCanvas2 demo' )
        frame.Show()
        self.app.MainLoop()


import icons.icons

def get_bitmap(name):
    return icons.icons.catalog[name].GetBitmap()

def get_icon(name):
    return wx.IconFromBitmap( get_bitmap(name) )

class StdoutStderrHook(object):
    ''' Class to catch stdout and stderr and output it to our log window '''
    def __init__(self, stream, callback):
        self.stream = stream        
        self.callback = callback
        
    def write(self, data):
        self.callback( data )
        self.stream.write( data )


class MainFrame(wx.Frame):   
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size = (970, 720),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.SetMinSize( (640,480) )

        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel( self )
        self.pnl = pnl
        
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow( pnl )

        icons = wx.IconBundle()
        icon_sizes = [ 16, 22, 32, 64, 128 ]
        for size in icon_sizes:            
            icons.AddIcon( get_icon('kpaint%dx%d' % (size, size) ) )
        self.SetIcons( icons )
         
        self.Centre( wx.BOTH )
        #self.Maximize()
        self.CreateStatusBar( 1, wx.ST_SIZEGRIP )
        
        ## Create a Notebook
        self.notebook = notebook = wx.Notebook( pnl, -1, style = wx.CLIP_CHILDREN )
        imgList = wx.ImageList( 32, 32 )
        for pic in [ 'edu_miscellaneous32x32', 'source32x32', 'kpaint32x32']:
            imgList.Add( get_bitmap( pic ) )
        notebook.AssignImageList( imgList )
        
        ## Create a TreeCtrl
        leftPanel = wx.Panel( pnl, style = wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN )
        self.tree = DemoTree( leftPanel )

        self.overview_win = wx.html.HtmlWindow( notebook, -1, size = (400, 400) )
        def OnLinkClicked(evt):
            href = evt.GetLinkInfo().GetHref()
            if href.startswith( 'http://' ):
                wx.LaunchDefaultBrowser( href )
            else:
                evt.Skip()
        self.overview_win.Bind( wx.html.EVT_HTML_LINK_CLICKED, OnLinkClicked )
        notebook.AddPage( self.overview_win, 'Overview', imageId = 0 )
        
        if 'gtk2' in wx.PlatformInfo:
            self.overview_win.SetStandardFonts()
        
        ## Set up a log window
        self.log = wx.TextCtrl(pnl, -1, style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL )
        if wx.Platform == '__WXMAC__':
            self.log.MacCheckSpelling(False)
            
        # we catch stdout and stderr here and display it in our log window
        def addToLog(data):
            self.log.AppendText( data )
        sys.stdout = StdoutStderrHook( sys.stdout, addToLog )
        sys.stderr = StdoutStderrHook( sys.stderr, addToLog )

        # tree sizer
        leftBox = wx.BoxSizer(wx.VERTICAL)
        leftBox.Add(self.tree, 1, wx.EXPAND)
        leftPanel.SetSizer(leftBox)
        
        # select initial items
        notebook.SetSelection(0)
        
        self.populateTree()
        self.tree.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnTreeItemChosen )
        
        ## Use the aui manager to set up everything
        self.mgr.AddPane(notebook, wx.aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(leftPanel,
                         wx.aui.AuiPaneInfo().
                         Left().Layer(2).BestSize((280, -1)).
                         MinSize((160, -1)).
                         Floatable(False).FloatingSize((240, 700)).
                         Caption("FloatCanvas Demos").
                         CloseButton(False).
                         Name("DemoTree"))
        self.mgr.AddPane(self.log,
                         wx.aui.AuiPaneInfo().
                         Bottom().BestSize((-1, 150)).
                         MinSize((-1, 60)).
                         Floatable(False).FloatingSize((500, 160)).
                         Caption("Demo Log Messages").
                        CloseButton(False).
                         Name("LogWindow"))
        
        #self.auiConfigurations[DEFAULT_PERSPECTIVE] = self.mgr.SavePerspective()
        self.mgr.Update()
        
        self.mgr.SetFlags( self.mgr.GetFlags() ^ wx.aui.AUI_MGR_TRANSPARENT_DRAG )

    def SetOverview(self, name, text):
        self.curOverview = text
        lead = text[:6]    
        if 'html' not in text.lower():
            text = '<br>'.join(text.split('\n'))
        if wx.USE_UNICODE:
            text = text.decode('iso8859_1')
        self.overview_win.SetPage( text )
        #self.notebook.SetPageText(0, name)

    def populateTree(self):
        self.tree.SetItems( config.entries )
        self.ChooseItem( config.entries[0] )
        self.tree.ExpandAll()
        
    def OnTreeItemChosen(self, event):
        item = event.GetItem()
        entry = self.tree.GetPyData( item )
        if entry is None:
            return
        self.ChooseItem( entry )
        
    def ChooseItem( self, entry ):
        self.log.Clear()
        self.notebook.SetSelection(0)

        self.Freeze()
        
        try:
            self.DeleteNotebookPage(2)
            self.enableCodePage( False )
    
            overview_text = file( entry.text_filename, 'r' ).read()
            self.SetOverview( entry.name, overview_text )

            if entry.code_filename is not None:
                self.LoadDemo( entry )
        finally:
            self.Thaw()
        
    def enableCodePage(self, enable = True):
        if enable:
            self.codePage = DemoCodePanel( self.notebook, self )
            self.notebook.AddPage( self.codePage, 'Code', imageId = 1 )
        else:
            if 1 in range(0, self.notebook.PageCount):
                self.notebook.DeletePage( 1 )

       
    def LoadDemo(self, entry):        
        self.enableCodePage()

        code_file_content = file( entry.code_filename, 'r' ).read()
        self.codePage.LoadDemoSource( code_file_content )
        
        globals = {}
        old_dir = os.getcwd()
        code_dir = os.path.dirname( entry.code_filename )
        os.chdir( code_dir )
        try:
            #import sys
            #try:
            #    sys.path.insert( 0, code_dir )
            #    module = __import__( os.path.splitext( os.path.basename(entry.code_filename) )[0] )
            #finally:
            #    sys.path.remove( code_dir )
            
            code = compile( code_file_content, entry.code_filename, 'exec' )
            exec code in globals, globals
            
            self.DeleteNotebookPage(2)
            resultPanel = wx.Panel( self.notebook, -1 )        
            self.notebook.AddPage( resultPanel, 'Result', imageId = 2 )
            
            sizer = wx.BoxSizer( wx.VERTICAL )
    
            try:
                func = globals['run_demo']
            except KeyError:
                print 'Error. The demo needs to have a run_demo(app, panel) function!'
            else:
                try:       
                    func( wx.GetApp(), resultPanel )
                except:
                    raise
                else:
                    sizer.Add( resultPanel.Children[0], 1, wx.GROW )
                    resultPanel.SetSizerAndFit( sizer )
        
        finally:
            os.chdir( old_dir )
            
    def DeleteNotebookPage(self, no):
        if no in range(0, self.notebook.PageCount):
            self.notebook.DeletePage( no )


from wx.lib.mixins.treemixin import ExpansionState
class DemoTree(ExpansionState, wx.TreeCtrl):
    def __init__(self, *args, **keys):
        wx.TreeCtrl.__init__(self, *args, **keys)        
        self.imgList = wx.ImageList(16, 16)
        self.AssignImageList( self.imgList )
        
    def addIcon(self, name):
        # todo: prevent addition of duplicates
        icon = get_bitmap( name )
        img_index = self.imgList.Add( icon )
        return img_index

    def SetItems(self, items):        
        self.DeleteAllItems()
                
        self.AddRoot( 'FloatCanvas demos', image = self.addIcon( 'kpaint16x16' ) )

        category_name_to_item = {}
        for entry in items:
            # create the category
            category_parts = tuple(entry.name.split('/'))
            category_parents, category_name = category_parts[:-1], category_parts[-1]
            
            if not category_parents:
                parent = self.GetRootItem()
            else:
                parent = category_name_to_item[ category_parents ]
                
            icon_index = self.addIcon( '%s16x16' % entry.icon )
            #item_name = '%02d - %s' % ( self.GetChildrenCount(parent, False) + 1, entry.display_name )
            item_name = entry.display_name
            category_item = self.AppendItem( parent, item_name, image = icon_index )            
            self.SetPyData( category_item, entry )
            category_name_to_item[ category_parts ] = category_item

        self.SelectItem( self.GetRootItem() )

if __name__ == '__main__':
    demo = FloatCanvasDemo()
    demo.Run()
