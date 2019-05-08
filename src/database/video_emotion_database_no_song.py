import datetime

from typing import Dict, Object, List

from pymongo import MongoClient
from utilities.config_loader import load_config


def _create_default_document(id: int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id: int
        id of the entity to be created
        
    Returns
    -------
    Dict
        Containing id and timestamp
    """

    return {
        "video_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }

def _augment_document(id1: dict, time: dict, 
                      emotion: dict) -> Dict:
    """Combines parameters into a larger dictionary
    
    Parameters
    ----------
    id1: dict
        id of the entity
    time: dict
        Dictionary of time interval
    emotion: dict
        Dictionary of emotion data
        
    Returns
    -------
    Dict
        Dictionary combining id, time interval and emotion data
    """

    return {**id1, **time, **emotion}


# Generic class for making functions implementable
# for lower level classes of music analysis
class VEDatabase:
    """
    A database class used to communicate with a database

    Methods
    -------
    insert(col,
               video_id, time, emotion)
        Inserts data into the collection in the database

    find(col, video_id)
        Finds one entity given an id

    find_by_video_id(col, video_id)
        Finds all entities given an id

    find_all(col)
        Finds all entities in the database
    
    """

    def __init__(self):

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
        col
            The collection to be added to
        video_id: int
            id of the video
        time: dict
            Dictionary with time interval
        emotion: dict
            Dictionary with emotion data
            
        Returns
        -------
        int
            An int of the id
        """

        collection = self._db[col]
        ins = _augment_document(_create_default_document(
                                    video_id), time, emotion)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col, video_id: int) -> Object:
        """Find one instance of the data requested
    
        Parameters
        ----------
        col
            The collection to be added to
        video_id
            id of the video
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db[col].find({'video_id': video_id}
                                   ).sort([('last_updated', -1)]
                                          ).limit(1)[0]

    def find_by_video_id(self, col, video_id: int) -> list<Object>():
        """Find all instances of the data requested in the collection by video_id
    
        Parameters
        ----------
        col
            The collection to be added to
        video_id
            id of the video
            
        Returns
        -------
        Object list
            A list of the Objects in the database from a given video_id
        """

        results = []
        data =  self._db[col].find({'video_id': video_id})
        for i in data:
            del i['_id']
            i['last_updated'] = i['last_updated'].isoformat()
            results.append(i)
        return results

    def find_all(self, col) -> list<Object>():
        """Find all instances of the data requested in the collection
    
        Parameters
        ----------
        col
            The collection to be added to
            
        Returns
        -------
        Object list
            A list of the Objects in the database 
        """

        results = []
        for r in self._db[col].find():
            results.append(r)
        return results
            

    def close(self):
        """Closes the conenction to the database"""
        
        self._client.close()