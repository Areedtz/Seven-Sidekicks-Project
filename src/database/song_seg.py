from database.database import Database
from database.storinator import Storinator



class SSegmentation(Storinator):
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
        the insert method from the database class with inputs
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
            
        Returns
        -------
        the find method with inputs
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
        the find_all method with inputs
        """
        
        return self._db.find_all(self._col)
