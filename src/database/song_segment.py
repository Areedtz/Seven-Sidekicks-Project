from database.database import Database
from database.storinator import Storinator


class SongSegment(Storinator):
    def __init__(self):
        self._dbname = 'song_segmentation'
        self._db = Database()

    def add(self, song_id, time_from, time_to, mfcc, chroma, tempogram, similar):
        return self._db.insert(self._dbname, song_id, {
            "time_from": time_from,
            "time_to": time_to,
            "mfcc": mfcc,
            "chroma": chroma,
            "tempogram": tempogram,
            "similar": similar,
        })

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_with_ids(self, song_ids):
        results = []
        for r in self._db._db[self._dbname].find({'_id': {'$in': song_ids}}):
            results.append(r)
        return results

    def get_all_with_id(self, song_id):
        return self._db.find_all_with_id(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)

    def get_all_in_range(self, from_count, to_count):
        results = []
        for r in self._db._db[self._dbname].find().limit(to_count - from_count).skip(from_count):
            results.append(r)
        return results

    def update_similar(self, id, similar):
        self._db._db[self._dbname].update_one({'_id': id}, {
            '$set': {
                "similar": similar
            }
        })

    def count(self):
        return self._db._db[self._dbname].count({})

    def close(self):
        self._db.close()