import abc


# Interface for different databases
class Storinator(abc.ABC):
    # Abstract methods
    @abc.abstractmethod
    def add(self, col: str, id: str):
        """Add document to the given collection

        Parameters
        ----------
        col : str
            The collection to be added to
        id : int
            The id of the the document
        """

        pass

    @abc.abstractmethod
    def get(self, col: str, id: str):
        """Finds one document from the given collection

        Parameters
        ----------
        col : str
            The collection to search in
        id : str
            The id of the the document
        """

        pass

    @abc.abstractmethod
    def get_all(self, col: str):
        """Returns everything from the given collection

        Parameters
        ----------
        col : str
            The collection to search in
        """

        pass

    @abc.abstractmethod
    def close(self):
        pass
