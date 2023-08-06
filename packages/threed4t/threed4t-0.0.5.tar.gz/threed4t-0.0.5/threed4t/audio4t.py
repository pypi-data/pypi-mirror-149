from ursina import *

from . import common



class 載入聲音(Audio):
    def __init__(self, *args,重複播放=False,自動播放=False,**kwargs):
        kwargs['loop'] = 重複播放
        kwargs['autoplay'] = 自動播放
        super().__init__(*args, **kwargs)


    def 播放(self):
        self.play()

    def 暫停(self):
        self.pause()

    def 繼續(self):
        self.resume()

    def 停止(self):
        self.stop()

    @property
    def 播放中嗎(self):
        return self.playing
