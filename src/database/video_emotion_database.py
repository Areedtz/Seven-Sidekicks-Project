import datetime

from pymongo import MongoClient

from utilities.config_loader import load_config


def _create_default_document(id, id2):
    return {
        "song_id": id,
        "video_id": id2,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(id1, time, emotion):
    return {**id1, **time, **emotion}


class VEDatabase:
    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col,
               song_id, video_id, time, emotion):
        collection = self._db[col]

        ins = _augment_document(_create_default_document(song_id,
                                                         video_id), time, emotion)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col,
             song_id, video_id):
        return self._db[col].find({'song_id': song_id, 'video_id': video_id}
                                  ).sort([('last_updated', -1)]
                                         ).limit(1)[0]

    def find_by_song_id(self, col, song_id):
        results = []
        data =  self._db[col].find({'song_id': song_id})
        for i in data:
            del i['_id']
            i['last_updated'] = i['last_updated'].isoformat()
            results.append(i)
        return results

    def find_all(self, col):
        results = []
        for r in self._db[col].find():
            results.append(r)

        return results

    def close(self):
        self._db.close()
