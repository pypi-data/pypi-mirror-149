

from kivy_garden.ebs.core.image import BleedImage
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class ImagePlayer(MediaPlayerBase):
    _extensions = ['.png', '.jpg', '.bmp', '.gif', '.jpeg']

    def _play(self, filepath, bgcolor=(0, 0, 0, 1), loop=True):
        self._player = BleedImage(source=filepath,
                                  allow_stretch=True,
                                  keep_ratio=True,
                                  bgcolor=bgcolor)
        return self._player

    def _stop(self):
        pass

    def _pause(self):
        pass

    def _resume(self):
        pass
