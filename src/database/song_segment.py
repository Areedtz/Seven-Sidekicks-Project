import typing


from database.database import Database
from database.storinator import Storinator


class SongSegment(Storinator):

    def __init__(self):

        self._dbcol = 'song_segmentation'
        self._db = Database()

    def add(self, song_id, time_from, time_to, mfcc, chroma, tempogram, similar):
        """adds entity to database

        Parameters
        ----------
        song_id: int
            the id of the song
        time_from
            the start of the time interval
        time_to
            the end of the time interval

        Returns
        -------
        the insert method from the database class with inputs
        """

        return self._db.insert(self._dbcol, song_id, {
            "time_from": time_from,
            "time_to": time_to,
            "mfcc": mfcc,
            "chroma": chroma,
            "tempogram": tempogram,
            "similar": similar,
        })

    def get(self, song_id):
        """Insert data into the collection

        Parameters
        ----------
        song_id
            the id of the song

        Returns
        -------
        Object
            either a None Object or the Object from the database
        """
        return self._db.find(self._dbcol, song_id)

    def get_by_ids(self, ids):
        """gets all entities in the database given by ids.

        Parameters
        ----------
        ids

        Returns
        -------
        Object list
            a list of the Objects in the database from id
        """

        results = []
        for r in self._db._db[self._dbcol].find({'_id': {'$in': ids}}):
            results.append(r)
        return results

    def get_all_by_song_id(self, song_id):
        """gets all entities from the database by song_id

        Parameters
        ----------
        song_id
            the id of the song

        Returns
        -------
        Object list
            a list of the Objects in the database from a given video_id
        """

        return self._db.find_all_by_id(self._dbcol, song_id)

    def get_all(self):
        """gets all entities from the database

        Returns
        -------
        Object list
            a list of the Objects in the database
        """

        return self._db.find_all(self._dbcol)

    def get_all_in_range(self, from_count, to_count):
        """updates an entity in the database given an id

        Parameters
        ----------

        from_count
            ???
        to_count
            ???

        Returns
        -------
        Object list
            a list of the Objects from the given interval???
        """

        results = []
        for r in self._db._db[self._dbcol].find().limit(to_count - from_count).skip(from_count):
            results.append(r)
        return results

    def update_similar(self, id, similar):
        """updates an entity in the database given an id

        Parameters
        ----------
        id
            id of the entity
        similar
            ???

        Returns
        -------
        Object list
            a list of the Objects in the database
        """
        self._db._db[self._dbcol].update_one({'_id': id}, {
            '$set': {
                "similar": similar
            }
        })

    def count(self) -> int:
        """counts the number of elements in the database

        Returns
        -------
        int
            the number of entities in the database
        """

        return self._db._db[self._dbcol].count({})

    def close(self):
        """Closes the conenction to the database"""

        self._db.close()
