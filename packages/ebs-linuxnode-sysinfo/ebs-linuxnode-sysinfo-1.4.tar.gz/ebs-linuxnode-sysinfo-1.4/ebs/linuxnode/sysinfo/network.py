

import ifcfg
from twisted.internet.defer import inlineCallbacks
from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from .base import SysInfoBase


class WifiNetworkInfo(SysInfoBase):
    @property
    def wifi_ssid(self):
        def _handle_result(result):
            return result.decode().strip()
        d = self._shell_execute(['iwgetid', '-s'], _handle_result)
        return d


class NetworkInfo(WifiNetworkInfo):
    def install(self):
        super(NetworkInfo, self).install()
        _elements = {
            'network_interface_wifi': ElementSpec('network', 'wifi', ItemSpec(fallback='wlan0')),
            'network_interface_ethernet': ElementSpec('network', 'ethernet', ItemSpec(fallback='eth0')),
            'network_interfaces': ElementSpec('_derived', self._network_interfaces)
        }
        for name, spec in _elements.items():
            self.actual.config.register_element(name, spec)

        self._items = {
            'info': 'network_info',
            'interfaces': 'network_interfaces',
        }

    @staticmethod
    def _network_check_interface(interface):
        if_spec = ifcfg.interfaces().get(interface, None)
        if not if_spec:
            return
        if_flags = if_spec['flags'].split('<')[1].split('>')[0].split(',')
        if "UP" in if_flags and "RUNNING" in if_flags:
            return True
        else:
            return False

    @staticmethod
    def _network_get_ipaddress(interface):
        if_spec = ifcfg.interfaces().get(interface, None)
        if not if_spec:
            return
        return if_spec['inet']

    def _network_interfaces(self, config):
        return [config.network_interface_wifi, config.network_interface_ethernet]

    def network_interfaces(self):
        return self.actual.config.network_interfaces

    def network_interfaces_wifi(self):
        return [self.actual.config.network_interface_wifi]

    def network_interfaces_ethernet(self):
        return [self.actual.config.network_interface_ethernet]

    @inlineCallbacks
    def network_info(self):
        rv = {}
        for interface in self.network_interfaces():
            if self._network_check_interface(interface):
                rv['interface'] = interface
                rv['ipaddress'] = self._network_get_ipaddress(interface)
                if interface in self.network_interfaces_wifi():
                    rv['ssid'] = yield self.wifi_ssid
        return rv
