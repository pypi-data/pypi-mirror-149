

from .base import SysInfoBase
from tendril.utils import versions


class VersionsInfo(SysInfoBase):
    def __init__(self, *args):
        super(VersionsInfo, self).__init__(*args)
        self._namespaces = []
        self._packages = []

    def register_namespace(self, namespace):
        if namespace not in self._namespaces:
            self._namespaces.append(namespace)

    def register_package(self, package):
        if package not in self._packages:
            self._packages.append(package)

    @property
    def items(self):
        if not self._items:
            for package in self._packages:
                self._items[package] = versions.get_version(package)
            for namespace in self._namespaces:
                self._items[namespace] = {k: v for k, v in versions.get_versions(namespace)}
        return self._items
