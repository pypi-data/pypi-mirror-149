

import psutil
from psutil._common import bytes2human
from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks

from .base import SysInfoBase


class MemoryInfo(SysInfoBase):
    def __init__(self, *args):
        super(MemoryInfo, self).__init__(*args)

    def install(self):
        super(MemoryInfo, self).install()
        self._items = {
            'capacity': self._capacity,
            'available': self._available
        }

    @inlineCallbacks
    def _capacity(self):
        result = yield threads.deferToThread(psutil.virtual_memory)
        return bytes2human(result.total)

    @inlineCallbacks
    def _available(self):
        result = yield threads.deferToThread(psutil.virtual_memory)
        return bytes2human(result.available)
