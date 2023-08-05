

from kivy.uix.video import Video
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class VideoPlayer(MediaPlayerBase):
    _extensions = ['*']

    def _play(self, filepath, loop=False, bgcolor=(0, 0, 0, 1)):
        if loop:
            eos = 'loop'
        else:
            eos = 'stop'

        self._player = Video(source=filepath, state='play',
                             eos=eos, allow_stretch=True)
        self._player.opacity = 0

        def _while_playing(*_):
            self._player.opacity = 1
        self._player.bind(texture=_while_playing)
        self._player.bind(eos=self._eos_handler)
        self._disarm_eos_ignore()
        return self._player

    def _eos_handler(self, *_):
        if self._ignore_eos_once_pause:
            self._disarm_eos_ignore()
            return
        self._actual.stop()

    def _arm_eos_ignore(self):
        self._ignore_eos_once_pause = True

    def _disarm_eos_ignore(self):
        self._ignore_eos_once_pause = False

    def _stop(self):
        if self._player:
            self._player.state = 'stop'
            self._player.unload()
            self._player = None

    def _pause(self):
        if self._player:
            if self._player.duration - self._player.position > 2:
                self._arm_eos_ignore()
            self._player.state = 'pause'

    def _resume(self):
        if self._player:
            self.actual.reactor.callLater(1, self._disarm_eos_ignore)
            self._player.state = 'play'
