

import json
from twisted import logger
from twisted.internet.defer import inlineCallbacks
from ebs.linuxnode.core.shell import BaseShellMixin

from .base import SysInfoBase

from .host import HostInfo
from .network import NetworkInfo
from .status import StatusInfo
from .app import AppInfo


class SysinfoContainer(SysInfoBase):
    def install_module(self, name, module):
        m = module(self)
        m.install()
        self._items[name] = m

    def install(self):
        self.install_module('app', AppInfo)
        self.install_module('host', HostInfo)
        self.install_module('network', NetworkInfo)
        self.install_module('status', StatusInfo)

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="sysinfo", source=self)
        return self._log

    @inlineCallbacks
    def write_to_log(self):
        sysinfo = yield self.render()
        self.log.info("System Information : {sysinfo}",
                      sysinfo=json.dumps(sysinfo, indent=2))


class SysinfoMixin(BaseShellMixin):
    def __init__(self, *args, **kwargs):
        super(SysinfoMixin, self).__init__(*args, **kwargs)
        self._sysinfo = SysinfoContainer(self)

    @property
    def sysinfo(self):
        return self._sysinfo

    def install(self):
        super(SysinfoMixin, self).install()
        self.sysinfo.install()
        self.sysinfo_install()
        self.reactor.callWhenRunning(self.sysinfo.write_to_log)

    @property
    @inlineCallbacks
    def network_info(self):
        # Legacy support
        info = yield self.sysinfo.network.info
        if 'ssid' in info.keys():
            return info['ssid']
        elif 'ipaddress' in info.keys():
            return info['ipaddress']
        else:
            return "NONE"
