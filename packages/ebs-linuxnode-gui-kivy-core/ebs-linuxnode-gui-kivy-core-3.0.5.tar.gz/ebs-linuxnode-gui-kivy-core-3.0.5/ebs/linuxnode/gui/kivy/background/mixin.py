

import os
import shutil
import appdirs

from kivy.uix.boxlayout import BoxLayout

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.core.background import BackgroundCoreMixin
from ebs.linuxnode.gui.kivy.core.basemixin import BaseGuiMixin

from .image import ImageBackgroundProvider
from .color import ColorBackgroundProvider
from .structured import StructuredBackgroundProvider


class BackgroundGuiMixin(BaseGuiMixin, BackgroundCoreMixin):
    def __init__(self, *args, **kwargs):
        self._bg_container = None
        super(BackgroundGuiMixin, self).__init__(*args, **kwargs)

    def _background_fallback(self):
        _path = os.path.abspath(os.path.dirname(__file__))
        fallback_default = os.path.join(_path, 'images/background.png')
        fallback = os.path.join(self.config_dir, 'background.png')
        if not os.path.exists(fallback):
            shutil.copy(fallback_default, fallback)
        return fallback

    def install(self):
        super(BackgroundGuiMixin, self).install()
        _elements = {
            'image_bgcolor': ElementSpec('display', 'image_bgcolor', ItemSpec('kivy_color', fallback='auto')),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

        self.install_background_provider(ColorBackgroundProvider(self))
        self.install_background_provider(ImageBackgroundProvider(self))
        self.install_background_provider(StructuredBackgroundProvider(self))

    @property
    def gui_bg_container(self):
        if self._bg_container is None:
            self._bg_container = BoxLayout()
            self.gui_main_content.add_widget(self._bg_container)
        return self._bg_container

    def bg_clear(self):
        if self._bg and self._bg.parent:
            self.gui_bg_container.remove_widget(self._bg)
        super(BackgroundGuiMixin, self).bg_clear()

    @BackgroundCoreMixin.bg.setter
    def bg(self, value):
        updated = BackgroundCoreMixin.bg.fset(self, value)
        if updated:
            self.gui_bg_container.add_widget(self._bg)

    def bg_pause(self):
        self.gui_main_content.remove_widget(self._bg_container)
        super(BackgroundGuiMixin, self).bg_pause()

    def bg_resume(self):
        super(BackgroundGuiMixin, self).bg_resume()
        if not self._bg_container.parent:
            self.gui_main_content.add_widget(self._bg_container, len(self.gui_main_content.children))

    def start(self):
        super(BackgroundGuiMixin, self).start()
        self.reactor.callLater(3, self.bg_update)

    def gui_setup(self):
        gui = super(BackgroundGuiMixin, self).gui_setup()
        _ = self.gui_bg_container
        return gui
