#!/usr/bin/env python2.4

# A script that installs the floatcanvas package in the wxPython lib It
# also installs the demo into the wxPython demo directory, if you set
# the path for that correctly NOTE: I can't figure out how to get
# distutils to put it into a subpackage of an existing package.
#   Now I do: package_dir = {"wx/lib": ""} or something like that should work.

DemoDir = "/home/cbarker/wxPython-2.6.3.0/demo"

import sys, os, shutil

import wx

InstallDir = wx.__path__[0]+"/lib/floatcanvas"


print "Copying floatcanvas to:", InstallDir
# copy the package there.
shutil.rmtree(InstallDir)
shutil.copytree("./floatcanvas",InstallDir)

#print SITE_PACKAGES
#SITE_PACKAGES=/usr/lib/python2.3/site-packages
#cp -r floatcanvas/ $SITE_PACKAGES/wxPython/lib/

# Now install the demo:

print "Copying the demo to:", DemoDir
shutil.copyfile("./FloatCanvasDemo.py", os.path.join(DemoDir,"FloatCanvas.py") )


