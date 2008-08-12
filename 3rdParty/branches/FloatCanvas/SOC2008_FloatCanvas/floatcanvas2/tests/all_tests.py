import unittest
import glob

files = glob.glob( '*_test.py' )

mainSuite = unittest.TestSuite()
runner = unittest.TextTestRunner()

for filename in files:
    modulename = filename.replace('.py','')
    module = __import__(modulename)
    suite = unittest.defaultTestLoader.loadTestsFromModule( module )
    mainSuite.addTests( suite )
##    if suite.countTestCases() != 0:
##        print '*** Running %s ***' % modulename
##        runner = unittest.TextTestRunner()
##        runner.run( suite )
##    else:
##        print '*** %s is not a unittest, skipping ***' % modulename

runner.run( mainSuite )
