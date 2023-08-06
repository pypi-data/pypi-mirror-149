

import psutil
from psutil._common import bytes2human
from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks
from .base import SysInfoBase


class DiskInfo(SysInfoBase):
    def __init__(self, *args):
        super(DiskInfo, self).__init__(*args)

    def install(self):
        super(DiskInfo, self).install()
        self._items = {
            'capacity': self._capacity,
            'free': self._free
        }

    @inlineCallbacks
    def _capacity(self):
        result = yield threads.deferToThread(psutil.disk_usage, '/')
        return bytes2human(result.total)

    @inlineCallbacks
    def _free(self):
        result = yield threads.deferToThread(psutil.disk_usage, '/')
        return bytes2human(result.free)
