###############################################################################
# Name: ed_search.py                                                          #
# Purpose: Text searching services and utilities                              #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2007,2008 Cody Precord <staff@editra.org>                    #
# License: wxWindows License                                                  #
###############################################################################

"""
Provides various search controls and searching services for finding text in a
document. The L{TextFinder} is a search service that can be used to search and
highlight text in a StyledTextCtrl.

@summary: Text searching and result ui

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Imports
import os
import sys
import re
import fnmatch
import types
from StringIO import StringIO
import wx

# Local imports
import ed_glob
import ed_txt
import ed_msg
import plugin
import iface
from util import FileTypeChecker
from profiler import Profile_Get, Profile_Set
import eclib

#--------------------------------------------------------------------------#
# Globals

_ = wx.GetTranslation
#--------------------------------------------------------------------------#

class SearchController(object):
    """Controls the interface to the text search engine"""
    def __init__(self, owner, getstc):
        """Create the controller
        @param owner: View that owns this controller
        @param getstc: Callable to get the current buffer with

        """
        object.__init__(self)

        # Attributes
        self._parent   = owner
        self._stc      = getstc
        self._finddlg  = None
        self._posinfo  = dict(scroll=0, start=0, found=0, ldir=None)
        self._data     = wx.FindReplaceData(eclib.AFR_RECURSIVE)
        self._li_choices = list()
        self._li_sel   = 0
        self._filters  = None
        self._clients = list()
        self._engine = None

        # Event handlers
        self._parent.Bind(eclib.EVT_FIND, self.OnFind)
        self._parent.Bind(eclib.EVT_FIND_NEXT, self.OnFind)
        self._parent.Bind(eclib.EVT_FIND_ALL, self.OnFindAll)
        self._parent.Bind(eclib.EVT_REPLACE, self.OnReplace)
        self._parent.Bind(eclib.EVT_REPLACE_ALL, self.OnReplaceAll)
        self._parent.Bind(eclib.EVT_FIND_CLOSE, self.OnFindClose)
        self._parent.Bind(eclib.EVT_OPTION_CHANGED, self.OnOptionChanged)

    def _CreateNewDialog(self, e_id):
        """Create and set the controlers find dialog
        @param eid: Dialog Type Id

        """
        if e_id == ed_glob.ID_FIND_REPLACE:
            dlg = eclib.AdvFindReplaceDlg(self._parent, self._data,
                                            (_("Find"), _("Find/Replace")),
                                            eclib.AFR_STYLE_REPLACEDIALOG)
        elif e_id == ed_glob.ID_FIND:
            dlg = eclib.AdvFindReplaceDlg(self._parent, self._data,
                                            (_("Find"), _("Find/Replace")))
        else:
            dlg = None

        # Change the icons to use ones from Editra's ArtProvider
        if dlg is not None:
            find = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FIND), wx.ART_MENU)
            replace = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FIND_REPLACE),
                                               wx.ART_MENU)
            if find is not None and find.IsOk():
                dlg.SetFindBitmap(find)

            if replace is not None and replace.IsOk():
                dlg.SetReplaceBitmap(replace)

            # Set the persisted data from the last time the dialog was shown
            dlg.SetLookinChoices(self._li_choices)
            dlg.SetLookinSelection(self._li_sel)
            dlg.SetFileFilters(self._filters)

        return dlg

    def _UpdateDialogState(self, e_id):
        """Update the state of the existing dialog"""
        if self._finddlg is None:
            self._finddlg = self._CreateNewDialog(e_id)
        else:
            mode = self._finddlg.GetDialogMode()
            if e_id == ed_glob.ID_FIND and mode != eclib.AFR_STYLE_FINDDIALOG:
                self._finddlg.SetDialogMode(eclib.AFR_STYLE_FINDDIALOG)
            elif e_id == ed_glob.ID_FIND_REPLACE and \
                 mode != eclib.AFR_STYLE_REPLACEDIALOG:
                self._finddlg.SetDialogMode(eclib.AFR_STYLE_REPLACEDIALOG)
            else:
                pass

        # Update the text that should be shown in the find replace fields
        self._finddlg.RefreshFindReplaceFields()
        self._finddlg.SetFocus()

    def GetClientString(self, multiline=False):
        """Get the selected text in the current client buffer. By default
        it will only return the selected text if its on a single line.
        @keyword multiline: Return text if it is multiple lines
        @return: string

        """
        cbuff = self._stc()
        if cbuff is None:
            return u''

        start, end = cbuff.GetSelection()
        rtext = cbuff.GetSelectedText()
        if start != end:
            sline = cbuff.LineFromPosition(start)
            eline = cbuff.LineFromPosition(end)
            if not multiline and (sline != eline):
                rtext = u''
        return rtext

    def GetData(self):
        """Get the contollers FindReplaceData
        @return: wx.FindReplaceData

        """
        return self._data

    def GetDialog(self):
        """Return the active find dialog if one exists else return None
        @return: FindDialog or None

        """
        return self._finddlg

    def GetLastFound(self):
        """Returns the position value of the last found search item
        if the last search resulted in nothing being found then the
        return value will -1.
        @return: position of last search opperation
        @rtype: int

        """
        return self._posinfo['found']

    def OnUpdateFindUI(self, evt):
        """Update ui handler for find related controls
        @param evt: updateui event

        """
        if evt.GetId() in (ed_glob.ID_FIND_PREVIOUS, ed_glob.ID_FIND_NEXT):
            evt.Enable(len(self.GetData().GetFindString()))
        else:
            evt.Skip()

    def OnFind(self, evt, findnext=False):
        """Do an incremental search in the currently buffer
        @param evt: EVT_FIND, EVT_FIND_NEXT
        @keyword findnext: force a find next action

        """
        data = self.GetData()

        # Find next from menu event or called internally by replace
        if findnext or evt.GetEventType() == wx.wxEVT_COMMAND_MENU_SELECTED:

            # Adjust flags
            flags = data.GetFlags()
            if not findnext and evt.GetId() == ed_glob.ID_FIND_PREVIOUS:
                flags |= eclib.AFR_UP

            evt = eclib.FindEvent(eclib.edEVT_FIND_NEXT,
                                    flags=flags)
            evt.SetFindString(data.GetFindString())

        stc = self._stc()
        data.SetFindString(evt.GetFindString())

        # Create the search engine
        isdown = not evt.IsUp()
        engine = SearchEngine(data.GetFindString(), evt.IsRegEx(),
                              isdown, evt.IsMatchCase(), evt.IsWholeWord())
        engine.SetResultFormatter(FormatResult)
        self._engine = engine

        # Check if expression was valid or not
        if engine.GetQueryObject() is None:
            wx.MessageBox(_("Invalid expression \"%s\"") % engine.GetQuery(),
                          _("Regex Compile Error"),
                          style=wx.OK|wx.CENTER|wx.ICON_ERROR)
            return

        # XXX: may be inefficent to copy whole buffer each time for files
        #      that are large.
        engine.SetSearchPool(stc.GetTextRaw())

        # Check if the direction changed
        ldir = self._posinfo['ldir']
        if isdown:
            self._posinfo['ldir'] = 'down'
        else:
            self._posinfo['ldir'] = 'up'

        # Get the search start position
        if evt.GetEventType() == eclib.edEVT_FIND:
            spos = self._posinfo['found']
        else:
            spos = stc.GetCurrentPos()
            if ldir != self._posinfo['ldir']:
                start, end = stc.GetSelection()
                if ldir == 'down':
                    spos = start
                else:
                    spos = end

        # Do the find
        match = engine.Find(spos)
        if match is not None:
            start, end = match

            if isdown:
                start = start + spos
                end = end + spos
                stc.SetSelection(start, end)
            else:
                stc.SetSelection(end, start)

            # Ensure caret and the line its in is exposed
            stc.EnsureCaretVisible()
            line = stc.LineFromPosition(start)
            stc.EnsureVisible(line)

            self._posinfo['found'] = start

            ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                               (ed_glob.SB_INFO, u""))
        else:
            # try search from top again
            if isdown:
                match = engine.Find(0)
                ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                                  (ed_glob.SB_INFO, _("Search wrapped to top")))
            else:
                match = engine.Find(-1)
                ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                                  (ed_glob.SB_INFO,
                                  _("Search wrapped to bottom")))

            if match is not None:
                start, end = match

                self._posinfo['found'] = start

                match = list(match)
                if not isdown:
                    match.reverse()
                stc.SetSelection(match[0], match[1])
                
                # Ensure caret and the line its in is exposed
                stc.EnsureCaretVisible()
                line = stc.LineFromPosition(match[0])
                stc.EnsureVisible(line)
            else:
                self._posinfo['found'] = -1
                ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                                  (ed_glob.SB_INFO,
                                  _("\"%s\" was not found") % engine.GetQuery()))

    def OnFindAll(self, evt):
        """Find all results for the given query and display results in a
        L{FindResultsScreen} in the Shelf.

        """
        smode = evt.GetSearchType()
        query = evt.GetFindString()
        if not query:
            return

        # Create a new search engine object
        engine = SearchEngine(query, evt.IsRegEx(), True,
                              evt.IsMatchCase(), evt.IsWholeWord())
        engine.SetResultFormatter(FormatResult)

        # Send the search function over to any interested parties that wish
        # to process the results.
        if smode == eclib.LOCATION_CURRENT_DOC:
            stc = self._stc()
            fname = stc.GetFileName()
            if len(fname):
                ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH,
                                   (engine.SearchInFile, [fname,], dict()))
            else:
                engine.SetSearchPool(stc.GetTextRaw())
                ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH, (engine.FindAllLines,))
        elif smode == eclib.LOCATION_OPEN_DOCS:
            files = [fname.GetFileName()
                     for fname in self._parent.GetTextControls()]
            ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH,
                               (engine.SearchInFiles, [files,], dict()))
        elif smode == eclib.LOCATION_IN_FILES:
            path = evt.GetDirectory()
            engine.SetFileFilters(evt.GetFileFilters())
            ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH,
                               (engine.SearchInDirectory,
                                [path,], dict(recursive=evt.IsRecursive())))

    def OnFindSelected(self, evt):
        """Set the search query to the selected text and progress the search
        to the next match.

        """
        stc = self._stc()

        fstring = stc.GetSelectedText()
        if fstring:
            data = self.GetData()
            data.SetFindString(fstring)
            self.OnFind(evt)
        else:
            evt.Skip()

    def OnFindClose(self, evt):
        """Destroy Find Dialog After Cancel is clicked in it
        @param evt: event that called this handler

        """
        if self._finddlg is not None:
            # Save the lookin values for next time dialog is shown
            self._li_choices = self._finddlg.GetLookinChoices()
            self._li_sel = self._finddlg.GetLookinSelection()
            self._filters = self._finddlg.GetFileFilters()

            # Store in profile. Only save most recent 5 in history
            if len(self._li_choices) > 5:
                choices = self._li_choices[-5:]
            else:
                choices = self._li_choices

            # Save the most recent choices of search locations
            Profile_Set('SEARCH_LOC', choices)
            Profile_Set('SEARCH_FILTER', self._filters)

            # Destroy it
            self._finddlg.Destroy()

        self._finddlg = None
        evt.Skip()

    def OnOptionChanged(self, evt):
        """Handle when the find options are changed in the dialog"""
        dead = list()
        for idx, client in enumerate(self._clients):
            try:
                client.NotifyOptionChanged(evt)
            except wx.PyDeadObjectError:
                dead.append(idx)

    def OnReplace(self, evt):
        """Replace the selected text in the current buffer
        @param evt: finddlg.EVT_REPLACE

        """
        replacestring = evt.GetReplaceString()
        if evt.IsRegEx() and self._engine is not None:
            match = self._engine.GetLastMatch()
            if match is not None:
                value = match.expand(replacestring)
            else:
                value = replacestring
        else:
            value = replacestring
        self._stc().ReplaceSelection(value)

        # Go to the next match
        # Fake event object for on Find Handler
        tevt = eclib.FindEvent(eclib.edEVT_FIND_NEXT,
                                 ed_glob.ID_FIND_PREVIOUS)
        self.OnFind(tevt, True)

    def OnReplaceAll(self, evt):
        """Replace all instance of the search string with the given
        replace string for the given search context.

        """
        smode = evt.GetSearchType()
        rstring = evt.GetReplaceString()
        engine = SearchEngine(evt.GetFindString(), evt.IsRegEx(),
                              True, evt.IsMatchCase(), evt.IsWholeWord())
        engine.SetResultFormatter(FormatResult)

        results = 0

        if smode == eclib.LOCATION_CURRENT_DOC:
            stc = self._stc()
            engine.SetSearchPool(stc.GetTextRaw())
            matches = engine.FindAll()
            if matches is not None:
                self.ReplaceInStc(stc, matches, rstring, evt.IsRegEx())
                results = len(matches)
        elif smode == eclib.LOCATION_OPEN_DOCS:
            for ctrl in self._parent.GetTextControls():
                engine.SetSearchPool(ctrl.GetTextRaw())
                matches = engine.FindAll()
                if matches is not None:
                    self.ReplaceInStc(ctrl, matches, rstring, evt.IsRegEx())
                    results += len(matches)
        elif smode == eclib.LOCATION_IN_FILES:
            dlg = wx.MessageDialog(self._parent,
                                   _("Sorry will be ready for next version"),
                                   _("Not implemented"),
#                                   _("Warning this cannot be undone!"),
#                                   _("Do Replace All?"),
                                   style=wx.ICON_WARNING|wx.OK|wx.CANCEL|wx.CENTER)
            result = dlg.ShowModal()
            dlg.Destroy()

            if result == wx.ID_OK:
                pass
#                path = evt.GetDirectory()
#                ed_msg.PostMessage(ed_msg.EDMSG_START_SEARCH,
#                                   (engine.SearchInDirectory,
#                                    [path,], dict(recursive=evt.IsRecursive())))
            else:
                return

        # Post number of matches that were replaced to the status bar
        if results > 0:
            ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                              (ed_glob.SB_INFO,
                              _("%d matches were replaced.") % results))

    def OnShowFindDlg(self, evt):
        """Catches the Find events and shows the appropriate find dialog
        @param evt: event that called this handler
        @postcondition: find dialog is shown

        """
        # Check for a selection in the buffer and load that text if
        # there is any and it is at most one line.
        query = self.GetClientString()
        if len(query):
            self.SetQueryString(query)

        eid = evt.GetId()
        # Dialog is not currently open
        if self._finddlg is None:
            self._finddlg = self._CreateNewDialog(eid)
            if self._finddlg is None:
                evt.Skip()
                return
            self._finddlg.SetTransparent(240)
#            self._finddlg.SetExtraStyle(wx.WS_EX_PROCESS_UI_UPDATES)
            self._finddlg.Show()
        else:
            # Dialog is open already so just update it
            self._UpdateDialogState(eid)
            self._finddlg.Raise()
        self._finddlg.SetFocus()

    def RegisterClient(self, client):
        """Register a client object of this search controller. The client object
        must implement a method called NotifyOptionChanged to be called when
        search options are changed.

        >>> def NotifyOptionChanged(self, evt)

        @param client: object

        """
        if client not in self._clients:
            self._clients.append(client)

    def RemoveClient(self, client):
        """Remove a client from this controller
        @param client: object

        """
        if client in self._clients:
            self._clients.remove(client)

    @staticmethod
    def ReplaceInStc(stc, matches, rstring, isregex=True):
        """Replace the strings at the position in the given StyledTextCtrl
        @param stc: StyledTextCtrl
        @param matches: list of tuples [(s1, e1), (s2, e2)]
        @param rstring: Replace string

        """
        stc.BeginUndoAction()
        for match in reversed(matches):
            start, end = match.span()
            if isregex:
                value = match.expand(rstring)
            else:
                value = rstring
            stc.SetTargetStart(start)
            stc.SetTargetEnd(end)
            stc.ReplaceTarget(value)
        stc.EndUndoAction()

    def SetFileFilters(self, filters):
        """Set the file filter to use
        @param filters: string '*.py *.pyw'

        """
        self._filters = filters

    def SetLookinChoices(self, choices):
        """Set the list of locations to use for the recent search
        locations.
        @param choices: list of strings

        """
        self._li_choices = choices

    def SetQueryString(self, query):
        """Sets the search query value
        @param query: string to search for

        """
        self._data.SetFindString(query)

    def SetSearchFlags(self, flags):
        """Set the find services search flags
        @param flags: bitmask of parameters to set

        """
        self._data.SetFlags(flags)
        if self._finddlg is not None:
            self._finddlg.SetData(self._data)

    def RefreshControls(self):
        """Refresh controls that are associated with this controllers data."""
        if self._finddlg is not None:
            self._finddlg.RefreshFindOptions()

#-----------------------------------------------------------------------------#

class SearchEngine(object):
    """Text Search Engine
    All Search* methods are iterable generators
    All Find* methods do a complete search and return the match collection
    @summary: Text Search Engine
    @todo: Add file filter support

    """
    def __init__(self, query, regex=True, down=True,
                  matchcase=True, wholeword=False):
        """Initialize a search engine object
        @param query: search string
        @keyword regex: Is a regex search
        @keyword down: Search down or up
        @keyword matchcase: Match case
        @keyword wholeword: Match whole word

        """
        object.__init__(self)

        # Attributes
        self._isregex = regex
        self._next = down
        self._matchcase = matchcase
        self._wholeword = wholeword
        self._unicode = False
        self._query = query
        self._regex = u''
        self._pool = u''
        self._lmatch = None             # Last match object
        self._filters = None            # File Filters
        self._formatter = lambda f, l, m: u"%s %d: %s" % (f, l+1, m)
        self._CompileRegex()

    def _CompileRegex(self):
        """Prepare and compile the regex object based on the current state
        and settings of the engine.
        @postcondition: the engines regular expression is created

        """
        tmp = self._query
        if not self._isregex:
            tmp = re.escape(tmp)

        if self._wholeword:
            tmp = "\\b%s\\b" % tmp

        flags = re.MULTILINE

        if not self._matchcase:
            flags |= re.IGNORECASE

        if self._unicode:
            flags |= re.UNICODE

        try:
            self._regex = re.compile(tmp, flags)
        except:
            self._regex = None

    def Find(self, spos=0):
        """Find the next match based on the state of the search engine
        @keyword spos: search start position
        @return: tuple (match start pos, match end pos) or None if no match
        @prerequisite: L{SetSearchPool} has been called to set search string

        """
        if self._regex is None:
            return None

        if self._next:
            return self.FindNext(spos)
        else:
            if spos == 0:
                spos = -1
            return self.FindPrev(spos)

    def FindAll(self):
        """Find all the matches in the current context
        @return: list of tuples [(start1, end1), (start2, end2), ]

        """
        if self._regex is None:
            return list()

        matches = [match for match in self._regex.finditer(self._pool)]
        return matches

    def FindAllLines(self):
        """Find all the matches in the current context
        @return: list of strings

        """
        rlist = list()
        if self._regex is None:
            return rlist

        for lnum, line in enumerate(StringIO(self._pool)):
            if self._regex.search(line) is not None:
                rlist.append(self._formatter(_("Untitled"), lnum, line))

        return rlist

    def FindNext(self, spos=0):
        """Find the next match of the query starting at spos
        @keyword spos: search start position in string
        @return: tuple (match start pos, match end pos) or None if no match
        @prerequisite: L{SetSearchPool} has been called to set the string to
                       search in.

        """
        if self._regex is None:
            return None

        if spos < len(self._pool):
            match = self._regex.search(self._pool[spos:])
            if match is not None:
                self._lmatch = match
                return match.span()
        return None

    def FindPrev(self, spos=-1):
        """Find the previous match of the query starting at spos
        @param pool: string to search in
        @keyword spos: search start position in string
        @return: tuple (match start pos, match end pos)

        """
        if self._regex is None:
            return None

        if spos+1 < len(self._pool):
            matches = [match for match in self._regex.finditer(self._pool[:spos])]
            if len(matches):
                lmatch = matches[-1]
                self._lmatch = lmatch
                return (lmatch.start(), lmatch.end())
        return None

    def GetLastMatch(self):
        """Get the last found match object from the previous L{FindNext} or
        L{FindPrev} action.
        @return: match object or None

        """
        return self._lmatch

    def GetOptionsString(self):
        """Get a string describing the search engines options"""
        rstring = u"\"%s\" [ " % self._query
        for desc, attr in ((_("regex: %s"), self._isregex),
                           (_("match case: %s"), self._matchcase),
                           (_("whole word: %s"), self._wholeword)):
            if attr:
                rstring += (desc % u"on; ")
            else:
                rstring += (desc % u"off; ")
        rstring += u"]"

        return rstring

    def GetQuery(self):
        """Get the raw query string used by the search engine
        @return: string

        """
        return self._query

    def GetQueryObject(self):
        """Get the regex object used for the search. Will return None if
        there was an error in creating the object.
        @return: pattern object

        """
        return self._regex

    def GetSearchPool(self):
        """Get the search pool string for this L{SearchEngine}.
        @return: string

        """
        return self._pool

    def IsMatchCase(self):
        """Is the engine set to a case sensitive search
        @return: bool

        """
        return self._matchcase

    def IsRegEx(self):
        """Is the engine searching with the query as a regular expression
        @return: bool

        """
        return self._isregex

    def IsWholeWord(self):
        """Is the engine set to search for wholeword matches
        @return: bool

        """
        return self._wholeword

    def SearchInBuffer(self, sbuffer):
        """Search in the buffer
        @param sbuffer: buffer like object
        @todo: implement

        """
        raise NotImplementedError

    def SearchInDirectory(self, directory, recursive=True):
        """Search in all the files found in the given directory
        @param directory: directory path
        @keyword recursive: search recursivly

        """
        if self._regex is None:
            return

        # Get all files in the directories
        paths = [os.path.join(directory, fname)
                for fname in os.listdir(directory) if not fname.startswith('.')]

        # Filter out files that don't match the current filter(s)
        if self._filters is not None and len(self._filters):
            filtered = list()
            for fname in paths:
                if os.path.isdir(fname):
                    filtered.append(fname)
                    continue

                for pat in self._filters:
                    if fnmatch.fnmatch(fname, pat):
                        filtered.append(fname)
            paths = filtered

        # Begin searching in the paths
        for path in paths:
            if recursive and os.path.isdir(path):
                # Recursive call to decend into directories
                for match in self.SearchInDirectory(path, recursive):
                    yield match
            else:
                for match in self.SearchInFile(path):
                    yield match
        return

    def SearchInFile(self, fname):
        """Search in a file for all lines with matches of the set query and
        yield the results as they are found.
        @param fname: filename
        @todo: unicode handling

        """
        if self._regex is None:
            return

        fchecker = FileTypeChecker()
        if fchecker.IsReadableText(fname):
            try:
                fobj = open(fname, 'rb')
            except (IOError, OSError):
                return
            else:
                # Special token to signify start of a search
                yield (None, fname)

            for lnum, line in enumerate(fobj):
                if self._regex.search(line) is not None:
                    yield self._formatter(fname, lnum, line)
            fobj.close()
        return

    def SearchInFiles(self, flist):
        """Search in a list of files and yield results as they are found.
        @param flist: list of file names

        """
        if self._regex is None:
            return

        for fname in flist:
            for match in self.SearchInFile(fname):
                yield match
        return

    def SearchInString(self, sstring, startpos=0):
        """Search in a string
        @param sstring: string to search in
        @keyword startpos: search start position

        """
        raise NotImplementedError

    def SetFileFilters(self, filters):
        """Set the file filters to specify what type of files to search in
        the filter should be a list of wild card patterns to match.
        @param filters: list of strings ['*.py', '*.pyw']

        """
        self._filters = filters

    def SetFlags(self, isregex=None, matchcase=None, wholeword=None, down=None):
        """Set the search engine flags. Leaving the parameter set to None
        will not change the flag. Setting it to non None will change the value.
        @keyword isregex: is regex search
        @keyword matchcase: matchcase search
        @keyword wholeword: wholeword search
        @keyword down: search down or up

        """
        for attr, val in (('_isregex', isregex), ('_matchcase', matchcase),
                          ('_wholeword', wholeword), ('_next', down)):
            if val is not None:
                setattr(self, attr, val)
        self._CompileRegex()

    def SetResultFormatter(self, funct):
        """Set the result formatter function
        @param funct: callable(filename, linenum, matchstr)

        """
        assert callable(funct)
        self._formatter = funct

    def SetSearchPool(self, pool):
        """Set the search pool used by the Find methods
        @param pool: string to search in

        """
        del self._pool
        self._pool = pool
        if isinstance(self._pool, types.UnicodeType):
            self._unicode = True
            self._CompileRegex()

    def SetQuery(self, query):
        """Set the search query
        @param query: string

        """
        self._query = query
        self._CompileRegex()

#-----------------------------------------------------------------------------#

def FormatResult(fname, lnum, match):
    """Format the search result string
    @return: string
    @todo: better unicode handling

    """
    fname = ed_txt.DecodeString(fname, sys.getfilesystemencoding())
    if not isinstance(fname, types.UnicodeType):
        fname = _("DECODING ERROR")

    match = ed_txt.DecodeString(match)
    if not isinstance(match, types.UnicodeType):
        match = _("DECODING ERROR")
    else:
        match = u" " + match.lstrip()

    rstring = u"%(fname)s (%(lnum)d): %(match)s"
    return rstring % dict(fname=fname, lnum=lnum+1, match=match)

#-----------------------------------------------------------------------------#

class EdSearchCtrl(wx.SearchCtrl):
    """Creates a simple search control for use in the toolbar
    or a statusbar and the such. Supports incremental search,
    and uses L{TextFinder} to do the actual searching of the
    document.

    """
    def __init__(self, parent, id_, value="", menulen=0, \
                 pos=wx.DefaultPosition, size=wx.DefaultSize, \
                 style=wx.TE_RICH2|wx.TE_PROCESS_ENTER):
        """Initializes the Search Control
        @param menulen: max length of history menu

        """
        wx.SearchCtrl.__init__(self, parent, id_, value, pos, size, style)

        # Attributes
        self._parent     = parent
        # TEMP HACK
        self.FindService = self.GetTopLevelParent().GetNotebook()._searchctrl
        self._flags      = 0
        self._recent     = list()        # The History List
        self._last       = None
        self.rmenu       = wx.Menu()
        self.max_menu    = menulen + 2   # Max menu length + descript/separator
        self._txtctrl    = None          # msw/gtk only

        # Setup Recent Search Menu
        lbl = self.rmenu.Append(wx.ID_ANY, _("Recent Searches"))
        lbl.Enable(False)
        self.rmenu.AppendSeparator()
        self.SetMenu(self.rmenu)

        # Bind Events
        if wx.Platform in ['__WXMSW__', '__WXGTK__']:
            for child in self.GetChildren():
                if isinstance(child, wx.TextCtrl):
                    child.Bind(wx.EVT_KEY_UP, self.ProcessEvent)
                    self._txtctrl = child
                    break
        else:
            self.Bind(wx.EVT_KEY_UP, self.ProcessEvent)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnCancel)
        self.Bind(wx.EVT_MENU, self.OnHistMenu)

    #---- Functions ----#
    def AutoSetQuery(self, multiline=False):
        """Autoload a selected string from the controls client buffer"""
        query = self.FindService.GetClientString(multiline)
        if len(query):
            self.FindService.SetQueryString(query)
            self.SetValue(query)

    def ClearSearchFlag(self, flag):
        """Clears a previously set search flag
        @param flag: flag to clear from search data

        """
        data = self.GetSearchData()
        if data is not None:
            c_flags = data.GetFlags()
            c_flags ^= flag
            self._flags = c_flags
            data.SetFlags(self._flags)
            self.FindService.RefreshControls()

    def DoSearch(self, next=True):
        """Do the search and move the selection
        @keyword next: search next or previous

        """
        s_cmd = eclib.edEVT_FIND
        if not next:
            self.SetSearchFlag(eclib.AFR_UP)
        else:
            if eclib.AFR_UP & self._flags:
                self.ClearSearchFlag(eclib.AFR_UP)

        if self.GetValue() == self._last:
            s_cmd = eclib.edEVT_FIND_NEXT

        evt = eclib.FindEvent(s_cmd, flags=self._flags)
        self._last = self.GetValue()
        evt.SetFindString(self.GetValue())
        self.FindService.OnFind(evt)

        # Give feedback on whether text was found or not
        if self.FindService.GetLastFound() < 0 and len(self.GetValue()) > 0:
            if self._txtctrl is None:
                self.SetForegroundColour(wx.RED)
            else:
                self._txtctrl.SetForegroundColour(wx.RED)
            wx.Bell()
        else:
            # ?wxBUG? cant set text back to black after changing color
            # But setting it to this almost black color works. Most likely its
            # due to bit masking but I havent looked at the source so I am not
            # sure
            if self._txtctrl is None:
                self.SetForegroundColour(wx.ColourRGB(0 | 1 | 0))
            else:
                self._txtctrl.SetForegroundColour(wx.ColourRGB(0 | 1 | 0))
        self.Refresh()

    def GetSearchController(self):
        """Get the L{SearchController} used by this control.
        @return: L{SearchController}

        """
        return self.FindService

    def GetSearchData(self):
        """Gets the find data from the controls FindService
        @return: search data
        @rtype: wx.FindReplaceData

        """
        if hasattr(self.FindService, "GetData"):
            return self.FindService.GetData()
        else:
            return None

    def GetHistory(self):
        """Gets and returns the history list of the control
        @return: list of recent search items

        """
        return getattr(self, "_recent", list())

    def InsertHistoryItem(self, value):
        """Inserts a search query value into the top of the history stack
        @param value: search string
        @postcondition: the value is added to the history menu

        """
        if value == wx.EmptyString:
            return

        # Make sure menu only has unique items
        m_items = list(self.rmenu.GetMenuItems())
        for menu_i in m_items:
            if value == menu_i.GetLabel():
                self.rmenu.RemoveItem(menu_i)

        # Create and insert the new item
        n_item = wx.MenuItem(self.rmenu, wx.NewId(), value)
        self.rmenu.InsertItem(2, n_item)

        # Update History list
        self._recent.insert(0, value)
        if len(self._recent) > self.max_menu:
            self._recent.pop()

        # Check Menu Length
        m_len = self.rmenu.GetMenuItemCount()
        if m_len > self.max_menu:
            try:
                self.rmenu.RemoveItem(m_items[-1])
            except IndexError, msg:
                wx.GetApp().GetLog()("[ed_search][err] menu error: %s" % str(msg))

    def IsMatchCase(self):
        """Returns True if the search control is set to search
        in Match Case mode.
        @return: whether search is using match case or not
        @rtype: boolean

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_MATCHCASE & data.GetFlags())
        return False

    def IsRegEx(self):
        """Returns True if the search control is set to search
        in regular expression mode.
        @return: whether search is using regular expressions or not
        @rtype: boolean

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_REGEX & data.GetFlags())
        return False

    def IsSearchPrevious(self):
        """Returns True if the search control is set to search
        in Previous mode.
        @return: whether search is searchin up or not
        @rtype: boolean

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_UP & data.GetFlags())
        return False

    def IsWholeWord(self):
        """Returns True if the search control is set to search
        in Whole Word mode.
        @return: whether search is using match whole word or not
        @rtype: boolean

        """
        data = self.GetSearchData()
        if data is not None:
            return bool(eclib.AFR_WHOLEWORD & data.GetFlags())
        return False

    def SetFocus(self):
        """Set the focus and select the text"""
        super(EdSearchCtrl, self).SetFocus()
        self.AutoSetQuery()
        self.SelectAll()

    def SetHistory(self, hist_list):
        """Populates the history list from a list of
        string values.
        @param hist_list: list of search items

        """
        hist_list.reverse()
        for item in hist_list:
            self.InsertHistoryItem(item)

    def SetSearchFlag(self, flags):
        """Sets the search data flags
        @param flags: search flag to add

        """
        data = self.GetSearchData()
        if data is not None:
            c_flags = data.GetFlags()
            c_flags |= flags
            self._flags = c_flags
            data.SetFlags(self._flags)
            self.FindService.RefreshControls()

    #---- End Functions ----#

    #---- Event Handlers ----#
    def ProcessEvent(self, evt):
        """Processes Events for the Search Control
        @param evt: the event that called this handler

        """
        if evt.GetEventType() != wx.wxEVT_KEY_UP:
            evt.Skip()
            return

        e_key = evt.GetKeyCode()
        if e_key == wx.WXK_ESCAPE:
            # TODO change to more safely determine the context
            # Currently control is only used in command bar
            self.GetParent().Hide()
            evt.Skip()
            return
        elif e_key == wx.WXK_SHIFT:
            self.ClearSearchFlag(eclib.AFR_UP)
            return
        else:
            pass

        tmp = self.GetValue()
        self.ShowCancelButton(len(tmp) > 0)

        # Dont do search for navigation keys
        if tmp == wx.EmptyString or evt.CmdDown() or \
           e_key in [wx.WXK_COMMAND, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_CONTROL,
                     wx.WXK_ALT, wx.WXK_UP, wx.WXK_DOWN, wx.WXK_F1, wx.WXK_F2, 
                     wx.WXK_F3, wx.WXK_F4, wx.WXK_F5, wx.WXK_F6, wx.WXK_F7, 
                     wx.WXK_F8, wx.WXK_F9, wx.WXK_F10, wx.WXK_F11, wx.WXK_F12]:
            return

        if e_key == wx.WXK_RETURN or e_key == wx.WXK_F3:
            if evt.ShiftDown():
                self.DoSearch(next=False)
            else:
                self.DoSearch(next=True)

            # Add to search history
            if e_key == wx.WXK_RETURN:
                self.InsertHistoryItem(self.GetValue())
        else:
            # Don't do incremental searches when the RegEx flag is set in order
            # to avoid errors in compiling the expression
            if not self.IsRegEx():
                self.DoSearch(next=True)

    def OnCancel(self, evt):
        """Cancels the Search Query
        @param evt: the event that called this handler

        """
        self.SetValue(u"")
        self.ShowCancelButton(False)
        evt.Skip()

    def OnHistMenu(self, evt):
        """Sets the search controls value to the selected menu item
        @param evt: the event that called this handler
        @type evt: wx.MenuEvent

        """
        item_id = evt.GetId()
        item = self.rmenu.FindItemById(item_id)
        if item != None:
            self.SetValue(item.GetLabel())
        else:
            evt.Skip()

    #---- End Event Handlers ----#

