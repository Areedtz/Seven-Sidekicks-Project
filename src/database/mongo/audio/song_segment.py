from database.mongo.database import Database
from database.mongo.storinator import Storinator


class SongSegment(Storinator):
    """
    An extension to the database class that calls its methods with other
    parameters to lessen code

    Methods
    -------
    add(song_id, time_from, time_to)
        Insert song segment into the song_segmentation collection

    get(song_id)
        Gets the newest document with the given song id in the
        song_segmentation collection

    get_by_ids(ids)
        Gets all song segments from the song_segmentation
        collection by document object ids

    get_all_by_song_id(song_id)
        Gets all song segments from the song_segmentation collection by song id

    get_all()
        Gets all song_segments from the database

    get_all_in_range(from_count, to_count)
        Get all documents in the song_segmentation collection
        in the given time range

    update_similar(id, similar)
        Updates a document in the song_segmentation collection

    count()
        Counts the number of documents in the song_segmentation collection

    close()
        Closes the connection to the database
    """

    def __init__(self):
        self._dbcol = 'song_segmentation'
        self._db = Database()

    def add(self, song_id: str, time_from: int, time_to: int,
            mfcc, chroma, tempogram, similar) -> str:
        """Insert song segment into the song_segmentation collection

        Parameters
        ----------
        song_id : str
            The id of the song
        time_from : int
            The start of the time interval
        time_to : int
            The end of the time interval
        mfcc

        chroma

        tempogram

        similar

        Returns
        -------
        str
            The document's object id
        """

        return self._db.insert(self._dbcol, song_id, {
            "time_from": time_from,
            "time_to": time_to,
            "mfcc": mfcc,
            "chroma": chroma,
            "tempogram": tempogram,
            "similar": similar,
        })

    def get(self, song_id: str):
        """Gets the newest document with the given song id
        in the song_segmentation collection

        Parameters
        ----------
        song_id : str
            The id of the song

        Returns
        -------
        object
            Either a None object or the object from the database
        """

        return self._db.find(self._dbcol, song_id)

    def get_by_ids(self, ids: [str]):
        """Gets all song segments from the song_segmentation
        collection by document object ids

        Parameters
        ----------
        ids : [str]
            List of document object ids

        Returns
        -------
        object list
            a list of the objects in the database from id
        """

        results = []
        for r in self._db._db[self._dbcol].find({'_id': {'$in': ids}}):
            results.append(r)

        return results

    def get_all_by_song_id(self, song_id: str):
        """Gets all song segments from the song_segmentation collection by song id

        Parameters
        ----------
        song_id : str
            The id of the song

        Returns
        -------
        object list
            A list of the objects in the database from a given video_id
        """

        return self._db.find_all_by_id(self._dbcol, song_id)

    def get_all(self):
        """Gets all song_segments from the database

        Returns
        -------
        object list
            A list of the objects in the database
        """

        return self._db.find_all(self._dbcol)

    def get_all_in_range(self, from_count: int, to_count: int):
        """Get all documents in the song_segmentation
        collection in the given time range

        Parameters
        ----------
        from_count : int

        to_count : int


        Returns
        -------
        object list
            A list of the objects from the given interval
        """

        results = []
        for r in self._db._db[
                self._dbcol
            ].find().limit(
                to_count - from_count
                          ).skip(from_count):
            results.append(r)

        return results

    def update_similar(self, id: str, similar: []):
        """Updates a document in the song_segmentation collection

        Parameters
        ----------
        id : str
            Id of the entity
        similar : []
            Array of similar song segments
        """

        self._db._db[self._dbcol].update_one({'_id': id}, {
            '$set': {
                "similar": similar
            }
        })

    def count(self) -> int:
        """Counts the number of documents in the song_segmentation collection

        Returns
        -------
        int
            The number of documents in the collection
        """

        return self._db._db[self._dbcol].count({})

    def close(self):
        """Closes the connection to the database"""

        self._db.close()
