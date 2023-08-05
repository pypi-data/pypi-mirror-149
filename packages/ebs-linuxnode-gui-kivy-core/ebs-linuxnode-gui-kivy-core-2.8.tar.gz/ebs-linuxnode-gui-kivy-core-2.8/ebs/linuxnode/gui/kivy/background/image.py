

import os
from kivy_garden.ebs.core.image import BleedImage

from .base import BackgroundProviderBase


class ImageBackgroundProvider(BackgroundProviderBase):
    def check_support(self, target):
        if not isinstance(target, str):
            return False
        if not os.path.exists(target):
            return False
        _extentions = ('.png', '.jpg', '.bmp', '.gif', '.jpeg')
        if os.path.splitext(target)[1] not in _extentions:
            return False
        return True

    def play(self, target, duration=None, callback=None, **kwargs):
        self._widget = BleedImage(
            source=target,
            allow_stretch=True,
            keep_ratio=True,
            **kwargs
        )
        super(ImageBackgroundProvider, self).play(target, duration, callback, **kwargs)
        return self._widget
