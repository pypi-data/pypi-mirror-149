

import warnings
from ebs.linuxnode.core.basemixin import BaseMixin
from .manager import MAIN


class MediaPlayerCoreMixin(BaseMixin):
    def __init__(self, *args, **kwargs):
        super(MediaPlayerCoreMixin, self).__init__(*args, **kwargs)
        self._media_player_managers = {}

    def media_player_manager(self, mpid):
        if mpid not in self._media_player_managers.keys():
            raise AttributeError("MediaPlayerManager with MPID {} not found!"
                                 "".format(mpid))
        return self._media_player_managers[mpid]

    def install_media_player_manager(self, manager):
        self.log.info("Installing Media Player Manager {} with MPID {}"
                      "".format(manager, manager.mpid))
        self._media_player_managers[manager.mpid] = manager
        manager.install()

    def install(self):
        super(MediaPlayerCoreMixin, self).install()

    def media_play(self, *args, **kwargs):
        warnings.warn("Deprecated Access of Bare Node media_play(). "
                      "Use the appropriate media_player_manager instead.")
        return self.media_player_manager(MAIN).play(*args, **kwargs)

    def media_stop(self, *args, **kwargs):
        warnings.warn("Deprecated Access of Bare Node media_stop(). "
                      "Use the appropriate media_player_manager instead.")
        return self.media_player_manager(MAIN).stop(*args, **kwargs)

    def stop(self):
        for mpid, mpm in self._media_player_managers.items():
            mpm.stop(forced=True)
        super(MediaPlayerCoreMixin, self).stop()
