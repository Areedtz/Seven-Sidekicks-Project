from database.database import Database
from database.storinator import Storinator


class SSegmentation(Storinator):
    def __init__(self):
        self._dbname = 'song_segmentation'
        self._db = Database()

    def add(self, song_id, time_from, time_to):
        return self._db.insert(self._dbname, song_id, {
            "time_from": time_from,
            "time_to": time_to
        })

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)
