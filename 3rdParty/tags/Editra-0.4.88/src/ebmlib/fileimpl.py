###############################################################################
# Name: Cody Precord                                                          #
# Purpose: File Object Interface Implementation                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
Editra Buisness Model Library: FileObjectImpl

Implementation of a file object interface class. Objects and methods inside
of this library expect a file object that derives from this interface.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#--------------------------------------------------------------------------#
# Imports
import os

# Editra Buisness Model Imports
import fileutil

#--------------------------------------------------------------------------#

class FileObjectImpl(object):
    """File Object Interface implementation base class"""
    def __init__(self, path=u'', modtime=0):
        object.__init__(self)

        # Attributes
        self._path = path
        self._modtime = modtime

        self._handle = None
        self.open = False

        self.last_err = None

    def ClearLastError(self):
        """Reset the error marker on this file"""
        del self.last_err
        self.last_err = None

    def Close(self):
        """Close the file handle
        @note: this is normally done automatically after a read/write operation

        """
        try:
            self._handle.close()
        except:
            pass

        self.open = False

    def DoOpen(self, mode):
        """Opens and creates the internal file object
        @param mode: mode to open file in
        @return: True if opened, False if not
        @postcondition: self._handle is set to the open handle

        """
        if not len(self._path):
            return False

        try:
            file_h = open(self._path, mode)
        except (IOError, OSError), msg:
            self.last_err = msg
            return False
        else:
            self._handle = file_h
            self.open = True
            return True

    def GetExtension(self):
        """Get the files extension if it has one else simply return the
        filename minus the path.
        @return: string file extension (no dot)

        """
        fname = os.path.split(self._path)
        return fname[-1].split(os.extsep)[-1].lower()

    def GetHandle(self):
        """Get this files handle"""
        return self._handle

    def GetLastError(self):
        """Return the last error that occured when using this file
        @return: err traceback or None

        """
        return unicode(self.last_err).replace("u'", "'")

    def GetModtime(self):
        """Get the timestamp of this files last modification"""
        return self._modtime

    def GetPath(self):
        """Get the path of the file
        @return: string

        """
        return self._path

    def GetSize(self):
        """Get the size of the file
        @return: int

        """
        if self._path:
            return fileutil.GetFileSize(self._path)
        else:
            return 0

    @property
    def Handle(self):
        """Raw file handle property"""
        return self._handle

    def IsOpen(self):
        """Check if file is open or not
        @return: bool

        """
        return self.open

    def IsReadOnly(self):
        """Is the file Read Only
        @return: bool

        """
        if os.path.exists(self._path):
            return not os.access(self._path, os.R_OK|os.W_OK)
        else:
            return False

    @property
    def Modtime(self):
        """File modification time propery"""
        return self.GetModtime()

    @property
    def ReadOnly(self):
        """Is the file read only?"""
        return self.IsReadOnly()

    def ResetAll(self):
        """Reset all file attributes"""
        self._handle = None
        self.open = False
        self._path = u''
        self._modtime = 0
        self.last_err = None

    def SetLastError(self, err):
        """Set the last error
        @param err: exception object / msg

        """
        self.last_err = err

    def SetPath(self, path):
        """Set the path of the file
        @param path: absolute path to file

        """
        self._path = path

    def SetModTime(self, mtime):
        """Set the modtime of this file
        @param mtime: long int to set modtime to

        """
        self._modtime = mtime

    def Read(self):
        """Open/Read the file
        @return: string (file contents)

        """
        txt = u''
        if self.DoOpen('rb'):
            try:
                txt = self._handle.read()
            except:
                pass

        return txt
    
    def Write(self, value):
        """Open/Write the value to disk
        @param value: string

        """
        if self.DoOpen('wb'):
            self._handle.write(value)
