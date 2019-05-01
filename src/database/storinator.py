import abc

# Interface for different databases
class Storinator(abc.ABC):

    # Abstract methods
    @abc.abstractmethod
    def add(self, name, song_id):
        pass

    @abc.abstractmethod
    def get(self, name, song_id):
        pass

    @abc.abstractmethod
    def get_all(self, name):
        pass
