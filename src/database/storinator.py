import abc


# Interface for different databases
class Storinator(abc.ABC):
    """
    A generic class to structure future database classes

    Methods
    -------
    def add(self, col, id: int):
        Adds entity to database

    def get(self, col, id: int):
        Finds one entity from the database

    def get_all(self, col):
        Finds all entities in the database
    
    """


    # Abstract methods
    @abc.abstractmethod
    def add(self, col, id: int):
        """Adds entity to database
    
        Parameters
        ----------
        col
            The collection to be added to
        id
            The id of the the entity
        pass
        """

        pass
    @abc.abstractmethod
    def get(self, col, id: int):
        """Finds one entity from the database
    
        Parameters
        ----------
        col
            The collection to be added to
        id
            The id of the the entity
        """

        pass

    @abc.abstractmethod
    def get_all(self, col):
        """Finds all entities in the database
    
        Parameters
        ----------
        col
            The collection to be added to
        """

        pass

    @abc.abstractmethod
    def close(self):
        pass


class SegmentStorinator(abc.ABC):
    @abc.abstractmethod
    def add(self, name, segment_id):
        """Adds entity to database
    
        Parameters
        ----------
        col
            The collection to be added to
        id
            The id of the the entity
        """

        pass

    @abc.abstractmethod
    def get(self, name, segment_id):
        """Finds one entity from the database
    
        Parameters
        ----------
        col
            The collection to be added to
        id
            The id of the the entity
        """

        pass

    @abc.abstractmethod
    def get_all(self, name):
        """Finds all entities in the database
    
        Parameters
        ----------
        col
            The collection to be added to
        """

        pass

    @abc.abstractmethod
    def close(self):
        pass
