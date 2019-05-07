from database.storinator import Storinator
from database.video_emotion_database import VEDatabase


class VideoEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    def add(self, song_id: int,
            video_id: int, time: int, emotions: dict):
        inserts data into the collection in the database

    def get(self, song_id: int, video_id: int):
        finds one entity given an id

    def get_by_song_id(self, song_id: int):
        finds all entities given an id

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

        self._col = 'video_emotion'
        self._db = VEDatabase()

    def add(self, song_id: int,
            video_id: int, time: int, emotions: dict):
        """adds entity to database

        Parameters
        ----------
        self
            the entity itself
        song_id
            the id of the song
        video_id
            the id of the video
        emotions
            the data from the entity
            
        Returns
        -------
        int
            an int of the id
        """

        return self._db.insert(self._col, song_id, video_id, time, emotions)


    def get(self, song_id: int, video_id: int):
        """gets an entity from the database
    
        Parameters
        ----------
        self
            the entity itself
        song_id
            the id of the song
        video_id
            the id from the video
            
        Returns
        -------
        Object
            either a None Object or the Object from the database
        """

        return self._db.find(self._col, song_id, video_id)

    def get_by_song_id(self, song_id: int):
        """gets all entities from the database by song_id
    
        Parameters
        ----------
        self
            the entity itself
        song_id
            the id of the song
            
        Returns
        -------
        Object list
            a list of the Objects in the database from a given video_id
        """

        return self._db.find_by_song_id(self._col, song_id)

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
        
        self._db.close()
