import sys
import os


def get_absolute_path(path):
    # Path up to the SevenSidekicks main folder with "/../.."
    dirname = os.path.abspath(os.path.dirname(__file__)) + "/../.."
    return os.path.join(
        dirname,
        path)
