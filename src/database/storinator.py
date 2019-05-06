import abc


# Interface for different databases
class Storinator(abc.ABC):

    # Abstract methods
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
