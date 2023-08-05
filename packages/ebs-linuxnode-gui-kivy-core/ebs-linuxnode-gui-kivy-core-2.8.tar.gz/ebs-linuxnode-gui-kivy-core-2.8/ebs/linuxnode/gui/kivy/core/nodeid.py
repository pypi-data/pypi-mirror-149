

from twisted.internet import task

from kivy_garden.ebs.core.labels import ColorLabel
from kivy_garden.ebs.core.colors import color_set_alpha

from .basemixin import BaseGuiMixin
from ebs.linuxnode.core.config import ElementSpec, ItemSpec


class NodeIDGuiMixin(BaseGuiMixin):
    _gui_nodeid_bgcolor = None
    _gui_nodeid_color = None

    def __init__(self, *args, **kwargs):
        super(NodeIDGuiMixin, self).__init__(*args, **kwargs)
        self._gui_id_tag = None
        self._gui_id_task = None

    def install(self):
        super(NodeIDGuiMixin, self).install()
        _elements = {
            'node_id_display': ElementSpec('id', 'display', ItemSpec(bool, fallback=False)),
            'node_id_display_frequency': ElementSpec('id', 'display_frequency', ItemSpec(int, fallback=0)),
            'node_id_display_duration': ElementSpec('id', 'display_duration', ItemSpec(int, fallback=15)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    @property
    def gui_id_tag(self):
        if not self._gui_id_tag:
            params = {'bgcolor': (self._gui_nodeid_bgcolor or
                                  color_set_alpha(self.gui_color_1, 0.4)),
                      'color': [1, 1, 1, 1]}
            self._gui_id_tag = ColorLabel(
                text=self.id, size_hint=(None, None),
                width=250, height=50, font_size='18sp',
                valign='middle', halign='center', **params
            )
        return self._gui_id_tag

    def gui_id_show(self, duration=None):
        if not self.gui_id_tag.parent:
            self.gui_status_stack.add_widget(self.gui_id_tag)
        if duration:
            self.reactor.callLater(duration, self.gui_id_hide)

    def gui_id_hide(self):
        if self.gui_id_tag.parent:
            self.gui_status_stack.remove_widget(self.gui_id_tag)

    def gui_setup(self):
        super(NodeIDGuiMixin, self).gui_setup()
        if not self.config.node_id_display:
            return
        if self.config.node_id_display_frequency:
            self._gui_id_task = task.LoopingCall(
                self.gui_id_show,
                duration=self.config.node_id_display_duration
            )
            self._gui_id_task.start(self.config.node_id_display_frequency)
        else:
            self.gui_id_show(duration=self.config.node_id_display_duration)
