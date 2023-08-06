

import psutil
from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks
from .base import SysInfoBase


class CpuInfo(SysInfoBase):
    def __init__(self, *args):
        super(CpuInfo, self).__init__(*args)

    def install(self):
        super(CpuInfo, self).install()
        self._items = {
            'frequency': self._frequency,
            'load_avg': self._load_avg
        }

    @inlineCallbacks
    def _frequency(self):
        result = yield threads.deferToThread(psutil.cpu_freq)
        return {
            'current': result.current,
            'min': result.min,
            'max': result.max
        }

    @inlineCallbacks
    def _load_avg(self):
        result = yield threads.deferToThread(psutil.getloadavg)
        return result
