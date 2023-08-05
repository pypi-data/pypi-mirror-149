

import os
import shutil
import appdirs
from collections import namedtuple

from kivy.uix.boxlayout import BoxLayout

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.gui.kivy.core.basemixin import BaseGuiMixin

from .base import BackgroundProviderBase
from .image import ImageBackgroundProvider
from .color import ColorBackgroundProvider
from .structured import StructuredBackgroundProvider


# TODO This is here, but not particularly tested. Expect it to only work for video.
# In general, background sequencing should be handled outside the Background code or
# by dedicated infrastructure with effectively allows gui_bg to accept a list of this class.
BackgroundSpec = namedtuple('BackgroundSpec', ["target", "bgcolor", "callback", "duration"],
                            defaults=[None, None, None])


class BackgroundGuiMixin(BaseGuiMixin):
    def __init__(self, *args, **kwargs):
        self._bg_providers = []
        self._bg_container = None
        self._bg = None
        self._bg_current = None
        self._bg_current_provider = None
        super(BackgroundGuiMixin, self).__init__(*args, **kwargs)

    def install_background_provider(self, provider):
        self.log.info("Installing BG Provider {}".format(provider))
        self._bg_providers.insert(0, provider)

    def install(self):
        super(BackgroundGuiMixin, self).install()

        _path = os.path.abspath(os.path.dirname(__file__))
        fallback_default = os.path.join(_path, 'images/background.png')
        fallback = os.path.join(appdirs.user_config_dir(self.config.appname), 'background.png')
        if not os.path.exists(fallback):
            shutil.copy(fallback_default, fallback)

        _elements = {
            'image_bgcolor': ElementSpec('display', 'image_bgcolor', ItemSpec('kivy_color', fallback='auto')),
            'background': ElementSpec('display', 'background', ItemSpec(str, read_only=False, fallback=fallback)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

        self.install_background_provider(ColorBackgroundProvider(self))
        self.install_background_provider(ImageBackgroundProvider(self))
        self.install_background_provider(StructuredBackgroundProvider(self))

    def _get_provider(self, target):
        provider: BackgroundProviderBase
        provider = None
        for lprovider in self._bg_providers:
            if lprovider.check_support(target):
                provider = lprovider
                break
        return provider

    def background_set(self, target):
        if not target:
            target = None

        provider = self._get_provider(target)
        if not provider:
            self.log.warn("Provider not found for background {}. Not Setting.".format(target))
            target = None

        if target and self.config.background != target:
            self.config.background = target

        self.gui_bg_update()

    @property
    def gui_bg_container(self):
        if self._bg_container is None:
            self._bg_container = BoxLayout()
            self.gui_main_content.add_widget(self._bg_container)
        return self._bg_container

    def gui_bg_clear(self):
        if self._bg and self._bg.parent:
            self.gui_bg_container.remove_widget(self._bg)
        self._bg = None
        if self._bg_current_provider:
            self._bg_current_provider.stop()

    @property
    def gui_bg(self):
        return self._bg_current

    @gui_bg.setter
    def gui_bg(self, value):
        self.log.info("Setting background to {value}", value=value)
        bgcolor, callback, duration = None, None, None
        if isinstance(value, BackgroundSpec):
            value, bgcolor, callback, duration = value

        if not bgcolor:
            bgcolor = self.config.image_bgcolor

        provider = self._get_provider(value)

        if not provider:
            self.log.warn("Provider not found for background {}".format(value))
            value = self.config.background
            provider = self._get_provider(value)
            self.log.warn("Tryin to use {} instead.".format(value))

        if not provider:
            self.log.warn("Unable to display config background. Clearing from config.")
            self.config.remove('background')
            value = self.config.background
            provider = self._get_provider(value)

        self.log.debug("Using {} to show background {}".format(provider, value))
        self.gui_bg_clear()

        self._bg_current = value
        self._bg_current_provider = provider
        self._bg = self._bg_current_provider.play(
            value, bgcolor=bgcolor, callback=callback, duration=duration
        )
        self.gui_bg_container.add_widget(self._bg)

    def gui_bg_pause(self):
        self.log.debug("Pausing Background")
        self.gui_main_content.remove_widget(self._bg_container)
        if self._bg_current_provider:
            self._bg_current_provider.pause()

    def gui_bg_resume(self):
        self.log.debug("Resuming Background")
        if self._bg_current_provider:
            self._bg_current_provider.resume()
        if not self._bg_container.parent:
            self.gui_main_content.add_widget(self._bg_container, len(self.gui_main_content.children))

    def start(self):
        super(BackgroundGuiMixin, self).start()
        self.reactor.callLater(3, self.gui_bg_update)

    def stop(self):
        if self._bg_current_provider:
            self._bg_current_provider.stop()
        super(BackgroundGuiMixin, self).stop()

    def gui_bg_update(self):
        self.gui_bg = self.config.background

    def gui_setup(self):
        gui = super(BackgroundGuiMixin, self).gui_setup()
        _ = self.gui_bg_container
        return gui
