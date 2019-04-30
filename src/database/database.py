import datetime

from pymongo import MongoClient

from utilities.config_loader import load_config


def _create_default_document(id):
    return {
        "song_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }


def _create_default_segment_document(id):
    return {
        "segment_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(doc1, doc2):
    return {**doc1, **doc2}


class Database:
    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client['dr']

    def insert(self, col, song_id, doc):
        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id), doc)
        _id = collection.insert_one(ins).inserted_id
        return _id

    # Gets the newest entry, the other option would be to overwrite it in the insert method
    def find(self, col, song_id):
        if (self._db[col].count({'song_id': song_id}) > 0):
            res = self._db[col].find({'song_id': song_id}
                                     ).sort([('last_updated', -1)]
                                            ).limit(1)
            return res[0]

        return None

    def find_all_with_id(self, name, song_id):
        results = []
        for res in self._db[name].find({'song_id': song_id}):
            results.append(res)
        return results

    def find_all(self, col):
        results = []
        for r in self._db[col].find():
            results.append(r)
        return results

    def close(self):
        self._client.close()
