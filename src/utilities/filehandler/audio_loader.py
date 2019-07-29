# Some linting might say these imports fail
from essentia.standard import MonoLoader
from essentia.streaming import AudioLoader

from utilities.filehandler.handle_path import get_absolute_path


def get_mono_loaded_song(song_path: str):
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


def get_audio_loaded_song(song_path: str):
    """Loads the file given at the path and returns the audio as a stereosample

    Parameters
    ----------
    song_path : str
        The file path of the song

    Returns
    -------
    stereosample
        The input stereo audio signal

    """

    path = get_absolute_path(song_path)
    loader = AudioLoader(filename=path)

    return loader
