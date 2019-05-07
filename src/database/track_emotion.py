from database.database import Database
from database.storinator import Storinator


class TrackEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    def add(self, song_id: int, data: dict):
        inserts data into the collection in the database

    def get(self, song_id: int):
        finds one entity given an id

    def get_all(self):
        finds all entities in the database
    
    """

    def __init__(self):

        self._col = 'track_emotion'
        self._db = Database()

    def add(self, song_id: int, data: dict):
        """adds entity to database
    
        Parameters
        ----------
        self
            the entity itself
        song_id
            the id of the song
        data
            the data of the entity
            
        Returns
        -------
        int
            an int of the id
        """

        return self._db.insert(self._col, song_id, data)

    def get(self, song_id: int):
        """gets an entity from the database
    
        Parameters
        ----------
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
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
            
        Returns
        -------
        Object list
            a list of the Objects in the database 
        """

        return self._db.find_all(self._col)

    def close(self):
        """closes the connection to the database
    
        Parameters
        ----------
        self
            the entity itself
        """

        self._db.close()

