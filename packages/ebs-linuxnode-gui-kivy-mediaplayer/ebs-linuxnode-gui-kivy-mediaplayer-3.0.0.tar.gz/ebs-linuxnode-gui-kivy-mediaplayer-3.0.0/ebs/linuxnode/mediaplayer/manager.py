

import os
import time
from twisted import logger
from twisted.internet.defer import Deferred

from .base import MediaPlayerBase


MAIN = 1
BACKGROUND = 2


class MediaPlayerBusy(Exception):
    def __init__(self, mpid, now_playing, collision_count):
        self.mpid = mpid
        self.now_playing = now_playing
        self.collision_count = collision_count

    def __repr__(self):
        return "<MediaPlayerBusy {0} Now Playing {1}" \
               "".format(self.mpid, self.now_playing)


class MediaPlayerManager(object):
    def __init__(self, actual, mpid):
        self._actual = actual
        self._mpid = mpid
        self._log = None
        self._players = []
        self._current_player = None
        self._deferred = None
        self._now_playing = None
        self._end_call = None
        self._collision_count = 0
        self._media_playing = None
        self._paused = False
        self._eresidual = None

    @property
    def mpid(self):
        return self._mpid

    @property
    def actual(self):
        if hasattr(self._actual, 'actual'):
            return self._actual.actual
        else:
            return self._actual

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="mpm.{0}".format(self.mpid),
                                      source=self)
        return self._log

    def install_player(self, player, index=0):
        self.log.info("Installing Media Player {} to Manager {}"
                      "".format(player.__class__, self.mpid))
        self._players.insert(index, player)

    def _install_builtin_players(self):
        pass

    def install(self):
        self._install_builtin_players()

    def check_supports(self, target):
        if not os.path.exists(target):
            return False
        for player in self._players:
            if player.check_support(target):
                return True
        return False

    def play(self, content, duration=None, **kwargs):
        # kwargs : loop=False, interval=None
        # Play the media file at filepath. If loop is true, restart the media
        # when it's done. You probably would want to provide a duration with
        # an image or with a looping video, not otherwise.
        if self._now_playing:
            self._collision_count += 1
            if self._collision_count > 30:
                self.stop(forced=True)
            raise MediaPlayerBusy(self.mpid,
                                  self._now_playing,
                                  self._collision_count)
        self._collision_count = 0
        if hasattr(content, 'filepath'):
            content = content.filepath
        if not os.path.exists(content):
            self.log.warn("Could not find media to play at {filepath}",
                          filepath=content)
            return
        if duration:
            self._end_call = self.actual.reactor.callLater(duration, self.stop)
        self._now_playing = os.path.basename(content)

        player: MediaPlayerBase
        for player in self._players:
            if player.check_support(content):
                self.log.info("Showing content '{filename}' using <{mpid} {player}>",
                              filename=os.path.basename(content), mpid=self.mpid,
                              player=player.__class__.__name__)
                self._current_player = player
                self._media_playing = player.play(content, **kwargs)
                break
        if not self._current_player:
            self.log.info("Have Players: {}".format(self._players))
            raise TypeError("Could not find a player to play media {}.".format(content))

        self._deferred = Deferred()
        return self._deferred

    def stop(self, forced=False):
        if not self._now_playing:
            return
        self.log.info("Stopping Media : {0}".format(self._now_playing))
        if self._collision_count:
            self.log.info("End Offset by {0} collisions."
                          "".format(self._collision_count))
        self._collision_count = 0

        assert isinstance(self._current_player, MediaPlayerBase)
        self._current_player.stop()
        self._current_player = None
        self._media_playing = None

        if self._end_call and self._end_call.active():
            self._end_call.cancel()

        self._eresidual = None

        if self._now_playing:
            self._now_playing = None

        if self._deferred:
            d = self._deferred
            self._deferred = None
            d.callback(forced)

    def pause(self):
        self.log.info("Pausing {} {}".format(self.__class__, self._media_playing))
        if self._paused:
            return
        if self._end_call and self._end_call.active():
            ietime = self._end_call.getTime()
            ptime = time.time()
            self._eresidual = ietime - ptime
            self._end_call.cancel()
        self._current_player.pause()
        self._paused = True

    def resume(self):
        self.log.info("Resuming {} {}".format(self.__class__, self._media_playing))
        if self._paused:
            self._current_player.resume()
            self._paused = False
            if self._eresidual:
                self._end_call = self.actual.reactor.callLater(self._eresidual, self.stop)
                self._eresidual = None
