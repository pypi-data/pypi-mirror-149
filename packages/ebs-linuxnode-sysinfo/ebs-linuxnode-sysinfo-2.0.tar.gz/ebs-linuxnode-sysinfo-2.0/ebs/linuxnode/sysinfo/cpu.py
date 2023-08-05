

import psutil
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

    def _frequency(self):
        result = psutil.cpu_freq()
        return {
            'current': result.current,
            'min': result.min,
            'max': result.max
        }

    def _load_avg(self):
        return psutil.getloadavg()
