from database.storinator import Storinator
from database.video_emotion_database_no_song import VEDatabase

# VideoEmotionNS = video emotions no song
class VideoEmotionNS(Storinator):
    def __init__(self):
        self._dbcol = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self,
            video_id, time, emotions):
        return self._db.insert(self._dbcol, video_id, time, emotions)

    def get(self, video_id):
        return self._db.find(self._dbcol, video_id)

    def get_by_video_id(self, video_id):
        return self._db.find_by_video_id(self._dbcol, video_id)

    def get_all(self):
        return self._db.find_all(self._dbcol)
