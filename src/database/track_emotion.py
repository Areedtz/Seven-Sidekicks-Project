from database.database import Database
from database.storinator import Storinator


class TrackEmotion(Storinator):
    def __init__(self):
        self._dbname = 'track_emotion'
        self._db = Database()

    def add(self, song_id, data):
        return self._db.insert(self._dbname, song_id, data)

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)
