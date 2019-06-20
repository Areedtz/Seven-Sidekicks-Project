#!/usr/local/bin/python3.6

import os

from rest_api.application import app, hostURL, hostPort

from similarity.similarity import analyze_songs, _load_songs
from utilities.get_song_id import get_song_id

if __name__ == "__main__":
    filenames = []

    for root, dirs, files in os.walk('../music_medium'):
        for filename in files:
            if filename.endswith('.wav'):
                filenames.append(filename)

    songs = list(
        map(lambda name: (get_song_id(name), '../music_medium/' + name), filenames))

    analyze_songs(songs)
