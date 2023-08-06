

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from .basemixin import BaseGuiMixin


class DisplayMixin(BaseGuiMixin):
    def install(self):
        super(DisplayMixin, self).install()
        _elements = {
            'fullscreen': ElementSpec('display', 'fullscreen', ItemSpec(bool, fallback=True)),
            'portrait': ElementSpec('display', 'portrait', ItemSpec(bool, read_only=False, fallback=False)),
            'flip': ElementSpec('display', 'flip', ItemSpec(bool, read_only=False, fallback=False)),
            'orientation': ElementSpec('_derived', self._orientation),
            'os_rotation': ElementSpec('display', 'os_rotation', ItemSpec(bool, fallback=False)),
            'app_dispmanx_layer': ElementSpec('display-rpi', 'dispmanx_app_layer', ItemSpec(int, fallback=5))
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    def _orientation(self, config):
        rv = 0
        if config.portrait is True:
            rv += 90
        if config.flip:
            rv += 180
        return rv

    def orientation_update(self):
        from kivy.config import Config
        Config.set('graphics', 'rotation', self.config.orientation)
