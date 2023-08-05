

from kivy.uix.boxlayout import BoxLayout
from ebs.linuxnode.omxplayer import OMXPlayerController
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class OMXPlayer(MediaPlayerBase):
    _extensions = ['*']

    def __init__(self, idx, *args, **kwargs):
        super(OMXPlayer, self).__init__(*args, **kwargs)
        self._idx = idx

    def _play(self, filepath, loop=False, bgcolor=(0, 0, 0, 1)):
        geometry = self.actual.geometry_transform(
            self._actual.target_container.x, self._actual.target_container.y,
            self._actual.target_container.width, self._actual.target_container.height,
        )
        self._player = OMXPlayerController(
            filepath, geometry, self._actual.stop, loop=loop,
            layer=self.actual.config.video_dispmanx_layer,
            orientation=self.actual.config.orientation,
            dbus_name='org.mpris.MediaPlayer2.omxplayer{}'.format(self._idx)
        )
        self._player_proxy = BoxLayout()

        def _update_geometry(widget, _):
            new_geometry = self.actual.geometry_transform(
                widget.x, widget.y, widget.width, widget.height
            )
            self._player.set_geometry(*new_geometry)

        self._player_proxy.bind(size=_update_geometry,
                                pos=_update_geometry)

        return self._player_proxy

    def _stop(self):
        if self._player:
            self._player.force_stop()
        self._player = None
        self._player_proxy = None

    def _pause(self):
        self._player.pause()

    def _resume(self):
        self._player.resume()
