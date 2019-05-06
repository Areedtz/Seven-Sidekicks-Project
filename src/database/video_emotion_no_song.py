from database.storinator import Storinator
from database.video_emotion_database_no_song import VEDatabase

# VideoEmotionNS = video emotions no song
class VideoEmotionNS(Storinator):
    def __init__(self):
        """initialises the database
    
        self
            the entity itself
        """
        self._dbname = 'video_emotion_no_song'
        self._db = VEDatabase()

    def add(self,
            video_id: int, emotions: dict):
        """adds entity to database
    
        self
            the entity itself
        video_id
            the id of the video
        emotions
            the data from the entity
            
        Returns
        -------
        the insert method from the database class with inputs
        """
        return self._db.insert(self._dbname, video_id, emotions)

    def get(self, video_id: int):
        """gets an entity from the database
    
        self
            the entity itself
        video_id
            the id from the video
            
        Returns
        -------
        the find method with inputs
        """
        return self._db.find(self._dbname, video_id)

    def get_all(self):
        """gets all entities from the database
    
        self
            the entity itself
            
        Returns
        -------
        the find_all method with inputs
        """
        return self._db.find_all(self._dbname)
