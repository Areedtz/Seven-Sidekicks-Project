from database.database import Database
from database.storinator import Storinator


class TrackEmotion(Storinator):
    def __init__(self):
        """initialises the database
    
        self
            the entity itself
        """
        self._col = 'track_emotion'
        self._db = Database()

    def add(self, song_id: int, data: dict):
        """adds entity to database
    
        self
            the entity itself
        song_id
            the id of the song
        data
            the data of the entity
            
        Returns
        -------
        the insert method from the database class with inputs
        """
        return self._db.insert(self._col, song_id, data)

    def get(self, song_id: int):
        """gets an entity from the database
    
        self
            the entity itself
        song_id
            the id of the song
            
        Returns
        -------
        the find method with inputs
        """
        return self._db.find(self._col, song_id)

    def get_all(self):
        """Finds all entities in the database
    
        self
            the entity itself
        col
            the collection to be added to
            
        Returns
        -------
        a pass
        """
        return self._db.find_all(self._col)
