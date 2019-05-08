from typing import Dict, Object, List

from database.storinator import Storinator
from database.video_emotion_database import VEDatabase


class VideoEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    add(song_id,
            video_id, time, emotions)
        Inserts data into the collection in the database

    get(song_id, video_id)
        Finds one entity given an id

    get_by_song_id(song_id)
        Finds all entities given an id

    get_all()
        Finds all entities in the database
    
    """

    def __init__(self):

        self._col = 'video_emotion'
        self._db = VEDatabase()

    def add(self, song_id : int,
            video_id : int, time : dict, emotions : dict) -> int:
        """Insert video_segment into the collection

        Parameters
        ----------
        song_id : int
            The id of the song
        video_id : int
            The id of the video
        time : dict
            Dictionary with time interval
        emotions : dict
            Dictionary with emotion data
            
        Returns
        -------
        int
            An int of the id
        """

        return self._db.insert(self._col, song_id, video_id, time, emotions)


    def get(self, song_id: int, video_id: int) -> Object:
        """gets a video_segment from the database
    
        Parameters
        ----------
        song_id : int
            The id of the song
        video_id : int
            The id from the video
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db.find(self._col, song_id, video_id)

    def get_by_song_id(self, song_id: int) -> list<Object>():
        """Gets all video_segments from the database by song_id
    
        Parameters
        ----------
        song_id : int
            The id of the song
            
        Returns
        -------
        Object list
            A list of the Objects in the database from a given video_id
        """

        return self._db.find_by_song_id(self._col, song_id)

    def get_all(self) -> list<Object>():
        """Gets all video_segments from the database
            
        Returns
        -------
        Object list
            A list of the Objects in the database
        """

        return self._db.find_all(self._col)

    def close(self):
        """Closes the conenction to the database"""
        
        self._db.close()