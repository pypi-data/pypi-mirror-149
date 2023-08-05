

import os
from raspi_system import hwinfo

from ebs.linuxnode.core.config import ItemSpec
from ebs.linuxnode.core.config import ElementSpec


def _orientation(config):
    rv = 0
    if config.portrait is True:
        rv += 90
    if config.flip:
        rv += 180
    return rv


def prepare_config(appname):
    from ebs.linuxnode.core.config import IoTNodeConfig
    node_config = IoTNodeConfig(appname=appname)

    items = [
            ('platform', ElementSpec('platform', 'platform', ItemSpec(fallback='native'))),
            ('fullscreen', ElementSpec('display', 'fullscreen', ItemSpec(bool, fallback=True))),
            ('portrait', ElementSpec('display', 'portrait', ItemSpec(bool, fallback=False))),
            ('flip', ElementSpec('display', 'flip', ItemSpec(bool, fallback=False))),
            ('app_dispmanx_layer', ElementSpec('display-rpi', 'dispmanx_app_layer', ItemSpec(int, fallback=5))),
            ('orientation', ElementSpec('_derived', _orientation)),
            ('os_rotation', ElementSpec('display', 'os_rotation', ItemSpec(bool, fallback=False)))
    ]

    for name, spec in items:
        node_config.register_element(name, spec)
    return node_config


def prepare_environment(node_config):
    print("Using pango Text Provider")
    os.environ['KIVY_TEXT'] = 'pango'
    if node_config.platform == 'rpi':
        if hwinfo.is_pi4():
            print("Using sdl2 Window Provider")
            os.environ['KIVY_WINDOW'] = 'sdl2'
        else:
            print("Using egl_rpi Window Provider")
            os.environ['KIVY_WINDOW'] = 'egl_rpi'
        os.environ['KIVY_BCM_DISPMANX_LAYER'] = str(node_config.app_dispmanx_layer)
        print("Using app_dispmanx_layer {0}".format(node_config.app_dispmanx_layer))
    else:
        print("Using ffpyplayer Video Provider")
        os.environ['KIVY_VIDEO'] = 'ffpyplayer'


def prepare_kivy(node_config):
    from kivy.config import Config
    if node_config.fullscreen is True:
        Config.set('graphics', 'fullscreen', 'auto')

    if node_config.orientation:
        Config.set('graphics', 'rotation', node_config.orientation)

    Config.set('kivy', 'keyboard_mode', 'systemandmulti')
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

    from kivy.support import install_twisted_reactor
    install_twisted_reactor()
