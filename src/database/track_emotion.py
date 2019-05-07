from database.database import Database
from database.storinator import Storinator


class TrackEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    def add(self, song_id: int, data: dict):
        Inserts data into the collection in the database

    def get(self, song_id: int):
        Finds one entity given an id

    def get_all(self):
        Finds all entities in the database
    
    """

    def __init__(self):

        self._col = 'track_emotion'
        self._db = Database()

    def add(self, song_id: int, data: dict):
        """Adds entity to database
    
        Parameters
        ----------
        song_id
            The id of the song
        data
            The data of the entity
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._col, song_id, data)

    def get(self, song_id: int):
        """Gets an entity from the database
    
        Parameters
        ----------
        song_id
            The id of the song
            
        Returns
        -------
            The find method with inputs
        """

        return self._db.find(self._col, song_id)

    def get_all(self):
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

        self._db.close()

