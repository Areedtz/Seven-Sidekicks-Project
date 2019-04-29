from database.storinator import Storinator
from database.video_emotion_database_no_song import VEDatabase

# VideoEmotionNS = video emotions no song
class VideoEmotionNS(Storinator):
    def __init__(self):
        self._dbname = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self,
            video_id, time, emotions):
        return self._db.insert(self._dbname, video_id, time, emotions)

    def get(self, video_id):
        return self._db.find(self._dbname, video_id)

    def get_all_same_id(self, video_id):
        return self._db.find_all_same_id(self._dbname, video_id)

    def get_all(self):
        return self._db.find_all(self._dbname)
