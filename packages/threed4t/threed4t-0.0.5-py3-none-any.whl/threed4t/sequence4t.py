from ursina import *

from . import common



class  動畫組合(Sequence):
    def __init__(self, *args,重複播放=False,自動移除=False,**kwargs):
        kwargs['loop'] = 重複播放
        kwargs['auto_destroy'] = 自動移除
        super().__init__(*args, **kwargs)


    def 開始(self):
        self.start()

    def 暫停(self):
        self.pause()

    def 繼續(self):
        self.resume()

    def 結束(self):
        self.finish()

    def 移除(self):
        self.kill()

    @property
    def 結束了嗎(self):
        return self.finished

    @property
    def 暫停了嗎(self):
        return self.paused

 