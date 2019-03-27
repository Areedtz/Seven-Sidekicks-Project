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
    print('Loaded: ' + filename)
    songs = []

    print('Processing: ' + filename)
    for i in range(0, y.shape[0]//sr//5 - 1):
        sample = y[(i * sr * 5):
                   ((i + 1) * sr * 5)]

        harmonic, percussive = librosa.effects.hpss(sample)

        tempo, beat_frames = librosa.beat.beat_track(
            y=percussive, sr=sr)

        mfcc = librosa.feature.mfcc(sample)
        fm = np.ndarray.flatten(mfcc)

        stft = np.abs(librosa.stft(sample))
        amp = librosa.amplitude_to_db(stft, ref=np.max)
        fa = np.ndarray.flatten(amp)

        chromagram = librosa.feature.chroma_cqt(y=harmonic, sr=sr)
        fc = np.ndarray.flatten(chromagram)

        songs.append((filename, 5*i, fm, fa, fc, np.array(tempo)))

    print('Processed: ' + filename)
    return songs


p = Pool(cpu_count())
filenames = []

for root, dirs, files in os.walk("./" + folder):
    for filename in files:
        if filename.endswith('.wav'):
            filenames.append(filename)

songs = p.map(process_file, filenames)

songs = flatten(songs)

print(len(songs))


def myround(x, base=5):
    return base * round(x/base)


weights = (4, 1, 400, 300)

for line in fileinput.input():
    if (len(line.split(' ')) < 2):
        print("Invalid search")
        continue

    if (len(line.split(' ')) == 4):
        split = line.split(' ')
        weights = (int(split[0]), int(split[1]), int(split[2]), int(split[3]))
        continue

    sample_index = next(i for i, v in enumerate(songs) if v[0] == line.split(' ')
                        [0] and v[1] == myround(int(line.split(' ')[1])))

    if (sample_index == None):
        print("Not found")
        continue

    dist1s = []
    dist2s = []
    dist3s = []
    dist4s = []
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
        dist4 = distance.euclidean(
            songs[sample_index][5], songs[i][5])
        dist4s.append(dist4)
        dist = dist1 * weights[0] + dist2 * weights[1] + \
            dist3 * weights[2] + dist4 * weights[3]

        if i != sample_index and songs[sample_index][0] != songs[i][0] and dist < low_dist:
            low_dist = dist
            low = i

    print(sum(dist1s) / len(songs))
    print(sum(dist2s) / len(songs))
    print(sum(dist3s) / len(songs))
    print(sum(dist4s) / len(songs))

    print(songs[low][0], songs[low][1], low_dist)

    # Save comparison file
    y, sr = librosa.load('./' + folder + '/' + songs[sample_index][0])
    sample = y[songs[sample_index][1]*sr: (songs[sample_index][1]+5)*sr]
    y, sr = librosa.load('./' + folder + '/' + songs[low][0])
    sample1 = y[songs[low][1]*sr: (songs[low][1]+5)*sr]
    librosa.output.write_wav('random_samples/' + songs[sample_index][0] + '-' + str(
        songs[sample_index][1]) + '_' + songs[low][0] + '-' + str(songs[low][1]) + '.wav', np.concatenate([sample, sample1]), sr)
