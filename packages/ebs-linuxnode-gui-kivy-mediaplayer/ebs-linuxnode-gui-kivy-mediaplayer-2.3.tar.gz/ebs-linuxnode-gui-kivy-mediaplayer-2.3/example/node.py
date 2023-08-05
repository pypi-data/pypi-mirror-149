

from twisted.internet import reactor
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.gui.kivy.mediaplayer.mixin import MediaPlayerGuiMixin
from kivy_garden.ebs.clocks.digital import SimpleDigitalClock
from ebs.linuxnode.gui.kivy.background.manager import BackgroundSpec

try:
    from ebs.linuxnode.gui.kivy.mediaplayer.omxplayer import OMXPlayerGuiMixin
    BaseNode = OMXPlayerGuiMixin
except ImportError:
    BaseNode = MediaPlayerGuiMixin


class ExampleNode(BaseNode, BaseIoTNodeGui):
    def _mediaplayer_example(self):
        reactor.callLater(10, self.mediaview.play, 'image.jpg', duration=10)
        reactor.callLater(50, self.mediaview.play, 'video-2.mp4')
        reactor.callLater(70, self.mediaview.play, 'pdf.pdf', duration=30)

    def _set_bg(self, target):
        self.gui_bg = target

    def _set_bg_sequence(self, targets):
        self.gui_bg_sequence = targets

    @property
    def clock(self):
        return SimpleDigitalClock()

    def _background_example(self):
        reactor.callLater(10, self._set_bg, '1.0:0.5:0.5:1.0')
        reactor.callLater(20, self._set_bg, 'image.jpg')
        reactor.callLater(30, self._set_bg, '0.5:1.0:0.5:1.0')
        reactor.callLater(40, self._set_bg, None)
        # Install kivy_garden.ebs.clocks
        # reactor.callLater(50, self._set_bg, 'structured:clock')
        reactor.callLater(50, self._set_bg, 'video-2.mp4')
        reactor.callLater(60, self._set_bg, BackgroundSpec('video-2.mp4', callback=lambda _: self._set_bg('video.mp4')))
        reactor.callLater(70, self._set_bg, 'pdf.pdf')

    def _background_series_example(self):
        bgseries = [
            BackgroundSpec('1.0:0.5:0.5:1.0', duration=30),
            BackgroundSpec('image.jpg', duration=10),
            'video.mp4',
            'pdf.pdf',
            BackgroundSpec(None, duration=10),
        ]
        reactor.callLater(5, self._set_bg_sequence, bgseries)

    def start(self):
        super(ExampleNode, self).start()
        self._background_series_example()
        self._mediaplayer_example()
