

from kivy.app import App
from twisted.internet import reactor

from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class BaseIOTNodeApplication(App):
    _node_class = BaseIoTNodeGui

    def __init__(self, config, *args, **kwargs):
        self._config = config
        self._debug = kwargs.pop('debug', False)
        super(BaseIOTNodeApplication, self).__init__(*args, **kwargs)
        self._node = None

    def build(self):
        print("Constructing Node : {}".format(self._node_class))
        self._node = self._node_class(reactor=reactor, application=self)
        print("Installing Node Resources")
        self._node.install()

        # Config is ready by this point, as long as config elements and
        # application roots are all registered in the install()
        # call-chain.
        self._config.print()

        print("Using Application Roots :")
        for root in self._config.roots:
            print("  ", root)

        print("Building GUI for node {0}".format(self._node))
        return self._node.gui_setup()

    def on_start(self):
        print("Starting Application : {}".format(self))
        self._node.start()

    def on_stop(self):
        self._node.stop()

    def on_pause(self):
        pass
