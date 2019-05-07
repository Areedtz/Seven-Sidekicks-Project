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
        Inserts data into the collection in the database

    def get(self, song_id: int, video_id: int):
        Finds one entity given an id

    def get_by_song_id(self, song_id: int):
        Finds all entities given an id

    def get_all(self):
        Finds all entities in the database
    
    """

    def __init__(self):

        self._col = 'video_emotion'
        self._db = VEDatabase()

    def add(self, song_id: int,
            video_id: int, time: int, emotions: dict) -> int:
        """adds entity to database

        Parameters
        ----------
        song_id
            The id of the song
        video_id
            The id of the video
        emotions
            The data from the entity
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._col, song_id, video_id, time, emotions)


    def get(self, song_id: int, video_id: int):
        """gets an entity from the database
    
        Parameters
        ----------
        song_id
            The id of the song
        video_id
            The id from the video
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db.find(self._col, song_id, video_id)

    def get_by_song_id(self, song_id: int):
        """Gets all entities from the database by song_id
    
        Parameters
        ----------
        song_id
            The id of the song
            
        Returns
        -------
        Object list
            A list of the Objects in the database from a given video_id
        """

        return self._db.find_by_song_id(self._col, song_id)

    def get_all(self):
        """Gets all entities from the database
            
        Returns
        -------
        Object list
            A list of the Objects in the database
        """

        return self._db.find_all(self._col)

    def close(self):
        
        self._db.close()