#-----------------------------------------------------------------------------#

class EdFindResults(plugin.Plugin):
    """Shelf interface implementation for the find results"""
    plugin.Implements(iface.ShelfI)
    SUBSCRIBED = False
    RESULT_SCREENS = list()

    def __init__(self, pmgr):
        """Create the FindResults plugin
        @param pmgr: This plugins manager

        """
        if not EdFindResults.SUBSCRIBED:
            ed_msg.Subscribe(EdFindResults.StartResultsScreen,
                             ed_msg.EDMSG_START_SEARCH)
            EdFindResults.SUBSCRIBED = True

#    def __del__(self):
#        if EdFindResults.SUBSCRIBED:
#            print "UNSUBSCRIBE"
#            ed_msg.Unsubscribe(self.StartResultsScreen)

    @property
    def __name__(self):
        return u'Find Results'

    def AllowMultiple(self):
        """Find Results allows multiple instances"""
        return True

    def CreateItem(self, parent):
        """Returns a log viewr panel"""
        screen = SearchResultScreen(parent)
        EdFindResults.RESULT_SCREENS.append(screen)
        return screen

    def GetBitmap(self):
        """Get the find results bitmap
        @return: wx.Bitmap

        """
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FIND), wx.ART_MENU)
        return bmp

    def GetId(self):
        """Plugin menu identifier ID"""
        return ed_glob.ID_FIND_RESULTS

    def GetMenuEntry(self, menu):
        """Get the menu entry for the log viewer
        @param menu: the menu items parent menu

        """
        return None

    def GetName(self):
        """Return the name of this control"""
        return self.__name__

    def IsStockable(self):
        """EdLogViewer can be saved in the shelf preference stack"""
        return False

    @classmethod
    def StartResultsScreen(cls, msg):
        """Start a search in an existing window or open a new one
        @param cls: this class
        @param msg: message object

        """
        win = wx.GetApp().GetActiveWindow()

        # Cleanup window list for dead objects
        to_pop = list()
        for idx, item in enumerate(list(EdFindResults.RESULT_SCREENS)):
            if not isinstance(item, SearchResultScreen):
                to_pop.append(idx)

        for idx in reversed(to_pop):
            EdFindResults.RESULT_SCREENS.pop(idx)

        # Try to find an empty existing window to use for the new search
        screen = None
        if win is not None:
            shelf = win.GetShelf()
            s_mw = shelf.GetOwnerWindow()
            shelf_nb = shelf.GetWindow()
            for item in EdFindResults.RESULT_SCREENS:
                if item.GetDisplayedLines() < 3 and \
                   s_mw is win and item.GetParent() is shelf_nb:
                    screen = shelf.RaiseWindow(item)
                    break

            if screen is None:
                shelf.PutItemOnShelf(ed_glob.ID_FIND_RESULTS)
                screen = shelf_nb.GetCurrentPage()

            # Fire off the search job
            data = msg.GetData()
            if len(data) > 1:
                # Doing a file search operation
                screen.StartSearch(data[0], *data[1], **data[2])
            else:
                # Doing a buffer find operation (in memory)
                screen.StartSearch(data[0])

