from database.video_emotion_database import VEDatabase
from database.storinator import Storinator


class VideoEmotion(Storinator):
    def __init__(self, host="localhost", port=27017, 
                 username=None, password=None):
        self._dbname = 'video_emotion'
        self._db = VEDatabase(host, port, username, password)

    def add(self, song_id, 
            video_id, emotions):
        return self._db.insert(self._dbname, song_id, video_id, emotions)

    def get(self, song_id, video_id):
        return self._db.find(self._dbname, song_id, video_id)

    def get_all(self):
        return self._db.find_all(self._dbname)
