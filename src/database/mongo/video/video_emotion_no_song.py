from typing import Dict

from database.mongo.storinator import Storinator
from database.mongo.video.video_emotion_database_no_song import VEDatabase


# VideoEmotionNS = video emotions no song


class VideoEmotionNS(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    add(video_id, time, emotions)
        Insert video segment into the video_emotion_no_song collection

    get(video_id)
        Gets a video segment from the video_emotion_no_song collection

    get_by_video_id(video_id)
        Gets all video segments from the video_emotion_no_song collection by video id

    get_all()
        Gets all video segments from the video_emotion_no_song collection

    close()
        Closes the connection to the database
    """

    def __init__(self):
        self._dbcol = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self, video_id: str, time: dict, emotions: dict) -> str:
        """Insert video segment into the video_emotion_no_song collection

        Parameters
        ----------
        video_id : str
            The id of the video
        time : dict
            Dictionary with time interval
        emotions : dict
            Dictionary with emotion data

        Returns
        -------
        str
            The created document's object id
        """

        return self._db.insert(self._dbcol, video_id, time, emotions)

    def get(self, video_id: str) -> object:
        """Gets a video segment from the video_emotion_no_song collection

        Parameters
        ----------
        video_id : str
            The id of the video

        Returns
        -------
        object
            None if nothing was found, otherwise the document
        """

        return self._db.find(self._dbcol, video_id)

    def get_by_video_id(self, video_id: str) -> [object]:
        """Gets all video segments from the video_emotion_no_song collection by video id

        Parameters
        ----------
        video_id : str
            The id of the video

        Returns
        -------
        object list
            A list of the objects in the video_emotion_no_song collection from a given song id
        """

        return self._db.find_by_video_id(self._dbcol, video_id)

    def get_all(self) -> [object]:
        """Gets all video segments from the video_emotion_no_song collection

        Returns
        -------
        object list
            A list of the objects in the video_emotion_no_song collection
        """

        return self._db.find_all(self._dbcol)

    def close(self):
        """Closes the connection to the database"""

        self._db.close()
