import datetime

from typing import Dict

from pymongo import MongoClient
from utilities.config_loader import load_config


def _create_default_document(id : int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id : int
        id of the entity to be created
        
    Returns
    -------
    Dict
        Containing id and timestamp
    """

    return {
        "song_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }

def _create_default_segment_document(id : int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id : int
        id of the entity to be created
        
    Returns
    -------
    Dict
        Containing id and timestamp
    """

    return {
        "segment_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }
 
def _augment_document(doc1 : dict, doc2 : dict) -> Dict:
    """Combines parameters into a larger dictionary
    
    Parameters
    ----------
    doc1 : dict
        First dictionary
    doc2 : dict
        Second dictionary
        
    Returns
    -------
    Dict
        Dictionary combining two dictionaries
    """
    return {**doc1, **doc2}


# Generic class for making functions implementable
# for lower level classes of music analysis
class Database:
    """
    A database class used to communicate with a database

    Methods
    -------
    insert(col, song_id, doc)
        Inserts data into the collection in the database

    find(col, song_id)
        Finds one entity given an id

    find_all_by_id(name, song_id)
        Finds all entities given an id

    find_all(col)
        Finds all entities in the database
    
    """

    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'],
            password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col : str, song_id : int, doc : dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        col : str
            The collection to be added to
        song_id : int
            id of the song
        doc : dict
            Dictionary with data
            
        Returns
        -------
        int
            An int of the id
        """

        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id), doc)
        _id = collection.insert_one(ins).inserted_id
        return _id

# Gets the newest entry, the other option would be to overwrite it in the insert method
    def find(self, col : str, song_id : int) -> object:
        """Find one instance of the data requested
    
        Parameters
        ----------
        col : str
            The collection to be added to
        song_id : int
            id of the song
            
        Returns
        -------
        object
            Either a None object or the object from the database
        """
        if (self._db[col].count({'song_id': song_id}) > 0):
            res = self._db[col].find({'song_id': song_id}
                                      ).sort([('last_updated', -1)]
                                             ).limit(1)
            return res[0]

        return None

    def find_all_by_id(self, col : str, song_id : int) -> [object]:
        """Find all instances of the data requested in the collection by song_id
    
        Parameters
        ----------
        col: str
            The collection to be added to
        song_id: int
            id of the song
            
        Returns
        -------
        object list
            A list of the objects in the database from a given song_id
        """

        results = []
        for res in self._db[col].find({'song_id': song_id}):
            results.append(res)
        return results

    def find_all(self, col : str)  -> [object]:
        """Find all instances of the data requested in the collection
    
        Parameters
        ----------
        col : str
            The collection to be added to
            
        Returns
        -------
        object list
            A list of the objects in the database
        """

        results = []
        for r in self._db[col].find():
            results.append(r)
        return results

    def close(self):
        """Closes the conenction to the database"""

        self._client.close()