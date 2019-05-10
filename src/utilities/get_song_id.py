import re


def get_song_id(filename: str) -> str:
    """Takes a file name and extracts the song id from that file name

    Parameters
    ----------
    filename
        The filename of a song

    Returns
    -------
        A string with the id of the song
    """

    return re.search(r"([0-9]+-[0-9]+-[0-9]+)", filename).group(0)

