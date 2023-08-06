

import psutil
import time
from .cpu import CpuInfo
from .disks import DiskInfo
from .memory import MemoryInfo
from .display import DisplayInfo
from .temperature import TemperatureInfo
from .base import SysInfoBase

from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks


class StatusInfo(SysInfoBase):
    def __init__(self, *args):
        super(StatusInfo, self).__init__(*args)

    def install(self):
        super(StatusInfo, self).install()
        temperature = TemperatureInfo(self.actual)
        temperature.install()
        disks = DiskInfo(self.actual)
        disks.install()
        memory = MemoryInfo(self.actual)
        memory.install()
        display = DisplayInfo(self.actual)
        display.install()
        cpu = CpuInfo(self.actual)
        cpu.install()
        self._items = {
            'uptime': self._uptime,
            'cpu': cpu,
            'disks': disks,
            'memory': memory,
            'display': display,
            'temperature': temperature,
        }

    @inlineCallbacks
    def _uptime(self):
        boot_time = yield threads.deferToThread(psutil.boot_time)
        return time.time() - boot_time
