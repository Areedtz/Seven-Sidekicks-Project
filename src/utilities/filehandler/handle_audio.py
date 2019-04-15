import sys
import os

from essentia.standard import MonoLoader

from utilities.filehandler.handle_path import get_absolute_path


def get_MonoLoaded_Song(path):
    path = get_absolute_path(path)
    loader = MonoLoader(filename=path)

    return loader()
