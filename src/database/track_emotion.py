from database.database import Database
from database.storinator import Storinator


class TrackEmotion(Storinator):
    def __init__(self, host="localhost", port=27017,
                username=None, password=None):
        self._dbname = 'track_information'
        self._db = Database(host, port, username, password)

    def add(self, song_id, data):
        return self._db.insert(self._dbname, song_id,
            {
                {
                    "bpm": data['bpm']['value'],
                    "confidence": data['bpm']['confidence']
                },
                {
                    "timbre": data['timbre']['value'],
                    "confidence": data['timbre']['confidence']
                },
                {
                    "relaxed": data['relaxed']['value'],
                    "confidence": data['relaxed']['confidence']
                },
                {
                    "party": data['party']['value'],
                    "confidence": data['party']['confidence']
                },
                {
                    "aggressive": data['aggressive']['value'],
                    "confidence": data['aggressive']['confidence']
                },
                {
                    "happy": data['happy']['value'],
                    "confidence": data['happy']['confidence']
                },
                {
                    "sad": data['sad']['value'],
                    "confidence": data['sad']['confidence']
                }
            }
        )

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)
