

import os
from kivy.core.text import FontContextManager
from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from .basemixin import BaseGuiMixin


class FontsGuiMixin(BaseGuiMixin):
    def __init__(self, *args, **kwargs):
        self._text_font_context = None
        super(FontsGuiMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(FontsGuiMixin, self).install()
        _elements = {
            'text_font_name': ElementSpec('text', 'font_name', ItemSpec('path', fallback=None)),
            'text_use_fcm': ElementSpec('text', 'use_fcm', ItemSpec(bool, fallback=False)),
            'text_fcm_system': ElementSpec('text', 'fcm_system', ItemSpec(bool, fallback=True)),
            'text_fcm_fonts': ElementSpec('text', 'fcm_fonts', ItemSpec('path', fallback=None)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

    @property
    def text_font_context(self):
        if not self._text_font_context and self.config.text_use_fcm:
            self._text_create_fcm()
        return self._text_font_context

    def _text_create_fcm(self):
        fc = self.appname
        if self.config.text_fcm_system:
            fc = "system://{0}".format(fc)
        self._text_font_context = fc
        self.log.info("Creating FontContextManager {0} using fonts in {1}"
                      .format(fc, self.config.text_fcm_fonts))
        FontContextManager.create(fc)

        for filename in os.listdir(self.config.text_fcm_fonts):
            self.log.info("Installing Font {0} to FCM {1}".format(filename, self._text_font_context))
            FontContextManager.add_font(fc, os.path.join(self.config.text_fcm_fonts, filename))

    @property
    def text_font_params(self):
        params = {}
        if self.text_font_context:
            params.update({
                'font_context': self._text_font_context
            })
        else:
            params.update({
                'font_name': self.config.text_font_name
            })
        return params
