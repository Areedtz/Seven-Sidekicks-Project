import datetime
from typing import Dict

from pymongo import MongoClient

from utilities.config_loader import load_config


def _create_default_document(song_id: str, video_id: str) -> Dict:
    """Creates a document with a song id, video id and a timestamp

    Parameters
    ----------
    song_id : str
        song id of the document to be created
    video_id : str
        video id of the document to be created

    Returns
    -------
    Dict
        Containing song id, video id and a timestamp
    """

    return {
        "song_id": song_id,
        "video_id": video_id,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(id: str, time: dict, emotion: dict) -> Dict:
    """Combines parameters into a larger dictionary

    Parameters
    ----------
    id : str
        id of the entity
    time : dict
        dictionary of time interval
    emotion : dict
        dictionary of emotion data

    Returns
    -------
    Dict
        Dictionary combining id, time interval and emotion data
    """

    return {**id, **time, **emotion}


# Generic class for making functions implementable
# for lower level classes of music analysis
class VEDatabase:
    """
    A class used to communicate with a MongoDB database

    Methods
    -------
    insert(col, song_id, video_id, time, emotion)
        Insert video segment into the given collection

    find(col, song_id, video_id)
        Finds documents in the given collection by song id and video id

    find_by_song_id(col, song_id)
        Finds documents in the given collection by song id

    find_all(col)
        Finds all documents in the given collection

    close()
        Closes the connection to the database
    """

    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col: str, song_id: str,
               video_id: str, time: dict, emotion: dict) -> str:
        """Insert video segment into the given collection

        Parameters
        ----------
        col : str
            The collection to be added to
        song_id : str
            id of the song
        video_id : str
            id of the video
        time : dict
            Dictionary with time interval
        emotion : dict
            Dictionary with emotion data

        Returns
        -------
        str
            The created document's object id
        """

        collection = self._db[col]

        ins = _augment_document(
            _create_default_document(song_id, video_id),
            time, emotion)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col: str, song_id: str, video_id: str) -> object:
        """Finds documents in the given collection by song id and video id

        Parameters
        ----------
        col : str
            The collection to look in
        song_id : str
            id of the song
        video_id : str
            id of the video

        Returns
        -------
        object
            None if nothing was found, otherwise the document
        """

        return self._db[col].find({'song_id': song_id, 'video_id': video_id}
                                  ).sort([('last_updated', -1)]
                                         ).limit(1)[0]

    def find_by_song_id(self, col: str, song_id: str) -> [object]:
        """Finds documents in the given collection by song id

        Parameters
        ----------
        col : str
            The collection to look in
        song_id : str
            id of the song

        Returns
        -------
        object list
            A list of the objects in the collection
        """

        results = []
        data = self._db[col].find({'song_id': song_id})
        for i in data:
            del i['_id']
            i['last_updated'] = i['last_updated'].isoformat()
            results.append(i)
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
