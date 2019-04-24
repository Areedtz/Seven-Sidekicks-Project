import librosa
import fileinput
from scipy.spatial import distance
import numpy as np
import os
import falconn
from multiprocessing import Pool, Process, Queue, cpu_count, Manager
from database.song_segment import SongSegment

MATCHES = 10

segments = SongSegment()


def flatten(l): return [item for sublist in l for item in sublist]


def process_segment(segment, sr):
    harmonic, percussive = librosa.effects.hpss(segment)

    tempogram = librosa.feature.tempogram(
        percussive, hop_length=1024, win_length=16)

    mfcc = librosa.feature.mfcc(segment, hop_length=1024)

    chromagram = librosa.feature.chroma_cqt(y=harmonic, sr=sr, hop_length=1024)

    return mfcc, chromagram, tempogram


def load_song(song):
    song_id, filename = song
    return _load_song(song_id, filename, False)


def _load_song(song_id, filename, force):
    segs = segments.get_all_with_id(song_id)

    segment_data = []

    if (force or segs == []):
        # No segments in db, which means no features in db
        y, sr = librosa.load(filename)

        for i in range(0, y.shape[0]//sr//5 - 1):

            sample = y[(i * sr * 5):
                       ((i + 1) * sr * 5)]

            mfcc, chromagram, tempogram = process_segment(sample, sr)

            _id = segments.add(song_id, i*5*1000, (i+1)*5*1000, mfcc.tobytes(),
                               chromagram.tobytes(), tempogram.tobytes(), [])

            feature = create_feature(mfcc, chromagram, tempogram)

            segment_data.append((_id, song_id, i*5, feature))

    else:
        # There are segments in db, try to look for features
        for i in range(0, len(segs)):
            segment = segs[i]

            feature = create_feature(np.frombuffer(segment['mfcc']), np.frombuffer(
                segment['chroma']), np.frombuffer(segment['tempogram']))

            segment_data.append((segment['_id'], song_id, i*5, feature))

    return segment_data


def create_feature(mfcc, chroma, tempogram):
    fm = mfcc
    fc = chroma
    ft = tempogram
    if (fm.ndim != 1):
        fm = fm.flatten()
    if (fc.ndim != 1):
        fc = fc.flatten()
    if (ft.ndim != 1):
        ft = ft.flatten()
    return np.concatenate((fm, fc * 133, ft * 280))


def create_bucket(segments):
    params_cp = falconn.LSHConstructionParameters()
    params_cp.dimension = len(segments[0])
    params_cp.lsh_family = falconn.LSHFamily.CrossPolytope
    params_cp.distance_function = falconn.DistanceFunction.EuclideanSquared
    params_cp.l = 25
    params_cp.num_rotations = 2
    params_cp.seed = 5721840
    params_cp.num_setup_threads = 0
    params_cp.storage_hash_table = falconn.StorageHashTable.BitPackedFlatHashTable
    falconn.compute_number_of_hash_functions(18, params_cp)

    table = falconn.LSHIndex(params_cp)
    table.setup(segments)

    return (segments, table)


def query(data, segment):
    segments, table = data

    query_object = table.construct_query_pool()
    query_object.set_num_probes(25)

    return query_object.find_k_nearest_neighbors(segment, MATCHES)


def add_songs(songs):
    p = Pool(min(len(songs), cpu_count()))

    data = p.map(load_song, songs)

    return data


def dist(seg1, seg2):
    return distance.euclidean(seg1[3], seg2[3])


def find_best(matches, segment):
    lows = []
    for i in range(0, len(matches)):
        dist = distance.euclidean(
            segment[3], matches[i][3])

        if segment[0] != matches[i][0]:
            if len(lows) < MATCHES:
                lows.append((i, dist))
            else:
                for j in range(0, MATCHES):
                    if lows[j][1] > dist:
                        lows.insert(j, (i, dist))
                        lows.pop()
                        break

    return list(map(lambda i: matches[i[0]], lows))
