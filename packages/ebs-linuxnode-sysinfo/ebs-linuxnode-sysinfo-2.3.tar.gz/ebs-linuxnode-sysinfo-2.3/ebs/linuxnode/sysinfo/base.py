

from twisted.internet.defer import inlineCallbacks


class SysInfoBase(object):
    def __init__(self, actual):
        self._log = None
        self._actual = actual
        self._items = {}

    @property
    def log(self):
        return self._log or self._actual.log

    @property
    def items(self):
        return self._items

    @property
    def actual(self):
        if hasattr(self._actual, '_actual'):
            return self._actual._actual
        else:
            return self._actual

    def _shell_execute(self, *args, **kwargs):
        return self._actual._shell_execute(*args, **kwargs)

    def install(self):
        pass

    @inlineCallbacks
    def render(self):
        rval = {}
        for k, v in self.items.items():
            if callable(v):
                rval[k] = yield v()
            elif hasattr(v, 'render'):
                rval[k] = yield v.render()
            elif not isinstance(v, str):
                rval[k] = v
            elif hasattr(self, v):
                if callable(getattr(self, v)):
                    rval[k] = yield getattr(self, v)()
                else:
                    rval[k] = yield getattr(self, v)
            else:
                rval[k] = v
        return rval

    def __getattr__(self, item):
        if item in self.items.keys():
            v = self.items[item]
            if callable(v):
                return v()
            if not isinstance(v, str):
                return v
            if callable(getattr(self, v)):
                rval = getattr(self, v)()
            else:
                rval = getattr(self, v)
            return rval
        raise AttributeError
