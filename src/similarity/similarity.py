import os
import fileinput
from multiprocessing import Pool, Process, Queue, cpu_count, Manager

import librosa
from scipy.spatial import distance
import numpy as np
import falconn

from database.song_segment import SongSegment
from utilities.config_loader import load_config
from utilities.filehandler.handle_path import get_absolute_path

cfg = load_config()
MATCHES = cfg['similarity_matches']
BUCKET_SIZE = cfg['similarity_bucket_size']


def _flatten(l): 
    """ Creates an array from
    an array of arrays
    """

    return [item for sublist in l for item in sublist]


def _process_segment(segment, sr):
    """ Computes the features from
    a song segment
    """
    harmonic, percussive = librosa.effects.hpss(segment)

    tempogram = librosa.feature.tempogram(
        percussive, hop_length=1024, win_length=16)

    mfcc = librosa.feature.mfcc(segment, hop_length=1024)

    chromagram = librosa.feature.chroma_cqt(y=harmonic, sr=sr, hop_length=1024)

    return mfcc, chromagram, tempogram


def _load_songs(songs):
    """ A wrapper around _load_song that
    allows for multiple songs to be looked
    up using the same database connection
    """
    seg_db = SongSegment()
    segments = []
    for song in songs:
        song_id, filename = song
        segments.append(_load_song(song_id, filename, seg_db))
    seg_db.close()
    return _flatten(segments)


def _load_song(song_id, filename, segments):
    """ Loads song features from the database if
    available otherwise loading the file and
    loading features from it directly
    """
    filename = get_absolute_path(filename)
    segs = segments.get_all_by_song_id(song_id)

    segment_data = []

    if (segs == []):
        # No segments in db, which means no features in db
        y, sr = librosa.load(filename)

        for i in range(0, y.shape[0]//sr//5 - 1):

            sample = y[(i * sr * 5):
                       ((i + 1) * sr * 5)]

            mfcc, chromagram, tempogram = _process_segment(sample, sr)

            _id = segments.add(song_id, i*5*1000, (i+1)*5*1000, mfcc.tobytes(),
                               chromagram.tobytes(), tempogram.tobytes(), [])

            feature = _create_feature(mfcc, chromagram, tempogram)

            segment_data.append((_id, song_id, i*5, feature))

    else:
        # There are segments in db, look for features
        for i in range(0, len(segs)):
            segment = segs[i]

            if segment['mfcc'] == None or segment['chroma'] == None or segment['tempogram'] == None:
                break

            feature = _create_feature(np.frombuffer(segment['mfcc']), np.frombuffer(
                segment['chroma']), np.frombuffer(segment['tempogram']))

            segment_data.append((segment['_id'], song_id, i*5, feature))

    return segment_data


def _process_db_segment(segment):
    """ Processes a db segment to the format
    used by the module
    """
    feature = _create_feature(np.frombuffer(segment['mfcc']), np.frombuffer(
        segment['chroma']), np.frombuffer(segment['tempogram']))

    return (segment['_id'], segment['song_id'], segment['time_from'] // 1000, feature)


def _create_feature(mfcc, chroma, tempogram):
    """ Creates a single feature vector from
    the three individual features
    """
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


def _create_bucket(segments):
    """ Creates a bucket of segments
    to use for LSH similarity lookup
    """
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


def _dist(seg1, seg2):
    """ Finds the distance between
    two segments
    """
    return distance.euclidean(seg1[3], seg2[3])


def _find_best_matches(matches, segment):
    """ Finds the best n matches
    out of all matches, where n is
    the MATCHES variable
    """

    lows = []
    for i in range(0, len(matches)):
        distance = _dist(
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
    """Queries the database for segments
    similar to the segment provided

    Parameters
    ----------
    song_id : string
        Id of the given song
    from_time : int
        The start time of the segment
    to_time : int
        The end time of the segment

    Returns
    -------
    list of Dict[song_id : string, from_time: time_from, to_time: time_to]
        A list of all the segments which are similar
    """

    seg_db = SongSegment()
    segments = seg_db.get_all_by_song_id(song_id)

    best = None
    for segment in segments:
        localdist = abs(from_time - segment['time_from'])
        if best == None or localdist < best[0]:
            best = (localdist, segment)

    if best == None or 'similar' not in best[1]:
        return None

    segment = best[1]

    similar = segment['similar']

    similar_ids = list(map(lambda sim: sim['id'], similar))

    similar_full = seg_db.get_by_ids(similar_ids)

    similar_segments = []
    for i in range(0, len(similar)):
        sim_seg = next(seg for seg in similar_full if seg['_id'] == similar[i]['id'])
        similar_segments.append(dict({
            'song_id': sim_seg['song_id'],
            'from_time': sim_seg['time_from'],
            'to_time': sim_seg['time_to'],
            'distance': similar[i]['distance'],
        }))

    seg_db.close()

    return similar_segments


def _find_matches(searchContext):
    """ Searches for segments that
    are similar in the bucket
    """
    
    searchSegment, query_object = searchContext

    return query_object.find_k_nearest_neighbors(searchSegment[3], MATCHES)


def analyze_songs(songs):
    """Analyzes the specified songs
    and adds their features and similar
    to the database

    Parameters
    ----------
    songs : list of Tuple[song_id: string, filepath: string]
        The songs that need to be analyzed, containing song_id and filepath

    """

    fileChunks = []
    x = len(songs) // cpu_count() + 1
    for i in range(0, cpu_count()):
        fileChunks.append(songs[i * x: (i+1) * x])

    p = Pool(cpu_count())
    segments = p.map(_load_songs, fileChunks)
    p.close()

    segs = _flatten(segments)

    ss = SongSegment()

    count = ss.count()

    allMatches = list(map(lambda x: [], segs))

    for i in range(0, count // BUCKET_SIZE + 1):
        established_segments = list(filter( lambda x:
            x['mfcc'] != None and
            x['chroma'] != None and
            x['tempogram'] != None,
            ss.get_all_in_range(i*BUCKET_SIZE, (i+1)*BUCKET_SIZE)))
        established_segments = list(
            map(_process_db_segment, established_segments))

        data = np.array(list(map(lambda x: x[3], established_segments)))

        bucket = _create_bucket(data)

        query_object = bucket[1].construct_query_pool()
        query_object.set_num_probes(25)

        p = Pool(cpu_count())

        matches = list(map(_find_matches, list(
            map(lambda seg: (seg, query_object), segs))))

        for j in range(0, len(matches)):

            allMatches[j].append(
                list(map(lambda x: established_segments[x], matches[j])))

        p.close()

    for i in range(0, len(segs)):
        print(segs[i][1] + ": " + str(segs[i][2]))
        best = _find_best_matches(_flatten(allMatches[i]), segs[i])

        matches = ss.get_by_ids(list(map(lambda match: match[0][0], best)))
        matches = list(
            map(lambda match: (match['_id'], match['similar']), matches))

        for j in range(0, len(matches)):
            matches[j][1].append(dict({
                'id': segs[i][0],
                'distance': best[j][1],
            }))

            match_ids = list(set(map(lambda x: x['id'], matches[j][1])))
            innerMatches = list(map(lambda match_id: next(
                x for x in matches[j][1] if x['id'] == match_id), match_ids))
            innerMatches.sort(key=lambda m: m['distance'])
            ss.update_similar(matches[j][0], innerMatches[:10])

        formatted = []
        for match in best:
            formatted.append(dict({
                'id': match[0][0],
                'distance': match[1]
            }))

        ss.update_similar(segs[i][0], formatted)

    ss.close()
