import datetime

from pymongo import MongoClient

from utilities.config_loader import load_config


# Mandatory for all entities
# Gives entity an id and a timestamp
def _create_default_document(id, id2):
    return {
        "song_id": id,
        "video_id": id2,
        "last_updated": datetime.datetime.utcnow(),
    }


# Combines parameters into a larger dictionary
def _augment_document(vme_id, bpm, timbre,
                      party, relaxed, emotions):
    return {**vme_id, **bpm, **timbre, **party, **relaxed, **emotions}


# Generic class for making functions implementable
# for lower level classes of music analysis
class VMEDatabase:
    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    # Insert data into the collection
    def insert(self, col, song_id, video_id,
               bpm, timbre, party, relaxed, emotions):
        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id, video_id),
                                bpm, timbre, party, relaxed, emotions)
        id = collection.insert_one(ins).inserted_id
        return id

    # Find one instance of the data requested
    def find(self, col,
             song_id, video_id):
        return self._db[col].find({'song_id': song_id, 'video_id': video_id}
                                  ).sort([('last_updated', -1)]
                                         ).limit(1)[0]

    # Find all instances of the data requested in the collection
    def find_all(self, col):
        results = []
        for r in self._db[col].find():
            results.append(r)
        return results
