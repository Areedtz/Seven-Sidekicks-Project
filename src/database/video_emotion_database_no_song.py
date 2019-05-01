import datetime

from pymongo import MongoClient

from utilities.config_loader import load_config


def _create_default_document(id):
    return {
        "video_id": id,
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

    def insert(self, name,
               video_id, time, emotion):
        collection = self._db[name]
        ins = _augment_document(_create_default_document(
<<<<<<< HEAD
                                                         video_id), time, emotion)
=======
            video_id), doc)
>>>>>>> 6ca04e4f0eb42f285b2595e67ae400cdd8a5cf8a
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, name,
             video_id):
        return self._db[name].find({'video_id': video_id}
                                   ).sort([('last_updated', -1)]
                                          ).limit(1)[0]

    def find_all_same_id(self, name, video_id):
        results = []
        data =  self._db[name].find({'video_id': video_id})
        for i in data:
            del i['_id']
            i['last_updated'] = i['last_updated'].isoformat()
            results.append(i)
        return results
            

    def find_all(self, name):
        results = []
        for track_bpm in self._db[name].find():
            results.append(track_bpm)
        return results
