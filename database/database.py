from pymongo import MongoClient
import datetime


def _create_default_document(id):
    return {
        "song_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(doc1, doc2):
    return {**doc1, **doc2}


class Database:
    def __init__(self, host="localhost", port=27017):
        self._client = MongoClient(host, port)
        self._db = self._client['dr']

    def _insert(self, name, song_id, doc):
        collection = self._db[name]
        ins = _augment_document(_create_default_document(song_id), doc)
        id = collection.insert_one(ins).inserted_id
        return id

    def add_track_BPM(self, song_id, bpm, confidence):
        return self._insert('track_bpm', song_id, {
            "bpm": bpm,
            "confidence": confidence
        })

    def get_track_BPMs(self):
        track_bpms = []
        for track_bpm in self._db['track_bpm'].find():
            track_bpms.append(track_bpm)
        return track_bpms

    def get_track_BPM(self, song_id):
        return self._db['track_bpm'].find_one({'song_id': song_id})
