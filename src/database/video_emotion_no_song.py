from typing import Dict, Object, List

from database.storinator import Storinator
from database.video_emotion_database_no_song import VEDatabase


# VideoEmotionNS = video emotions no song


class VideoEmotionNS(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    add(video_id, time, emotions)
        Inserts data into the collection in the database

    get(video_id)
        Finds one entity given an id

    get_by_video_id(video_id)
        Finds all entities given an id

    get_all()
        Finds all entities in the database
    
    """

    def __init__(self):

        self._dbcol = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self,
            video_id: int, time: dict, emotions: dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        video_id: int
            The id of the video
        time: dict
            Dictionary with time interval
        emotions: dict
            Dictionary with emotion data
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._dbcol, video_id, time, emotions)

    def get(self, video_id: int) -> Object:
        """Gets an entity from the database
    
        Parameters
        ----------
        video_id: int
            The id from the video
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db.find(self._dbcol, video_id)

    def get_by_video_id(self, video_id: int) -> list<Object>():
        """Gets all entities from the database by video_id
    
        Parameters
        ----------
        video_id: int
            The id of the video
            
        Returns
        -------
        Object list
            A list of the Objects in the database from a given video_id
        """

        return self._db.find_by_video_id(self._dbcol, video_id)

    def get_all(self) -> list<Object>():
        """Gets all entities from the database
            
        Returns
        -------
        Object list
            A list of the Objects in the database
        """

        return self._db.find_all(self._dbcol)

    def close(self):
        """Closes the conenction to the database"""
        
        self._db.close()