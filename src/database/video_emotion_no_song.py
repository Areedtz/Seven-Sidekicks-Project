from database.storinator import Storinator
from database.video_emotion_database_no_song import VEDatabase


# VideoEmotionNS = video emotions no song


class VideoEmotionNS(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    def add(self,
            video_id: int, time: int, emotions: dict):
        Inserts data into the collection in the database

    def get(self, video_id: int):
        Finds one entity given an id

    def get_by_video_id(self, video_id: int):
        Finds all entities given an id

    def get_all(self):
        Finds all entities in the database
    
    """

    def __init__(self):

        self._dbcol = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self,
            video_id: int, time: int, emotions: dict) -> int:
        """Adds entity to database
    
        Parameters
        ----------
        video_id
            The id of the video
        emotions
            The data from the entity
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._dbcol, video_id, time, emotions)

    def get(self, video_id: int):
        """Gets an entity from the database
    
        Parameters
        ----------
        video_id
            The id from the video
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db.find(self._dbcol, video_id)

    def get_by_video_id(self, video_id: int):
        """Gets all entities from the database by video_id
    
        Parameters
        ----------
        video_id
            The id of the video
            
        Returns
        -------
        Object list
            A list of the Objects in the database from a given video_id
        """

        return self._db.find_by_video_id(self._dbcol, video_id)

    def get_all(self):
        """Gets all entities from the database
            
        Returns
        -------
        Object list
            A list of the Objects in the database
        """

        return self._db.find_all(self._dbcol)

    def close(self):
        
        self._db.close()
