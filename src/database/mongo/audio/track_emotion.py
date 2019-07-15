from typing import Dict

from database.mongo.database import Database
from database.mongo.storinator import Storinator


class TrackEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    add(song_id, data)
        Insert document into the track_emotion collection

    get(song_id)
        Gets the newest document with the given id in the track_emotion collection

    get_all()
        Gets all documents from the track_emotion collection

    close()
        Closes the connection to the database
    """

    def __init__(self):
        self._col = 'track_emotion'
        self._db = Database()

    def add(self, song_id: str, data: dict) -> str:
        """Insert document into the track_emotion collection

        Parameters
        ----------
        song_id : str
            The id of the song
        data : dict
            The data of the entity

        Returns
        -------
        str
            The created document's object id
        """

        return self._db.insert(self._col, song_id, data)

    def get(self, song_id: str) -> object:
        """Gets the newest document with the given id in the track_emotion collection

        Parameters
        ----------
        song_id : str
            The id of the song

        Returns
        -------
        object
            Either a None object or the object from the database
        """

        return self._db.find(self._col, song_id)

    def get_all(self) -> [object]:
        """Gets all documents from the track_emotion collection

        Returns
        -------
        object list
            A list of the objects in the track_emotion collection
        """

        return self._db.find_all(self._col)

    def close(self):
        """Closes the connection to the database"""

        self._db.close()
