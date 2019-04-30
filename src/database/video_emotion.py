from database.storinator import Storinator
from database.video_emotion_database import VEDatabase


class VideoEmotion(Storinator):
    def __init__(self):
        self._col = 'video_emotion'
        self._db = VEDatabase()

    def add(self, song_id,
            video_id, emotions):
        return self._db.insert(self._col, song_id, video_id, emotions)

    def get(self, song_id, video_id):
        return self._db.find(self._col, song_id, video_id)

    def get_all(self):
        return self._db.find_all(self._col)

    def close(self):
        self._db.close()
