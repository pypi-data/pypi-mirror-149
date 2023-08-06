

from ebs.linuxnode.mediaplayer.manager import MediaPlayerManager

from .players.video import VideoPlayer
from .players.image import ImagePlayer
from .players.pdf import PdfPlayer


class KivyMediaPlayerManager(MediaPlayerManager):
    def __init__(self, actual, mpid, target_container, on_play=None, on_stop=None):
        self._target_container = target_container
        self._on_play = on_play
        self._on_stop = on_stop
        super(KivyMediaPlayerManager, self).__init__(actual, mpid)

    @property
    def target_container(self):
        return self._target_container

    def _install_builtin_players(self):
        super(KivyMediaPlayerManager, self)._install_builtin_players()
        self.install_player(VideoPlayer(self))
        self.install_player(PdfPlayer(self))
        self.install_player(ImagePlayer(self))

    def play(self, content, duration=None, **kwargs):
        deferred = super(KivyMediaPlayerManager, self).play(content, duration=duration, **kwargs)
        if self._current_player.is_visual:
            if self._on_play:
                self._on_play()
                self._target_container.make_opaque()
            self._target_container.add_widget(self._media_playing)
        return deferred

    def stop(self, forced=False):
        if self._current_player:
            is_visual = self._current_player.is_visual
        else:
            is_visual = False
        if is_visual:
            self._target_container.clear_widgets()
        super(KivyMediaPlayerManager, self).stop(forced=forced)

        def _resume_bg():
            if not self._now_playing:
                if self._on_stop:
                    self._on_stop()
                    self._target_container.make_transparent()
        if is_visual:
            self.actual.reactor.callLater(1, _resume_bg)
