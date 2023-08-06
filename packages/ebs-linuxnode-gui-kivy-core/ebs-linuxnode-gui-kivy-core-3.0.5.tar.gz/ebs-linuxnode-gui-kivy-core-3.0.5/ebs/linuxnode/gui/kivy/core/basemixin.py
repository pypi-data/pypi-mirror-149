

from .structure import BaseGuiStructureMixin
from kivy_garden.ebs.core.colors import GuiPalette


class BaseGuiMixin(BaseGuiStructureMixin):
    _palette = GuiPalette(
        background=(0x00 / 255, 0x00 / 255, 0x00 / 255),
        foreground=(0xff / 255, 0xff / 255, 0xff / 255),
        color_1=(0x00 / 255, 0x00 / 255, 0xff / 255),
        color_2=(0xff / 255, 0x00 / 255, 0x00 / 255)
    )

    def gui_setup(self):
        pass

    @property
    def gui_color_1(self):
        return self._palette.color_1

    @property
    def gui_color_2(self):
        return self._palette.color_2

    @property
    def gui_color_foreground(self):
        return self._palette.foreground

    @property
    def gui_color_background(self):
        return self._palette.background
