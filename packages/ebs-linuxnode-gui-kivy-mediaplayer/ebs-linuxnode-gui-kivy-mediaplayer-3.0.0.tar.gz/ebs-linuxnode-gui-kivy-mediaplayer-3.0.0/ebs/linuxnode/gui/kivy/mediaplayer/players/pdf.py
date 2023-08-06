

from kivy_garden.ebs.pdfplayer import PDFPlayer
from ebs.linuxnode.mediaplayer.base import MediaPlayerBase


class PdfPlayer(MediaPlayerBase):
    _extensions = ['.pdf']

    def _play(self, filepath, interval=None, bgcolor=(0, 0, 0, 1), loop=False):
        self._player = PDFPlayer(source=filepath,
                                 temp_dir=self.actual.temp_dir,
                                 loop=loop)
        if interval:
            self._player.interval = interval
        self._player.bind(on_done=lambda *_: self._actual.stop())
        return self._player

    def _stop(self):
        self._player.stop()

    def _pause(self):
        self._player.pause()

    def _resume(self):
        self._player.resume()
