import os


def split_song(audio, segment_length=5):
    sr = 44100
    song_length = len(audio) // sr

    segment_list = []
    for i in range(segment_length, song_length, segment_length):
        segment = audio[(i-segment_length)*sr: i*sr]
        segment_list.append(segment)

    return segment_list
