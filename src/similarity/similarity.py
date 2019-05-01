import librosa
import fileinput
from scipy.spatial import distance
import numpy as np
import os
import falconn
from multiprocessing import Pool, Process, Queue, cpu_count, Manager
from database.song_segment import SongSegment

MATCHES = 10
BUCKET_SIZE = 60 * 100


def flatten(l): return [item for sublist in l for item in sublist]


def process_segment(segment, sr):
    harmonic, percussive = librosa.effects.hpss(segment)

    tempogram = librosa.feature.tempogram(
        percussive, hop_length=1024, win_length=16)

    mfcc = librosa.feature.mfcc(segment, hop_length=1024)

    chromagram = librosa.feature.chroma_cqt(y=harmonic, sr=sr, hop_length=1024)

    return mfcc, chromagram, tempogram


def load_songs(songs):
    segments = SongSegment()
    for song in songs:
        song_id, filename = song
        _load_song(song_id, filename, segments, False)


def load_song(song):
    song_id, filename = song
    segments = SongSegment()
    return _load_song(song_id, filename, segments, False)


def _load_song(song_id, filename, segments, force):
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
        # There are segments in db, look for features
        for i in range(0, len(segs)):
            segment = segs[i]

            feature = create_feature(np.frombuffer(segment['mfcc']), np.frombuffer(
                segment['chroma']), np.frombuffer(segment['tempogram']))

            segment_data.append((segment['_id'], song_id, i*5, feature))

    return segment_data


def process_db_segment(segment):
    feature = create_feature(np.frombuffer(segment['mfcc']), np.frombuffer(
        segment['chroma']), np.frombuffer(segment['tempogram']))

    return (segment['_id'], segment['song_id'], segment['time_from'] // 1000, feature)


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


def add_songs(songs):
    p = Pool(min(len(songs), cpu_count()))

    data = p.map(load_song, songs)

    return data


def dist(seg1, seg2):
    return distance.euclidean(seg1[3], seg2[3])


def find_best(matches, segment):
    lows = []
    for i in range(0, len(matches)):
        distance = dist(
            segment, matches[i])

        if segment[1] != matches[i][1]:
            if len(lows) < MATCHES:
                lows.append((i, distance))
            else:
                for j in range(0, MATCHES):
                    if lows[j][1] > distance:
                        lows.insert(j, (i, distance))
                        lows.pop()
                        break

    return list(map(lambda i: (matches[i[0]], i[1]), lows))


def query_similar(song_id, from_time, to_time):
    seg_db = SongSegment()
    segments = seg_db.get_all_with_id(song_id)

    best = None
    for segment in segments:
        localdist = from_time - segment['time_from']
        if best == None or localdist < best[0]:
            best = (localdist, segment)

    if best == None or 'similar' not in best[1]:
        return None

    segment = best[1]

    similar = segment['similar']

    similar_ids = list(map(lambda sim: sim['id'], similar))

    ss = SongSegment()
    similar = ss.get_with_ids(similar_ids)

    return list(map(lambda x: dict({
        'song_id': x['song_id'],
        'from_time': x['time_from'],
        'to_time': x['time_to'],
        'dist': x['dist'],
    }), similar))

# TMP
def load_files(songs):
    segments = []
    for song in songs:
        segments.append(load_song(song))
    return flatten(segments)


def find_matches(s):
    searchSegment, query_object = s

    return query_object.find_k_nearest_neighbors(searchSegment[3], MATCHES)


def analyze_songs(songs):

    fileChunks = []

    x = len(songs) // cpu_count() + 1
    for i in range(0, cpu_count()):
        fileChunks.append(songs[i * x: (i+1) * x])

    p = Pool(cpu_count())

    segments = p.map(load_files, fileChunks)

    p.close()

    segs = flatten(segments)

    ss = SongSegment()

    count = ss.count()

    # TODO: Rename
    m = list(map(lambda x: [], segs))

    for i in range(0, count // BUCKET_SIZE + 1):
        established_segments = list(
            map(process_db_segment, ss.get_all_in_range(i*BUCKET_SIZE, (i+1)*BUCKET_SIZE)))

        data = np.array(list(map(lambda x: x[3], established_segments)))

        bucket = create_bucket(data)

        query_object = bucket[1].construct_query_pool()
        query_object.set_num_probes(25)

        p = Pool(cpu_count())

        matches = list(map(find_matches, list(
            map(lambda seg: (seg, query_object), segs))))

        for j in range(0, len(matches)):

            m[j].append(
                list(map(lambda x: established_segments[x], matches[j])))

        p.close()

    for i in range(0, len(segs)):
        best = find_best(flatten(m[i]), segs[i])

        formatted = []
        for match in best:
            formatted.append(dict({
                'id': match[0][0],
                'distance': match[1]
            }))

        ss.update_similar(segs[i][0], formatted)
