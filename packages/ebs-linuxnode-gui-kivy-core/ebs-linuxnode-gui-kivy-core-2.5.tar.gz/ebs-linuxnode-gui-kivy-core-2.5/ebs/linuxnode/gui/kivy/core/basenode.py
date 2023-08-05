

import os
from ebs.linuxnode.gui.kivy.background.mixin import OverlayWindowGuiMixin
from .text import FontsGuiMixin
from .log import LoggingGuiMixin
from .busy import BusySpinnerGuiMixin
from .nodeid import NodeIDGuiMixin
from .display import DisplayMixin


class BaseIoTNodeGui(NodeIDGuiMixin,
                     BusySpinnerGuiMixin,
                     LoggingGuiMixin,
                     FontsGuiMixin,
                     OverlayWindowGuiMixin,
                     DisplayMixin):

    def __init__(self, *args, **kwargs):
        self._application = kwargs.pop('application')
        self._gui_root = None
        super(BaseIoTNodeGui, self).__init__(*args, **kwargs)

    def install(self):
        super(BaseIoTNodeGui, self).install()
        self.config.register_application_root(
            os.path.abspath(os.path.dirname(__file__))
        )

    def gui_setup(self):
        super(BaseIoTNodeGui, self).gui_setup()
        return self.gui_root
