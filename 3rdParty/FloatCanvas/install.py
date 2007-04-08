#!/usr/bin/env python2.4
'''!
   A script that installs the floatcanvas package in the wxPython lib It
   also installs the demo into the wxPython demo directory, if you set
   the path for that correctly.
   
   CB -- Now use the os.path module to make the install script OS independent.
   
   Issues:
   - SVN's folder .svn doesn't delete with shutil.
   - Demo folder must be hard coded.
'''

import sys, os, shutil
import os.path

import wx

# The installation Directory
InstallDir = os.path.join(wx.__path__[0],"lib","floatcanvas")

# The Demo Directory (Please Set correctly or leave blank.)
Demodir = ''

# ##########################################################################

# Remove the old package if its there the package there.
if os.path.isdir(InstallDir):
    shutil.rmtree(InstallDir)
else:
    print "FloatCanvas failed to install or doesn't exist.\nHave you removed the .svn subfolder fro mthe previous install?"


# Copy-in the flatcavas package from the current working directory.
try:
    print "Copying floatcanvas to:", InstallDir
    shutil.copytree(".%sfloatcanvas"%(os.path.sep),InstallDir)
    # Python raise an exception for one of the file in the folder below. I don't know why. Manual delete works fine.
    print 'If you installed from a SVN package, please remove the .svn folder.'
except:
    print "Failed to copy to install directory, do you have permission to do so?"


# Install the demo if the path is specified.
if Demodir:
    print "Copying the demo to:", DemoDir
    shutil.copyfile(".%sFloatCanvasDemo.py"%(os.path.sep), os.path.join(DemoDir,"FloatCanvas.py") )


