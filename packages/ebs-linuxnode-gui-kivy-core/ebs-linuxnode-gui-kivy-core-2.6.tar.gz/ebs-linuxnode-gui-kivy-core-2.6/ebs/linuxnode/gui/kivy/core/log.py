
from twisted.logger import formatEvent

from datetime import datetime
from collections import deque
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.utils import get_hex_from_color

from kivy_garden.ebs.core.labels import ColorLabel
from ebs.linuxnode.core.log import NodeLoggingMixin
from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from .basemixin import BaseGuiMixin


class LoggingGuiMixin(BaseGuiMixin):
    def __init__(self, *args, **kwargs):
        self._gui_log = None
        self._gui_log_end = None
        self._gui_log_layout = None
        self._gui_log_scroll = None
        self._gui_log_lines = deque([], maxlen=100)
        super(LoggingGuiMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(LoggingGuiMixin, self).install()
        _elements = {
            'gui_log_display': ElementSpec('debug', 'gui_log_display', ItemSpec(bool, fallback=False)),
            'gui_log_level': ElementSpec('debug', 'gui_log_level', ItemSpec(fallback='info')),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    def _observers(self):
        rv = NodeLoggingMixin._observers(self)
        if self.config.gui_log_display:
            rv.extend([self.gui_log_observer])
        return rv

    _level_ignore_map = {
        'trace': [],
        'debug': ['trace'],
        'info': ['trace', 'debug'],
        'warning': ['trace', 'debug', 'info'],
        'error': ['trace', 'debug', 'info', 'error'],
    }

    def gui_log_observer(self, event):
        ll = event['log_level'].name
        if ll in self._level_ignore_map[self.config.gui_log_level]:
            return
        msg = "[font=RobotoMono-Regular][{0:^8}][/font] {1} {2}".format(
            ll.upper(),
            datetime.fromtimestamp(event['log_time']).strftime("%d%m %H:%M:%S"),
            formatEvent(event)
        )
        color = None
        if ll == 'warn':
            color = [1, 1, 0, 1]
        elif ll == 'error':
            color = [1, 0, 0, 1]
        elif ll == 'critical':
            color = [1, 0, 0, 1]
        if color:
            color = get_hex_from_color(color)
            msg = '[color={0}]{1}[/color]'.format(color, msg)

        self._gui_log_lines.append(msg)
        self._gui_log.text = '\n'.join(self._gui_log_lines)

    @property
    def gui_log(self):
        if not self._gui_log:
            self._gui_log_scroll = ScrollView(
                size_hint=(None, None), bar_pos_y='right',
                bar_color=[1, 1, 1, 1], effect_cls=ScrollEffect,
                do_scroll_x=False, do_scroll_y=True)

            def _set_log_size(_, size):
                width = min(max(700, size[0] * 0.3), size[0])
                height = size[1] * 0.6
                self._gui_log_scroll.size = width, height
            self.gui_root.bind(size=_set_log_size)

            self._gui_log_layout = BoxLayout(orientation='vertical',
                                             size_hint=(1, None))

            self._gui_log = ColorLabel(
                size_hint=(1, 1), padding=(8, 8), bgcolor=[0, 0, 0, 0.2],
                halign='left', valign='top', markup=True, font_size='12sp',
            )

            self._gui_log_end = Label(size_hint=(1, None), height=1)

            def _set_label_height(_, size):
                if size[1] > Window.height * 0.3:
                    self._gui_log.height = size[1]
                else:
                    self._gui_log.height = Window.height * 0.3
            self._gui_log.bind(texture_size=_set_label_height)

            def _set_layout_height(_, size):
                if size[1] > Window.height * 0.3:
                    self._gui_log_layout.height = size[1]
                else:
                    self._gui_log_layout.height = Window.height * 0.3
                self._gui_log_scroll.scroll_to(self._gui_log_end)
            self._gui_log.bind(texture_size=_set_layout_height)

            def _set_text_width(_, size):
                self._gui_log.text_size = size[0], None
            self._gui_log.bind(size=_set_text_width)

            self._gui_log_layout.add_widget(self._gui_log)
            self._gui_log_layout.add_widget(self._gui_log_end)
            self._gui_log_scroll.add_widget(self._gui_log_layout)
            self.gui_debug_stack.add_widget(self._gui_log_scroll)
        return self._gui_log

    def gui_setup(self):
        super(LoggingGuiMixin, self).gui_setup()
        if not self.config.gui_log_display:
            return
        _ = self.gui_log
