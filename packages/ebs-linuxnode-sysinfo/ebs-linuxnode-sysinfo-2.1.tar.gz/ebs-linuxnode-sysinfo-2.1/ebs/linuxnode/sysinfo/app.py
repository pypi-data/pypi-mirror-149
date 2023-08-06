

from .base import SysInfoBase
from .versions import VersionsInfo
from .config import ConfigInfo


class AppInfo(SysInfoBase):
    def __init__(self, *args):
        super(AppInfo, self).__init__(*args)
        self._app_name = None
        self._app_class = None
        self._versions = None

    def install(self):
        super(AppInfo, self).install()
        self._items = {'name': 'app_name',
                       'class': 'app_class',
                       'versions': VersionsInfo(self.actual),
                       'config': ConfigInfo(self.actual)}

    def app_name(self):
        if not self._app_name:
            self._app_name = self.actual.config.appname
        return self._app_name

    def app_class(self):
        if not self._app_class:
            self._app_class = str(self.actual.__class__)
        return self._app_class
