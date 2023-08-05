

import os
from ebs.linuxnode.gui.kivy.utils.application import BaseIOTNodeApplication
from node import ExampleNode


class ExampleApplication(BaseIOTNodeApplication):
    _node_class = ExampleNode

    def build(self):
        # This is an emergency-only approach. In general, configure
        # roots in the appropriate node classes instead.
        # ( for ex, see BaseIoTNodeGui.install() )
        r = super(ExampleApplication, self).build()
        self._config.register_application_root(
            os.path.abspath(os.path.dirname(__file__))
        )
        return r

    def on_start(self):
        # Config is ready by this point, as long as config elements and
        # application roots are all registered in the install()
        # call-chain.
        self._config.print()
        # Application Roots should also be ready before this
        super(ExampleApplication, self).on_start()
