from similarity.similarity import process_segment, create_feature, load_song, flatten, create_bucket, query, find_best
from multiprocessing import Pool, Process, Queue, cpu_count, Manager
from database.song_segment import SongSegment
from utilities.get_song_id import get_song_id
from bson.objectid import ObjectId
import numpy as np
import librosa
import os
import time

FOLDER = '../music_medium'

filenames = []

for root, dirs, files in os.walk("./" + FOLDER):
    for filename in files:
        if filename.endswith('.wav'):
            filenames.append(filename)


def load_files(filenames):
    segments = []
    for filename in filenames:
        segments.append(load(filename))
    return flatten(segments)


def load(filename):
    print(filename)

    song_id = get_song_id(filename)

    data = load_song((song_id, FOLDER + '/' + filename))

    return data


fileChunks = []

x = len(filenames) // cpu_count() + 1
for i in range(0, cpu_count()):
    fileChunks.append(filenames[i * x: (i+1) * x])

p = Pool(cpu_count())

segments = p.map(load_files, fileChunks)

p.close()

segs = flatten(segments)

BUCKET_SIZE = 60 * 1000

bucketSize = (len(segs) // BUCKET_SIZE) + 1

print("Buckets: " + str(bucketSize))
print("Segment amount:" + str(len(segs)))

buckets = []
for i in range(0, bucketSize):
    segments = segs[i * BUCKET_SIZE:(i+1) * BUCKET_SIZE]

    data = np.array(list(map(lambda x: x[3], segments)))

    bucket = create_bucket(data)

    buckets.append(bucket)


def find_matches(searchSegment):
    print()
    s = time.time()

    matches = []
    for i in range(0, bucketSize):
        x = query(buckets[i], np.array(searchSegment[3]))

        for j in x:
            match = segs[i*BUCKET_SIZE+j]
            matches.append(match)
    print(time.time() - s)

    for match in find_best(matches, searchSegment):
        print(match[0])
        print(match[1] + ": " + str(match[2]))


p = Pool(cpu_count())

p.map(find_matches, segs)

p.close()
