from typing import Dict, Object, List

from database.database import Database
from database.storinator import Storinator


class TrackEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    add(song_id, data)
        Inserts data into the collection in the database

    get(song_id)
        Finds one entity given an id

    get_all()
        Finds all entities in the database
    
    """

    def __init__(self):

        self._col = 'track_emotion'
        self._db = Database()

    def add(self, song_id: int, data: dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        song_id: int
            The id of the song
        data: dict
            The data of the entity
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._col, song_id, data)

    def get(self, song_id: int) -> Object:
        """Gets an entity from the database
    
        Parameters
        ----------
        song_id: int
            The id of the song
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db.find(self._col, song_id)

    def get_all(self) -> list<Object>():
        """Finds all entities in the database
    
        Parameters
        ----------
        col
            The collection to be added to
            
        Returns
        -------
        Object list
            A list of the Objects in the database 
        """

        return self._db.find_all(self._col)

    def close(self):
        """Closes the conenction to the database"""
        
        self._db.close()