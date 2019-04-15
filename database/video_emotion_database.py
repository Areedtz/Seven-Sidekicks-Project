import datetime
from pymongo import MongoClient


def _create_default_document(id, id2):
    return {
        "song_id": id,
        "video_id": id2,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(doc1, doc2):
    return {**doc1, **doc2}


class VEDatabase:
    def __init__(self, host="localhost", port=27017,
                 username=None, password=None):
        self._client = MongoClient(
            host, port, username=username, password=password)
        self._db = self._client['dr']

    def insert(self, name,
               song_id, video_id, doc):
        collection = self._db[name]
        ins = _augment_document(_create_default_document(song_id,
                                                         video_id), doc)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, name,
             song_id, video_id):
        return self._db[name].find({'song_id': song_id, 'video_id': video_id}
                                   ).sort([('last_updated', -1)]
                                          ).limit(1)[0]

    def find_all(self, name):
        results = []
        for track_bpm in self._db[name].find():
            results.append(track_bpm)
        return results

    def close(self):
        self._db.close()
