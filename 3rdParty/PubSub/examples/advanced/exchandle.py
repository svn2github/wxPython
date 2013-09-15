'''

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
'''

from pubsub import pub
from pubsub.utils.exchandling import IListenerExcHandler, TracebackInfo


# create one special notification handler that ignores all except
# one type of notification
class MyPubsubExcHandler(IListenerExcHandler):

    def __call__(self, listenerID):
        print 'Exception raised in listener %s during sendMessage()' % listenerID
        print TracebackInfo()


pub.setListenerExcHandler( MyPubsubExcHandler() )

