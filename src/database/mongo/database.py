import datetime
from typing import Dict

from pymongo import MongoClient

from utilities.config_loader import load_config


def _create_default_document(id: str) -> Dict:
    """Creates a MongoDB document with song_id and a timestamp

    Parameters
    ----------
    id : str
        id of the song to be created

    Returns
    -------
    Dict
        Containing id and timestamp
    """

    return {
        "song_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }


def _create_default_segment_document(id: str) -> Dict:
    """Creates a MongoDB document with segment_id and a timestamp

    Parameters
    ----------
    id : str
        id of the entity to be created

    Returns
    -------
    Dict
        Containing id and timestamp
    """

    return {
        "segment_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(doc1: dict, doc2: dict) -> Dict:
    """Combines the given dictionaries into a single dictionary

    Parameters
    ----------
    doc1 : dict
        First dictionary
    doc2 : dict
        Second dictionary

    Returns
    -------
    Dict
        The combined dictionaries
    """

    return {**doc1, **doc2}


class Database:
    """
    A class used to communicate with a MongoDB database

    Methods
    -------
    insert(col, song_id, doc)
        Inserts data into the given collection in the database

    find(col, song_id)
        Finds the newest document with the given id in the given collection

    find_all_by_id(col, song_id)
        Finds all documents with the given id in the given collection

    find_all(col)
        Finds all documents in the given collection

    close()
        Closes the connection to the database
    """

    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'],
            authSource=cfg['mongo_db'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col: str, song_id: str, doc: dict) -> str:
        """Inserts data into the given collection in the database

        Parameters
        ----------
        col : str
            The collection to add data to
        song_id : str
            id of the song
        doc : dict
            Dictionary with data

        Returns
        -------
        str
            The document's object id
        """

        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id), doc)

        _id = collection.update_one({'song_id': song_id}, {'$set': ins},
                                    upsert=True).upserted_id

        return _id

    def find(self, col: str, song_id: str) -> object:
        """Finds the newest document with the given id in the given collection

        Parameters
        ----------
        col : str
            The collection to look in
        song_id : str
            id of the song

        Returns
        -------
        object
            None if nothing was found, otherwise the document
        """

        if (self._db[col].count({'song_id': song_id}) > 0):
            res = self._db[col].find({'song_id': song_id}
                                     ).sort([('last_updated', -1)]
                                            ).limit(1)
            return res[0]

        return None

    def find_all_by_id(self, col: str, song_id: str) -> [object]:
        """Finds all documents with the given id in the given collection

        Parameters
        ----------
        col : str
            The collection to look in
        song_id : str
            id of the song

        Returns
        -------
        object list
            A list of the objects in the database with the given song id
        """

        results = []
        for res in self._db[col].find({'song_id': song_id}):
            results.append(res)

        return results

    def find_all(self, col: str) -> [object]:
        """Finds all documents in the given collection

        Parameters
        ----------
        col : str
            The collection to look in

        Returns
        -------
        object list
            A list of the objects in the collection
        """

        results = []
        for r in self._db[col].find():
            results.append(r)

        return results

    def close(self):
        """Closes the connection to the database"""

        self._client.close()
