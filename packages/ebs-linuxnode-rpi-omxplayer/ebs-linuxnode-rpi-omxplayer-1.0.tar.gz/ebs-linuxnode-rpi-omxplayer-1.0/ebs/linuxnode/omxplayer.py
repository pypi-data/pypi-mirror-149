

from twisted.internet import reactor
from pymediainfo import MediaInfo
from omxplayer.player import OMXPlayer
from dbus.exceptions import DBusException

_mediainfo_available = MediaInfo.can_parse()


class OMXPlayerController(object):
    def __init__(self, filepath, geometry, when_done,
                 layer=None, loop=False, dbus_name=None, orientation=0):
        self._player = None
        self._pposition = None
        self._pstate = None
        self._paused = False
        self._filepath = filepath
        self._cover = None
        self._loop = loop
        self._dbus_name = dbus_name
        self._geometry = geometry
        self._orientation = orientation
        self._when_done = when_done
        self._layer = layer
        self._launch_player()

    def _exit_handler(self, player, exit_state):
        if self._when_done and not self._paused:
            reactor.callFromThread(self._when_done)

    def _primary_rotation(self):
        mi = MediaInfo.parse(self._filepath)
        return int(float(mi.video_tracks[0].rotation))

    def _launch_player(self, paused=False):
        x, y, width, height = self._geometry

        args = [
            '--no-osd', '--aspect-mode', 'letterbox',
            '--layer', str(self._layer),
            '--win', '{0},{1},{2},{3}'.format(x, y, x + width, y + height),
            '--adev', 'hdmi',
        ]

        if _mediainfo_available:
            orientation = self._primary_rotation() - self._orientation
            if orientation < 0:
                orientation = 360 + orientation
            args.extend(['--orientation', '{}'.format(orientation)])

        if self._loop:
            args.append('--loop')

        try:
            # print("Launching player on {0} with {1}".format(self._dbus_name, self._filepath))
            self._player = OMXPlayer(self._filepath, args=args, dbus_name=self._dbus_name)
            if paused:
                self._player.pause()
            # print("Installing exit handler")
            self._player.exitEvent = self._exit_handler
        except SystemError as e:
            self._player = None
            self._exit_handler(None, 1)
        # print("Done launching player")

    def force_stop(self):
        if self._player:
            # print("Force stopping player")
            self._player.quit()
            self._player = None

    def pause(self):
        if self._player:
            # print("Pausing player")
            self._paused = True
            self._pposition = self._player.position()
            self._pstate = self._player.playback_status()
            self._player.quit()
            self._player = None
            # print("Done pausing")

    def resume(self):
        if self._player or not self._pstate:
            return
        # print("Resuming player")
        self._paused = False
        self._launch_player(paused=True)
        if self._pposition:
            self._player.set_position(self._pposition)
        if self._pstate == "Playing":
            self._player.play()
        self._pstate = None
        # print("Done resume")

    def set_geometry(self, x, y, width, height):
        self._geometry = (x, y, width, height)
        if self._player:
            try:
                self._player.set_video_pos(x, y, x + width, y + height)
            except DBusException:
                pass
