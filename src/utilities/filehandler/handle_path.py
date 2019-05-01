import os


def get_absolute_path(path: str) -> str:
    """Gets and returns the absolute path for the root of source code

    Parameters
    ----------
    path : str
        The location of the file to give the absolute path for

    Returns
    -------
    string
        a path to the supplied file
    """

    dirname = os.path.abspath(os.path.dirname(__file__)) + "/../.."
    return os.path.join(dirname, path)
