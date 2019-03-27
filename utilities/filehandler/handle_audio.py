from utilities.filehandler import get_absolute_path
from essentia.standard import MonoLoader


def get_MonoLoaded_Song(path):
    path = get_absolute_path(path)
    loader = MonoLoader(filename=path)

    return loader()