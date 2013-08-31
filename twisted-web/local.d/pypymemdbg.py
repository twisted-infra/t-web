import gc, os

from twisted.application.internet import TimerService

class MemoryDebugService(TimerService):
    counter = 0

    def __init__(self):
        TimerService.__init__(self, 60 * 60, self._report)


    def _report(self):
        gc.dump_rpy_heap(b"%d-%d.rpy_heap" % (os.getpid(), self.counter))
        self.counter += 1


MemoryDebugService().setServiceParent(application)
