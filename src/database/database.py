import datetime


from typing import Dict
from pymongo import MongoClients
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
        "song_id": id,
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
class Database:

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
        self._db = self._client['dr']

    def insert(self, col, song_id: int, doc: dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
        doc
            dictionary with data
            
        Returns
        -------
        id of the entity
        """
        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id), doc)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col, song_id: int):
        """Find one instance of the data requested
    
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
            
        Returns
        -------
        an Object
        """
        if (self._db[col].count({'song_id': song_id}) > 0):
            res = self._db[col].find({'song_id': song_id}
                                      ).sort([('last_updated', -1)]
                                             ).limit(1)
            return res[0]

        return None

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