#-----------------------------------------------------------------------------#

class SearchResultScreen(eclib.ControlBox):
    """Screen for displaying search results and navigating to them"""
    def __init__(self, parent):
        """Create the result screen
        @param parent: parent window

        """
        eclib.ControlBox.__init__(self, parent)

        # Attributes
        self._meth = None
        self._job = None
        self._list = SearchResultList(self)
        self._cancelb = None
        self._clearb = None

        # Layout
        self.__DoLayout()
        self._cancelb.Disable()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON,
                  lambda evt: self._list.Clear(), id=wx.ID_CLEAR)
        self.Bind(wx.EVT_BUTTON,
                  lambda evt: self.CancelSearch(), id=wx.ID_CANCEL)
        self._list.Bind(eclib.EVT_TASK_START, self.OnTaskStart)
        self._list.Bind(eclib.EVT_TASK_COMPLETE, self.OnTaskComplete)

        # Message Handlers
        ed_msg.Subscribe(self.OnThemeChange, ed_msg.EDMSG_THEME_CHANGED)

    def __del__(self):
        ed_msg.Unsubscribe(self.OnThemeChange)

    def __DoLayout(self):
        """Layout and setup the results screen ui"""
        ctrlbar = eclib.ControlBar(self, style=eclib.CTRLBAR_STYLE_GRADIENT)
        if wx.Platform == '__WXGTK__':
            ctrlbar.SetWindowStyle(eclib.CTRLBAR_STYLE_DEFAULT)

        ctrlbar.AddStretchSpacer()

        # Cancel Button
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_STOP), wx.ART_MENU)
        if cbmp.IsNull() or not cbmp.IsOk():
            cbmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR,
                                            wx.ART_MENU, (16, 16))
        cancel = eclib.PlateButton(ctrlbar, wx.ID_CANCEL, _("Cancel"),
                                      cbmp, style=eclib.PB_STYLE_NOBG)
        self._cancelb = cancel
        ctrlbar.AddControl(cancel, wx.ALIGN_RIGHT)

        # Clear Button
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DELETE), wx.ART_MENU)
        if cbmp.IsNull() or not cbmp.IsOk():
            cbmp = None
        clear = eclib.PlateButton(ctrlbar, wx.ID_CLEAR, _("Clear"),
                                     cbmp, style=eclib.PB_STYLE_NOBG)
        self._clearb = clear
        ctrlbar.AddControl(clear, wx.ALIGN_RIGHT)

        ctrlbar.SetVMargin(1, 1)
        self.SetControlBar(ctrlbar)
        self.SetWindow(self._list)

    def GetDisplayedLines(self):
        """Get the number of lines displayed in the output window"""
        return self._list.GetLineCount()

    def OnTaskStart(self, evt):
        """Start accepting results from the search thread
        @param evt: UpdateBufferEvent

        """
        start = u">>> %s" % _("Search Started")
        if self._meth is not None:
            start += (u": " + self._meth.im_self.GetOptionsString())
        self._list.SetStartEndText(start + os.linesep)
        self._list.Start(250)

    def OnTaskComplete(self, evt):
        """Update when task is complete
        @param evt: UpdateBufferEvent

        """
        self._meth = None

        # Stop the timer
        self._list.Stop()
        self._cancelb.Disable()

        # Update statusbar to show search is complete
        ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                           (ed_glob.SB_INFO, _("Search complete")))

        # Let the update buffer be flushed
        wx.YieldIfNeeded()
 
        # Add our end message
        lines = max(0, self._list.GetLineCount() - 2)
        msg = _("Search Complete: %d matching lines where found.") % lines
        msg2 = _("Files Searched: %d" % self._list.GetFileCount())
        end = u">>> %s \t%s" % (msg, msg2)
        self._list.SetStartEndText(end + os.linesep)

    def OnThemeChange(self, msg):
        """Update the button icons after the theme has changed
        @param msg: Message Object

        """
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DELETE), wx.ART_MENU)
        self._clearb.SetBitmap(cbmp)
        self._clearb.Refresh()

        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_STOP), wx.ART_MENU)
        self._cancelb.SetBitmap(cbmp)
        self._cancelb.Refresh()

    def CancelSearch(self):
        """Cancel the currently running search"""
        if self._job is not None:
            self._job.Cancel()
        self._cancelb.Disable()

    def StartSearch(self, searchmeth, *args, **kwargs):
        """Start a search with the given method and display the results
        @param searchmeth: callable

        """
        self._meth = searchmeth

        if self._job is not None:
            self._job.Cancel()

        self._list.Clear()
        self._job = eclib.TaskThread(self._list, searchmeth, *args, **kwargs)
        self._job.start()
        self._cancelb.Enable()

