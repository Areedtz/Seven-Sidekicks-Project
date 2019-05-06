import abc


# Interface for database classes
class Storinator(abc.ABC):

    # Generic methods for the database classes
    @abc.abstractmethod
    def add(self, col, id: int):
        """Adds entity to database
    
        self
            the entity itself
        col
            the collection to be added to
        id
            the id of the the entity
            
        Returns
        -------
        a pass
        """
        pass

    @abc.abstractmethod
    def get(self, col, id: int):
        """Finds one entity from the database
    
        self
            the entity itself
        col
            the collection to be added to
        id
            the id of the the entity
            
        Returns
        -------
        a pass
        """
        pass

    @abc.abstractmethod
    def get_all(self, col):
        """Finds all entities in the database
    
        self
            the entity itself
        col
            the collection to be added to
            
        Returns
        -------
        a pass
        """
        pass
