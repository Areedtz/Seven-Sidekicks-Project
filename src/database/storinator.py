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

    @abc.abstractmethod
    def close(self):
        pass


class SegmentStorinator(abc.ABC):
    @abc.abstractmethod
    def add(self, name, segment_id):
        pass

    @abc.abstractmethod
    def get(self, name, segment_id):
        pass

    @abc.abstractmethod
    def get_all(self, name):
        pass

    @abc.abstractmethod
    def close(self):
        pass
        
