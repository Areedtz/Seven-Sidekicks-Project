from essentia.standard import MonoLoader

from utilities.filehandler.handle_path import get_absolute_path


def get_MonoLoaded_Song(song_path: str):
    """Loads the file given at the path and returns the raw audio data

    Parameters
    ----------
    song_path : str
        The file path of the song

    Returns
    -------
    vector_real
        The file's audio downmixed to mono

    """

    path = get_absolute_path(song_path)
    loader = MonoLoader(filename=path)

    return loader()
