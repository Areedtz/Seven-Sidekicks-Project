from database.database import Database
from database.storinator import Storinator


class TrackParty(Storinator):
    def __init__(self):
        self._dbname = 'track_party'
        self._db = Database()

    def add(self, song_id, party, confidence):
        return self._db.insert(self._dbname, song_id, {
            "party": party,
            "confidence": confidence
        })

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)
