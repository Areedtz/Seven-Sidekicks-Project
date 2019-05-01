import datetime

from pymongo import MongoClient

from utilities.config_loader import load_config


# Mandatory for all entities
# Gives entity an id and a timestamp
def _create_default_document(id):
    return {
        "song_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }
 

# Combines parameters into a larger dictionary
def _augment_document(doc1, doc2):
    return {**doc1, **doc2}


# Generic class for making functions implementable
# for lower level classes of music analysis
class Database:

    # Creates the individual collection in the database
    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client['dr']

    # Insert data into the collection
    def insert(self, col, song_id, doc):
        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id), doc)
        id = collection.insert_one(ins).inserted_id
        return id

    # Find one instance of the data requested
    def find(self, col, song_id):
        if (self._db[col].count({'song_id': song_id}) > 0):
            res = self._db[col].find({'song_id': song_id}
                                      ).sort([('last_updated', -1)]
                                             ).limit(1)
            return res[0]

        return None

    # Find all instances of the data requested in the collection
    def find_all(self, col):
        results = []
        for r in self._db[col].find():
            results.append(r)
        return results
