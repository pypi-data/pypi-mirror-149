

import re
import psutil
import platform
from raspi_system import hwinfo
from twisted.internet.defer import inlineCallbacks
from .base import SysInfoBase


class HostInfo(SysInfoBase):
    def __init__(self, *args):
        super(HostInfo, self).__init__(*args)
        self._hostname = None
        self._machine_id = None
        self._boot_id = None
        self._operating_system = None
        self._kernel = None
        self._architecture = None
        self._hardware_vendor = None
        self._hardware_model = None
        self._cpu_name = None

    def install(self):
        super(HostInfo, self).install()
        self._items = {
            'hostname': 'hostname',
            'machine_id': 'machine_id',
            'boot_id': 'boot_id',
            'operating_system': 'operating_system',
            'kernel': 'kernel',
            'architecture': 'architecture',
            'hardware_vendor': 'hardware_vendor',
            'hardware_model': 'hardware_model',
            'cpu_name': 'cpu_name',
            'cpu_cores': '_cpu_cores',
        }

    _hnc_items = {
        'static hostname': '_hostname',
        'machine id': '_machine_id',
        'boot id': '_boot_id',
        'operating system': '_operating_system',
        'kernel': '_kernel',
        'architecture': '_architecture',
        'hardware vendor': '_hardware_vendor',
        'hardware model': '_hardware_model',
    }

    def _hostnamectl(self):
        def _parse_result(result):
            rval = {}
            for row in result.split(b'\n'):
                try:
                    tag, value = row.split(b':')
                except ValueError:
                    continue
                tag = tag.strip().lower().decode('utf-8')
                value = value.strip().decode('utf-8')
                if tag in self._hnc_items.keys():
                    rval[self._hnc_items[tag]] = value
            return rval
        d = self._shell_execute(['hostnamectl'], _parse_result)

        def _save_result(result):
            for k, v in result.items():
                setattr(self, k, v)

        d.addCallback(_save_result)
        return d

    @inlineCallbacks
    def hostname(self):
        if not self._hostname:
            yield self._hostnamectl()
        return self._hostname

    @inlineCallbacks
    def machine_id(self):
        if not self._machine_id:
            yield self._hostnamectl()
        return self._machine_id

    @inlineCallbacks
    def boot_id(self):
        if not self._boot_id:
            yield self._hostnamectl()
        return self._boot_id

    @inlineCallbacks
    def operating_system(self):
        if not self._operating_system:
            yield self._hostnamectl()
        return self._operating_system

    @inlineCallbacks
    def kernel(self):
        if not self._kernel:
            yield self._hostnamectl()
        return self._kernel

    @inlineCallbacks
    def architecture(self):
        if not self._architecture:
            yield self._hostnamectl()
        return self._architecture

    @inlineCallbacks
    def hardware_vendor(self):
        if not self._hardware_vendor:
            yield self._hostnamectl()
        if not self._hardware_vendor and self.actual.config.platform == 'rpi':
            if hwinfo.is_pi3() or hwinfo.is_pi4():
                self._hardware_vendor = "Raspberry Pi Foundation"
        return self._hardware_vendor

    @inlineCallbacks
    def hardware_model(self):
        if not self._hardware_model:
            yield self._hostnamectl()
        if not self._hardware_model and self.actual.config.platform == 'rpi':
            if hwinfo.is_pi3() or hwinfo.is_pi4():
                self._hardware_model = "{} {}".format(hwinfo.model_string(), hwinfo.model_revcode())
        return self._hardware_model

    def _cpu_cores(self):
        return psutil.cpu_count()

    @staticmethod
    def _parse_cpuinfo(output):
        output = output.decode()
        for line in output.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1).strip()

    @inlineCallbacks
    def cpu_name(self):
        if not self._cpu_name:
            if platform.system() == "Windows":
                self._cpu_name = platform.processor()
            elif platform.system() == "Linux":
                self._cpu_name = yield self._shell_execute(['cat', '/proc/cpuinfo'], self._parse_cpuinfo)
        return self._cpu_name
