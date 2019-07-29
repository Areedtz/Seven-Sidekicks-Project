from database.mongo.storinator import Storinator
from database.mongo.video.video_emotion_database import VEDatabase


class VideoEmotion(Storinator):
    """
    An extension to the database class that calls it's methods with other
    parameters to lessen code

    Methods
    -------
    add(song_id, video_id, time, emotions)
        Insert video segment into the video_emotion collection

    get(song_id, video_id)
        Gets a video_segment from the video_emotion collection

    get_by_song_id(song_id)
        Gets all video segments from the video_emotion collection by song id

    get_all()
        Gets all video segments from the video_emotion collection

    close()
        Closes the connection to the database
    """

    def __init__(self):
        self._col = 'video_emotion'
        self._db = VEDatabase()

    def add(self, song_id: str, video_id: str,
            time: dict, emotions: dict) -> str:
        """Insert video segment into the video_emotion collection

        Parameters
        ----------
        song_id : str
            The id of the song
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

        return self._db.insert(self._col, song_id, video_id, time, emotions)

    def get(self, song_id: str, video_id: str) -> object:
        """Gets a video segment from the video_emotion collection

        Parameters
        ----------
        song_id : str
            The id of the song
        video_id : str
            The id of the video

        Returns
        -------
        object
            None if nothing was found, otherwise the document
        """

        return self._db.find(self._col, song_id, video_id)

    def get_by_song_id(self, song_id: str) -> [object]:
        """Gets all video segments from the video_emotion collection by song id

        Parameters
        ----------
        song_id : str
            The id of the song

        Returns
        -------
        object list
            A list of the objects in the video_emotion
            collection from a given song id
        """

        return self._db.find_by_song_id(self._col, song_id)

    def get_all(self) -> [object]:
        """Gets all video segments from the video_emotion collection

        Returns
        -------
        object list
            A list of the objects in the video_emotion collection
        """

        return self._db.find_all(self._col)

    def close(self):
        """Closes the connection to the database"""

        self._db.close()
