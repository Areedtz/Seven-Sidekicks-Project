from database.storinator import Storinator
from database.video_emotion_database_no_song import VEDatabase


# VideoEmotionNS = video emotions no song


class VideoEmotionNS(Storinator):
    def __init__(self):
        """initialises the database
    
        Parameters
        ----------
        self
            the entity itself
        """

        self._dbcol = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self,
            video_id: int, time: int, emotions: dict):
        """adds entity to database
    
        Parameters
        ----------
        self
            the entity itself
        video_id
            the id of the video
        emotions
            the data from the entity
            
        Returns
        -------
        int
            an int of the id
        """

        return self._db.insert(self._dbcol, video_id, time, emotions)

    def get(self, video_id: int):
        """gets an entity from the database
    
        Parameters
        ----------
        self
            the entity itself
        video_id
            the id from the video
            
        Returns
        -------
        Object
            either a None Object or the Object from the database
        """

        return self._db.find(self._dbcol, video_id)

    def get_by_video_id(self, video_id: int):
        """gets all entities from the database by video_id
    
        Parameters
        ----------
        self
            the entity itself
        video_id
            the id of the video
            
        Returns
        -------
        Object list
            a list of the Objects in the database from a given video_id
        """

        return self._db.find_by_video_id(self._dbcol, video_id)

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

        return self._db.find_all(self._dbcol)

    def close(self):
        """closes the connection to the database
    
        Parameters
        ----------
        self
            the entity itself
        """
        
        self._db.close()
