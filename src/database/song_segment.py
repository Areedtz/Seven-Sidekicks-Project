from database.database import Database
from database.storinator import Storinator


class SongSegment(Storinator):
    def __init__(self, host="localhost", port=27017,
                 username=None, password=None):
        self._dbname = 'song_segmentation'
        self._db = Database(host, port, username, password)

    def add(self, song_id, time_from, time_to, mfcc, chroma, tempogram):
        return self._db.insert(self._dbname, song_id, {
            "time_from": time_from,
            "time_to": time_to,
            "mfcc": mfcc,
            "chroma": chroma,
            "tempogram": tempogram,
        })

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_all_with_id(self, song_id):
        return self._db.find_all_with_id(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)

    def close(self):
        self._db.close()
