import pykka
from database.song_segment import SongSegment


class Loader(pykka.ThreadingActor):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.seg_db = SongSegment()

    def on_receive(self, message):
        return
