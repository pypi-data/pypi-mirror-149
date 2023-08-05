

import json
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from ebs.linuxnode.core import config
from ebs.linuxnode.core.basenode import BaseIoTNode

from ebs.linuxnode.sysinfo import SysinfoMixin


class ExampleNode(SysinfoMixin, BaseIoTNode):
    @inlineCallbacks
    def test_sysinfo(self):
        print("Executing Sysinfo Modules")
        sysinfo = yield self.sysinfo.render()
        print(json.dumps(sysinfo, indent=4))
        print(self.network_info)

    def start(self):
        self.install()
        super(ExampleNode, self).start()
        self.config.print()
        reactor.callLater(5, self.test_sysinfo)
        reactor.callLater(60, self.stop)
        reactor.run()

    def stop(self):
        super(ExampleNode, self).stop()
        reactor.stop()


def main():
    nodeconfig = config.IoTNodeConfig()
    config.current_config = nodeconfig

    node = ExampleNode(reactor=reactor)
    node.start()


if __name__ == '__main__':
    main()
