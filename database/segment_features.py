from database.database import Database
from database.storinator import SegmentStorinator


class SegmentFeatures(SegmentStorinator):
    def __init__(self, host="localhost", port=27017,
                 username=None, password=None):
        self._dbname = 'segment_features'
        self._db = Database(host, port, username, password)

    def add(self, segment_id, mfcc, chroma, tempogram):
        return self._db.insert(self._dbname, segment_id, {
            "mfcc": mfcc,
            "chroma": chroma,
            "tempogram": tempogram,
        })

    def get(self, segment_id):
        return self._db.find(self._dbname, segment_id)

    def get_all(self):
        return self._db.find_all(self._dbname)

    def close(self):
        self._db.close()
