

from numbers import Number
from kivy_garden.ebs.core.colors import ColorBoxLayout

from .base import BackgroundProviderBase


class ColorBackgroundProvider(BackgroundProviderBase):
    def _parse_color_str(self, target):
        color = target.split(':')
        if len(color) not in (3, 4):
            raise ValueError
        try:
            color = (float(x) for x in color)
        except ValueError:
            raise
        return color

    def check_support(self, target):
        if isinstance(target, str):
            try:
                self._parse_color_str(target)
                return True
            except ValueError:
                return False
        elif isinstance(target, (tuple, list)):
            if len(target) not in (3, 4):
                return False
            for elem in target:
                if not isinstance(elem, Number):
                    return False
        else:
            return False
        return True

    def play(self, target, duration=None, callback=None, **kwargs):
        if isinstance(target, str):
            target = self._parse_color_str(target)
        self._widget = ColorBoxLayout(bgcolor=target)
        super(ColorBackgroundProvider, self).play(target, duration, callback, **kwargs)
        return self._widget
