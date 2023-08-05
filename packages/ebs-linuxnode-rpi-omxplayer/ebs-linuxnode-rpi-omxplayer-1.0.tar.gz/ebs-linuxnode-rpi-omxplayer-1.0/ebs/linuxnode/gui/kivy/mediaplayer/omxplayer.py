

from ebs.linuxnode.core.config import ElementSpec, ItemSpec
from ebs.linuxnode.gui.kivy.mediaplayer.mixin import MediaPlayerGuiMixin

from ebs.linuxnode.mediaplayer.manager import MAIN
from ebs.linuxnode.mediaplayer.manager import BACKGROUND

from .players.omxplayer import OMXPlayer


class OMXPlayerGuiMixin(MediaPlayerGuiMixin):
    def __init__(self, *args, **kwargs):
        super(OMXPlayerGuiMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(OMXPlayerGuiMixin, self).install()
        if not self.config.platform == 'rpi':
            return
        _elements = {
            'video_dispmanx_layer': ElementSpec('video-rpi', 'dispmanx_video_layer', ItemSpec(int, fallback=4)),
        }
        for name, spec in _elements.items():
            self.config.register_element(name, spec)

        mpm_main = self.media_player_manager(MAIN)
        mpm_main.install_player(OMXPlayer(MAIN, mpm_main), index=-1)
        mpm_bg = self.media_player_manager(BACKGROUND)
        mpm_bg.install_player(OMXPlayer(BACKGROUND, mpm_bg), index=-1)

    def gui_setup(self):
        gui = super(MediaPlayerGuiMixin, self).gui_setup()
        return gui
