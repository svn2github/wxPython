/////////////////////////////////////////////////////////////////////////////
// Name:        _taskbar.i
// Purpose:     SWIG interface defs for wxTaskBarIcon
//
// Author:      Robin Dunn
//
// Created:     2-June-1998
// RCS-ID:      $Id$
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

%{
%}

//---------------------------------------------------------------------------
%newgroup;


%{
#ifndef wxHAS_TASK_BAR_ICON
// implement dummy classes for platforms that don't have it

class wxTaskBarIcon : public wxEvtHandler
{
public:
    wxTaskBarIcon()  { wxPyRaiseNotImplemented(); }
};


class wxTaskBarIconEvent : public wxEvent
{
public:
    wxTaskBarIconEvent(wxEventType, wxTaskBarIcon *)
        { wxPyRaiseNotImplemented(); }
    virtual wxEvent* Clone() const { return NULL; }
    bool IsOk() const { return false; }
    bool IsIconInstalled() const { return false; }
    bool SetIcon(const wxIcon& icon, const wxString& tooltip = wxPyEmptyString) { return false; }
    bool RemoveIcon() { return false; }
    bool PopupMenu(wxMenu *menu) { return false; }
};

enum {
    wxEVT_TASKBAR_MOVE = 0,
    wxEVT_TASKBAR_LEFT_DOWN = 0,
    wxEVT_TASKBAR_LEFT_UP = 0,
    wxEVT_TASKBAR_RIGHT_DOWN = 0,
    wxEVT_TASKBAR_RIGHT_UP = 0,
    wxEVT_TASKBAR_LEFT_DCLICK = 0,
    wxEVT_TASKBAR_RIGHT_DCLICK = 0,
};


#else
// Otherwise make a class that can virtualize CreatePopupMenu

inline wxPyObject &operator>>(wxPyObject &po, wxMenu *&obj)
{
    wxPyExtractObject(wxT("wxMenu"), po, obj);
    return po;
}

class wxPyTaskBarIcon : public wxTaskBarIcon
{
    DECLARE_ABSTRACT_CLASS(wxPyTaskBarIcon)
public:
    wxPyTaskBarIcon() : wxTaskBarIcon()
    {}

    PYCALLBACK_0_EXTRACT(wxTaskBarIcon, wxMenu*, rval = NULL, CreatePopupMenu)

    PYPRIVATE;
};

IMPLEMENT_ABSTRACT_CLASS(wxPyTaskBarIcon, wxTaskBarIcon);

#endif
%}


MustHaveApp(wxPyTaskBarIcon);

%rename(TaskBarIcon) wxPyTaskBarIcon;
class wxPyTaskBarIcon : public wxEvtHandler
{
public:
    %pythonAppend wxPyTaskBarIcon   setCallbackInfo(TaskBarIcon)

    wxPyTaskBarIcon();
    ~wxPyTaskBarIcon();

    void _setCallbackInfo(PyObject* self, PyObject* _class, int incref=0);

    void Destroy();
    
    bool IsOk() const;
    %pythoncode { def __nonzero__(self): return self.IsOk() }

    bool IsIconInstalled() const;

    bool SetIcon(const wxIcon& icon, const wxString& tooltip = wxPyEmptyString);
    bool RemoveIcon();
    bool PopupMenu(wxMenu *menu);

    DocStr(ShowBalloon,
           "Show a balloon notification (the icon must have been already
initialized using SetIcon).  Only implemented for Windows.

title and text are limited to 63 and 255 characters respectively, msec
is the timeout, in milliseconds, before the balloon disappears (will
be clamped down to the allowed 10-30s range by Windows if it's outside
it) and flags can include wxICON_ERROR/INFO/WARNING to show a
corresponding icon

Returns True if balloon was shown, False on error (incorrect parameters
or function unsupported by OS)
", "");
#ifdef __WXMSW__
    bool ShowBalloon(const wxString& title,
                     const wxString& text,
                     unsigned msec = 0,
                     int flags = 0);

#else
    %extend {
        bool ShowBalloon(const wxString& title,
                         const wxString& text,
                         unsigned msec = 0,
                         int flags = 0)  { return false; }
    }
#endif    
};



class wxTaskBarIconEvent : public wxEvent
{
public:
    wxTaskBarIconEvent(wxEventType evtType, wxTaskBarIcon *tbIcon);
};



%constant wxEventType wxEVT_TASKBAR_MOVE;
%constant wxEventType wxEVT_TASKBAR_LEFT_DOWN;
%constant wxEventType wxEVT_TASKBAR_LEFT_UP;
%constant wxEventType wxEVT_TASKBAR_RIGHT_DOWN;
%constant wxEventType wxEVT_TASKBAR_RIGHT_UP;
%constant wxEventType wxEVT_TASKBAR_LEFT_DCLICK;
%constant wxEventType wxEVT_TASKBAR_RIGHT_DCLICK;
%constant wxEventType wxEVT_TASKBAR_CLICK;
%constant wxEventType wxEVT_TASKBAR_BALLOON_TIMEOUT;
%constant wxEventType wxEVT_TASKBAR_BALLOON_CLICK;


%pythoncode {
EVT_TASKBAR_MOVE = wx.PyEventBinder (         wxEVT_TASKBAR_MOVE )
EVT_TASKBAR_LEFT_DOWN = wx.PyEventBinder (    wxEVT_TASKBAR_LEFT_DOWN )
EVT_TASKBAR_LEFT_UP = wx.PyEventBinder (      wxEVT_TASKBAR_LEFT_UP )
EVT_TASKBAR_RIGHT_DOWN = wx.PyEventBinder (   wxEVT_TASKBAR_RIGHT_DOWN )
EVT_TASKBAR_RIGHT_UP = wx.PyEventBinder (     wxEVT_TASKBAR_RIGHT_UP )
EVT_TASKBAR_LEFT_DCLICK = wx.PyEventBinder (  wxEVT_TASKBAR_LEFT_DCLICK )
EVT_TASKBAR_RIGHT_DCLICK = wx.PyEventBinder ( wxEVT_TASKBAR_RIGHT_DCLICK )
EVT_TASKBAR_CLICK =  wx.PyEventBinder (       wxEVT_TASKBAR_CLICK )
EVT_TASKBAR_BALLOON_TIMEOUT = wx.PyEventBinder ( wxEVT_TASKBAR_BALLOON_TIMEOUT )
EVT_TASKBAR_BALLOON_CLICK = wx.PyEventBinder ( wxEVT_TASKBAR_BALLOON_CLICK )
}

//---------------------------------------------------------------------------
