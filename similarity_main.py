from similarity.similarity import process_segment
from database.segment_features import SegmentFeatures
from database.song_seg import SSegmentation
from utilities.get_song_id import get_song_id
from bson.objectid import ObjectId
import librosa
import os

FOLDER = 'music_small'

filenames = []

for root, dirs, files in os.walk("./" + FOLDER):
    for filename in files:
        if filename.endswith('.wav'):
            print(filename)
            filenames.append(filename)

# Load features
segments = SSegmentation()

sf = SegmentFeatures()

for filename in filenames:
    print(filename)

    song_id = get_song_id(filename)

    segs = segments.get_all_with_id(song_id)

    if (segs == []):
        y, sr = librosa.load('./' + FOLDER + '/' + filename)

        for i in range(0, y.shape[0]//sr//5 - 1):
            _id = segments.add(song_id, i*5*1000, (i+1)*5*1000)

            sample = y[(i * sr * 5):
                       ((i + 1) * sr * 5)]

            mfcc, chromagram, tempogram = process_segment(sample, sr)

            print(mfcc.shape)
            print(chromagram.shape)
            print(tempogram.shape)

            sf = SegmentFeatures()

            sf.add(_id, mfcc.tobytes(),
                   chromagram.tobytes(), tempogram.tobytes())
    else:
        for segment in segs:
            print(segment)
            print(segment['_id'])

            f = sf.get(segment['_id'])
            print(f)

segments.close()
sf.close()
