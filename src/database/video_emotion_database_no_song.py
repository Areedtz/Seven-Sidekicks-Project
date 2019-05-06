import datetime


from typing import Dict
from pymongo import MongoClient
from utilities.config_loader import load_config


def _create_default_document(id: int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id
        id of the entity to be created
        
    Returns
    -------
    id and timestamp
    """
    return {
        "video_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }

def _augment_document(id1: int, time: dict, emotion: dict) -> Dict:
    """Combines parameters into a larger dictionary
    
    Parameters
    ----------
    id1
        id of the entity
    time
        dictionary of time interval
    emotion
        dictionary of emotion data
        
    Returns
    -------
    data
    """
    return {**id1, **time, **emotion}

# Generic class for making functions implementable
# for lower level classes of music analysis
class VEDatabase:
    def __init__(self):
        """Creates the individual collection in the database
    
        Parameters
        ----------
        self
            the entity itself
            
        """
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col,
               video_id: int, time: dict, emotion: dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
        video_id
            id of the video
        doc
            dictionary with data
            
        Returns
        -------
        id of the entity
        """
        collection = self._db[col]
        ins = _augment_document(_create_default_document(
                                    video_id), time, emotion)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col, video_id: int):
        """Find one instance of the data requested
    
        self
            the entity itself
        col
            the collection to be added to
        video_id
            id of the video
            
        Returns
        -------
        an Object
        """
        return self._db[col].find({'video_id': video_id}
                                   ).sort([('last_updated', -1)]
                                          ).limit(1)[0]

    def find_by_video_id(self, col, video_id: int):
        """Find all instances of the data requested in the collection by video_id
    
        self
            the entity itself
        col
            the collection to be added to
        video_id
            id of the video
            
        Returns
        -------
        a list of Objects
        """
        results = []
        data =  self._db[col].find({'video_id': video_id})
        for i in data:
            del i['_id']
            i['last_updated'] = i['last_updated'].isoformat()
            results.append(i)
        return results

    def find_all(self, col):
        """Find all instances of the data requested in the collection
    
        self
            the entity itself
        col
            the collection to be added to
            
        Returns
        -------
        a list of Objects
        """
        results = []
        for r in self._db[col].find():
            results.append(r)
        return results
            
