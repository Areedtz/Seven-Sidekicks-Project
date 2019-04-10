import re

def get_song_id(filename):
    return re.search(r"([0-9]+-[0-9]+-[0-9]+)", filename).group(0)