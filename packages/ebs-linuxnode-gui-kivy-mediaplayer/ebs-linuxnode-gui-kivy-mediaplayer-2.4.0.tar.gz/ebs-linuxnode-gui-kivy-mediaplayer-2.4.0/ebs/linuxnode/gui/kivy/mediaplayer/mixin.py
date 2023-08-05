

from kivy_garden.ebs.core.colors import ColorBoxLayout
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.mediaplayer.mixin import MediaPlayerCoreMixin

from ebs.linuxnode.gui.kivy.mediaplayer.manager import KivyMediaPlayerManager
from ebs.linuxnode.mediaplayer.manager import MAIN

from ebs.linuxnode.gui.kivy.background.mediaplayer import MediaPlayerBackgroundProvider


class MediaPlayerGuiMixin(MediaPlayerCoreMixin, BaseIoTNodeGui):
    def __init__(self, *args, **kwargs):
        super(MediaPlayerGuiMixin, self).__init__(*args, **kwargs)
        self._gui_mediaview = None

    def install(self):
        super(MediaPlayerGuiMixin, self).install()
        self.install_background_provider(MediaPlayerBackgroundProvider(self))
        self.install_media_player_manager(
            KivyMediaPlayerManager(self, MAIN, self.gui_mediaview,
                                   on_play=self.gui_bg_pause,
                                   on_stop=self.gui_bg_resume)
        )

    @property
    def mediaview(self):
        return self.media_player_manager(MAIN)

    @property
    def gui_mediaview(self):
        if self._gui_mediaview is None:
            self._gui_mediaview = ColorBoxLayout(bgcolor=(0, 0, 0, 0))
            self.gui_main_content.add_widget(self._gui_mediaview)
        return self._gui_mediaview

    def gui_setup(self):
        gui = super(MediaPlayerGuiMixin, self).gui_setup()
        _ = self.gui_mediaview
        return gui
