import datetime


from typing import Dict
from pymongo import MongoClient
from utilities.config_loader import load_config


def _create_default_document(id: int, id2: int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id1
        song_id of the entity to be created
    id2
        video_id of the entity to be created
        
    Returns
    -------
    id and timestamp
    """
    return {
        "song_id": id,
        "video_id": id2,
        "last_updated": datetime.datetime.utcnow(),
    }

def _augment_document(doc1: dict, doc2: dict) -> Dict:
    """Combines parameters into a larger dictionary
    
    Parameters
    ----------
    doc1
        first dictionary
    doc2
        second dictionary
        
    Returns
    -------
    data
    """
    return {**doc1, **doc2}


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
               song_id, video_id, doc):
        """Insert data into the collection
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
        video_id
            id of the video
        doc
            dictionary with data
            
        Returns
        -------
        id of the entity
        """
        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id,
                                                         video_id), doc)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col,
             song_id, video_id):
        """Find one instance of the data requested
    
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
        video_id
            id of the videos
            
        Returns
        -------
        an Object
        """
        return self._db[col].find({'song_id': song_id, 'video_id': video_id}
                                  ).sort([('last_updated', -1)]
                                         ).limit(1)[0]

    def find_all(self, col):
        """Find all instances of the data requested in the collection
    
        self
            the entity itself
        col
            the collection to be added to
            
        Returns
        -------
        all a list of Objects
        """
        results = []
        for r in self._db[col].find():
            results.append(r)

        return results
