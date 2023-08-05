

import psutil
from psutil._common import bytes2human
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

    def _capacity(self):
        return bytes2human(psutil.disk_usage('/').total)

    def _free(self):
        return bytes2human(psutil.disk_usage('/').free)
