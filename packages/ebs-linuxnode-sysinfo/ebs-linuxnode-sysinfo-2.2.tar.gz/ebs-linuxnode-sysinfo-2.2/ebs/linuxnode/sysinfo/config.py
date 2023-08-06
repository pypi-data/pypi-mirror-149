

from .base import SysInfoBase


class ConfigInfo(SysInfoBase):
    def __init__(self, *args):
        super(ConfigInfo, self).__init__(*args)

    @property
    def items(self):
        rv = {}
        for key in self.actual.config._elements.keys():
            rv[key] = getattr(self.actual.config, key)
        return rv
