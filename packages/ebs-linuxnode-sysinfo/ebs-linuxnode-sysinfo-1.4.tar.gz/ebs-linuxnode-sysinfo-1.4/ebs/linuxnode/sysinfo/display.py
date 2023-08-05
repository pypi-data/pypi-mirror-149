

import pyedid
from functools import partial
from glob import glob
from ebs.linuxnode.core.config import ElementSpec, ItemSpec

from .base import SysInfoBase


class DisplayInfo(SysInfoBase):
    def __init__(self, *args):
        super(DisplayInfo, self).__init__(*args)
        self._names = []

    def install(self):
        super(DisplayInfo, self).install()

        _elements = {
            'sysinfo_display': ElementSpec('sysinfo', 'display', ItemSpec(fallback=None)),
        }

        for element, element_spec in _elements.items():
            self.actual.config.register_element(element, element_spec)

        if self.actual.config.sysinfo_display:
            candidates = [self.actual.config.sysinfo_display]
        else:
            candidates = glob('/sys/class/drm/*-HDMI-*/edid') + \
                glob('/sys/class/drm/*-DP-*/edid')
        for candidate in candidates:
            name = candidate[len('/sys/class/drm/'):(-1 * len('/edid'))]
            self._items[name] = partial(self._display_edid, candidate)
            self._names.append(name)

        self._items['connected'] = self._display_connected

    def _display_edid(self, path):
        with open(path, 'rb') as f:
            content = f.read()
        try:
            edid_info = pyedid.parse_edid(content)
            rv = {
                'detected': True, 'serial': edid_info.serial,
                'product_id': edid_info.product_id, 'manufacturer_id': edid_info.manufacturer_id,
                'name': edid_info.name, 'manufacturer': edid_info.manufacturer,
                'width': edid_info.width, 'height': edid_info.height,
            }
            return rv
        except ValueError:
            return {'detected': False}

    def _display_connected(self):
        for name in self._names:
            info = getattr(self, name)
            if info['detected']:
                return True
        else:
            return False