#-----------------------------------------------------------------------------#

class SearchResultList(eclib.OutputBuffer):
    """Outputbuffer for listing matching lines from the search results that
    a L{SearchEngine} dispatches. The matching lines are turned into hotspots
    that allow them to be clicked on for instant navigation to the matching
    line.

    """
    STY_SEARCH_MATCH = eclib.OPB_STYLE_MAX + 1
    RE_FIND_MATCH = re.compile('(.+) \(([0-9]+)\)\: .+')
    def __init__(self, parent):
        eclib.OutputBuffer.__init__(self, parent)

        # Attributes
        self._files = 0

        # Setup
        font = Profile_Get('FONT1', 'font', wx.Font(11, wx.FONTFAMILY_MODERN, 
                                                    wx.FONTSTYLE_NORMAL, 
                                                    wx.FONTWEIGHT_NORMAL))
        self.SetFont(font)
        style = (font.GetFaceName(), font.GetPointSize(), "#FFFFFF")
        self.StyleSetSpec(SearchResultList.STY_SEARCH_MATCH,
                          "face:%s,size:%d,fore:#000000,back:%s" % style)
        self.StyleSetHotSpot(SearchResultList.STY_SEARCH_MATCH, True)

    def AppendUpdate(self, value):
        """Do a little filtering of updates as they arrive
        @param value: search result from search method

        """
        if isinstance(value, basestring):
            # Regular search result
            eclib.OutputBuffer.AppendUpdate(self, value)
        else:
            # Search in a new file has started
            self._files += 1

            # Only updated status bar for every 10 files to reduce the overhead
            # of updating the status bar and to improve performance of search.
            if self._files == 1 or \
               ((self._files / 10) > ((self._files-1) / 10)): 
                ed_msg.PostMessage(ed_msg.EDMSG_UI_SB_TXT,
                                   (ed_glob.SB_INFO,
                                   _("Searching in: %s") % value[1]))

    def ApplyStyles(self, start, txt):
        """Set a hotspot for each search result
        Search matches strings should be formatted as follows
        /file/name (line) match string
        @param start: long
        @param txt: string

        """
        self.StartStyling(start, 0x1f)
        if re.match(SearchResultList.RE_FIND_MATCH, txt):
            self.SetStyling(len(txt), SearchResultList.STY_SEARCH_MATCH)
        else:
            self.SetStyling(len(txt), eclib.OPB_STYLE_DEFAULT)

    def Clear(self):
        """Override OutputBuffer.Clear"""
        self._files = 0
        super(SearchResultList, self).Clear()

    def DoHotSpotClicked(self, pos, line):
        """Handle a click on a hotspot and open the file to the matched line
        @param pos: long
        @param line: int

        """
        txt = self.GetLine(line)
        match = re.match(SearchResultList.RE_FIND_MATCH, txt)
        if match is not None:
            groups = match.groups()
            if len(groups) == 2:
                fname, lnum = groups
                if lnum.isdigit():
                    lnum = int(lnum) - 1
                else:
                    lnum = 0
                self._OpenToLine(fname, lnum)

    def GetFileCount(self):
        """Get the number of files searched in the previous/current search job.
        @return: int

        """
        return self._files

    def SetStartEndText(self, txt):
        """Add a start task or end task message to the output. Styled in
        Info style.
        @param txt: text to add

        """
        self.SetReadOnly(False)
        cpos = self.GetLength()
        self.AppendText(txt)
        self.StartStyling(cpos, 0x1f)
        self.SetStyling(self.GetLength() - cpos, eclib.OPB_STYLE_INFO)
        self.SetReadOnly(True)

    @staticmethod
    def _OpenToLine(fname, line):
        """Open the given filename to the given line number
        @param fname: File name to open, relative paths will be converted to abs
                      paths.
        @param line: Line number to set the cursor to after opening the file
        @param mainw: MainWindow instance to open the file in

        """
        mainw = wx.GetApp().GetActiveWindow()
        nbook = mainw.GetNotebook()
        buffers = [ page.GetFileName() for page in nbook.GetTextControls() ]
        if fname in buffers:
            page = buffers.index(fname)
            nbook.ChangePage(page)
            cpage = nbook.GetPage(page)
        else:
            nbook.OnDrop([fname])
            cpage = nbook.GetPage(nbook.GetSelection())

        cpage.GotoLine(line)
        cpage.SetFocus()

#-----------------------------------------------------------------------------#
