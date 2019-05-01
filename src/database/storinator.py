import abc

# Interface for database classes
class Storinator(abc.ABC):

    # Generic methods for the database classes
    @abc.abstractmethod
    def add(self, name, song_id):
        pass

    @abc.abstractmethod
    def get(self, name, song_id):
        pass

    @abc.abstractmethod
    def get_all(self, name):
        pass
