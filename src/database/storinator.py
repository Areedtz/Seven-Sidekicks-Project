import abc


class Storinator(abc.ABC):
    @abc.abstractmethod
    def add(self, name, song_id):
        pass

    @abc.abstractmethod
    def get(self, name, song_id):
        pass

    @abc.abstractmethod
    def get_all(self, name):
        pass
