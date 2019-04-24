from similarity.similarity import process_segment, create_feature, load_song, flatten
from multiprocessing import Pool, Process, Queue, cpu_count, Manager
from database.song_segment import SongSegment
from utilities.get_song_id import get_song_id
from bson.objectid import ObjectId
import numpy as np
import librosa
import os

FOLDER = 'music_small'

filenames = []

for root, dirs, files in os.walk("./" + FOLDER):
    for filename in files:
        if filename.endswith('.wav'):
            filenames.append(filename)


segments = []
# Load features
for filename in filenames:
    print(filename)

    song_id = get_song_id(filename)

    data = load_song((song_id, FOLDER + '/' + filename))

    segments.append(data)

segs = flatten(segments)

print(segs)
