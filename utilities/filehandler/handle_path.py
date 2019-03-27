import sys
import os


def get_absolute_path(path):
    dirname = os.path.abspath(os.path.dirname(__file__)) + "/../.."
    return os.path.join(
        dirname,
        path)
