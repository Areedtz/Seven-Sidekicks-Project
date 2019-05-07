from database.database import Database
from database.storinator import Storinator



class SSegmentation(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    def add(self, song_id: int, time_from: int, time_to: int):
        Inserts data into the collection in the database

    def get(self, song_id: int):
        Finds one entity given an id

    def get_all(self):
        Finds all entities in the database
    """
    
    def __init__(self):
        self._col = 'song_segmentation'
        self._db = Database()

    def add(self, song_id: int, time_from: int, time_to: int):
        """adds entity to database
    
        Parameters
        ----------
        song_id
            The id of the song
        time_from
            The start of the time interval
        time_to
            The end of the time interval
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._col, song_id, {
            "time_from": time_from,
            "time_to": time_to
        })

    def get(self, song_id: int):
        """Gets an entity from the database
    
        Parameters
        ----------
        song_id
            The id of the song
            
        Object
            Either a None Object or the Object from the database
        """

        return self._db.find(self._col, song_id)

    def get_all(self):
        """Gets all entities from the database
            
        Returns
        -------
        Object list
            A list of the Objects in the database
        """
        return self._db.find_all(self._col)

    def close(self):
        """Closes the connection to the database

        Parameters
        ----------
        self
            The entity itself
        """

        self._client.close()
