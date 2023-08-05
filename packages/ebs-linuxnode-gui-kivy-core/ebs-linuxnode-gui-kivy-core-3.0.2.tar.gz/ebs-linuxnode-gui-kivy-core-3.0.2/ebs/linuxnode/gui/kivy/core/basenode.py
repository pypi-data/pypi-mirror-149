

import os
from ebs.linuxnode.gui.kivy.background.mixin import BackgroundMixin
from .text import FontsGuiMixin
from .log import LoggingGuiMixin
from .busy import BusySpinnerGuiMixin
from .nodeid import NodeIDGuiMixin
from .display import DisplayMixin


class BaseIoTNodeGui(NodeIDGuiMixin,
                     BusySpinnerGuiMixin,
                     BackgroundMixin,
                     LoggingGuiMixin,
                     FontsGuiMixin,
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

    def sysinfo_install(self):
        super(BaseIoTNodeGui, self).sysinfo_install()
        self.sysinfo.app.versions.register_package('kivy')
        self.sysinfo.app.versions.register_namespace('kivy-garden')

    def gui_setup(self):
        super(BaseIoTNodeGui, self).gui_setup()
        return self.gui_root
