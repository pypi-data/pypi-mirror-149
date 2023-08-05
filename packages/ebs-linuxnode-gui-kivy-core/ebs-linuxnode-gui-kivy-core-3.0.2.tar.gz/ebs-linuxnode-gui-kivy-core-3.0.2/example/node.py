

from twisted.internet import reactor
from kivy_garden.ebs.clocks.digital import SimpleDigitalClock
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui


class ExampleNode(BaseIoTNodeGui):
    @property
    def clock(self):
        return SimpleDigitalClock()

    def _set_bg(self, target):
        self.gui_bg = target

    def _background_examples(self):
        reactor.callLater(10, self._set_bg, '1.0:0.5:0.5:1.0')
        reactor.callLater(20, self._set_bg, 'image.jpg')
        reactor.callLater(30, self._set_bg, '0.5:1.0:0.5:1.0')
        reactor.callLater(40, self._set_bg, None)
        # Install kivy_garden.ebs.clocks
        # reactor.callLater(50, self._set_bg, 'structured:clock')

    def _enter_overlay_mode(self):
        self.overlay_mode = True

    def _exit_overlay_mode(self):
        self.overlay_mode = False

    def _overlay_examples(self):
        reactor.callLater(10, self._enter_overlay_mode)
        reactor.callLater(30, self._exit_overlay_mode)

    def start(self):
        super(ExampleNode, self).start()
        self._background_examples()
