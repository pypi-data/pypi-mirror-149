

import psutil
from psutil._common import bytes2human
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

    def _capacity(self):
        return bytes2human(psutil.virtual_memory().total)

    def _available(self):
        return bytes2human(psutil.virtual_memory().available)
