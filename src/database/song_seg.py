from database.database import Database
from database.storinator import Storinator



class SSegmentation(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    def add(self, song_id: int, time_from: int, time_to: int):
        inserts data into the collection in the database

    def get(self, song_id: int):
        finds one entity given an id

    def get_all(self):
        finds all entities in the database
    """
    
    def __init__(self):
        """initialises the database
    
        Parameters
        ----------
        self
            the entity itself
        """

        self._col = 'song_segmentation'
        self._db = Database()

    def add(self, song_id: int, time_from: int, time_to: int):
        """adds entity to database
    
        Parameters
        ----------
        self
            the entity itself
        song_id
            the id of the song
        time_from
            the start of the time interval
        time_to
            the end of the time interval
            
        Returns
        -------
        int
            an int of the id
        """

        return self._db.insert(self._col, song_id, {
            "time_from": time_from,
            "time_to": time_to
        })

    def get(self, song_id: int):
        """gets an entity from the database
    
        Parameters
        ----------
        self
            the entity itself
        song_id
            the id of the song
            
        Object
            either a None Object or the Object from the database
        """

        return self._db.find(self._col, song_id)

    def get_all(self):
        """gets all entities from the database
    
        Parameters
        ----------
        self
            the entity itself
            
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

        self._client.close()
