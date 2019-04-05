import librosa
import fileinput
from librosa import display
from scipy.spatial import distance
import numpy as np
import os

from multiprocessing import Pool, Process, Queue, cpu_count, Manager

import matplotlib.pyplot as plt

folder = 'music'


def flatten(l): return [item for sublist in l for item in sublist]


def process_file(filename):
    print('Loading: ' + filename)
    y, sr = librosa.load('./' + folder + '/' + filename)
    songs = []

    print('Processing: ' + filename)
    for i in range(0, y.shape[0]//sr//5 - 1):
        sample = y[(i * sr * 5):
                   ((i + 1) * sr * 5)]

        harmonic, percussive = librosa.effects.hpss(sample)

        tempogram = librosa.feature.tempogram(percussive)
        ft = np.ndarray.flatten(tempogram)

        mfcc = librosa.feature.mfcc(sample)
        fm = np.ndarray.flatten(mfcc)

        chromagram = librosa.feature.chroma_cqt(y=harmonic, sr=sr)
        fc = np.ndarray.flatten(chromagram)

        # Because we use a lot of RAM :)
        del harmonic
        del percussive
        del tempogram
        del chromagram

        songs.append((filename, 5*i, fm, fc, ft))

    del y

    print('Done: ' + filename)
    return songs


p = Pool(cpu_count())
#p = Pool(1)

filenames = []

for root, dirs, files in os.walk("./" + folder):
    for filename in files:
        if filename.endswith('.wav'):
            filenames.append(filename)

songs = p.map(process_file, filenames)

p.close()

songs = flatten(songs)

print(len(songs))


def myround(x, base=5):
    return base * round(x/base)


weights = (3, 400, 200)


def find_similar(name):
    sample_index = next((i for i, v in enumerate(songs)
                         if v[0] == name and v[1] == 30), None)

    if (sample_index == None):
        print("Not found")
        return

    dist1s = []
    dist2s = []
    dist3s = []
    low = 0
    low_dist = 10000000
    for i in range(0, len(songs)):
        dist1 = distance.euclidean(
            songs[sample_index][2], songs[i][2])
        dist1s.append(dist1)
        dist2 = distance.euclidean(
            songs[sample_index][3], songs[i][3])
        dist2s.append(dist2)
        dist3 = distance.euclidean(
            songs[sample_index][4], songs[i][4])
        dist3s.append(dist3)
        dist = dist1 * weights[0] + dist2 * weights[1] + \
            dist3 * weights[2]

        if i != sample_index and songs[sample_index][0] != songs[i][0] and dist < low_dist:
            low_dist = dist
            low = i

    print(sum(dist1s) / len(songs))
    print(sum(dist2s) / len(songs))
    print(sum(dist3s) / len(songs))
    print()

    print(songs[low][0], songs[low][1], low_dist)
    print()

    # Save comparison file
    y, sr = librosa.load('./' + folder + '/' + songs[sample_index][0])
    sample = y[songs[sample_index][1]*sr: (songs[sample_index][1]+5)*sr]
    y, sr = librosa.load('./' + folder + '/' + songs[low][0])
    sample1 = y[songs[low][1]*sr: (songs[low][1]+5)*sr]
    librosa.output.write_wav('random_samples/' + str(weights) + '_' + songs[sample_index][0] + '-' + str(
        songs[sample_index][1]) + '_' + songs[low][0] + '-' + str(songs[low][1]) + '.wav', np.concatenate([sample, sample1]), sr)


for line in fileinput.input():
    del p

    if (len(line.split(' ')) == 3):
        split = line.split(' ')
        weights = (int(split[0]), int(split[1]), int(split[2]))

    p = Pool(cpu_count())
    # only does sideeffects, but is easy async
    p.map(find_similar, filenames)

    p.close()
