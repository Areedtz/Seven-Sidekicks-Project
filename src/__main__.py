#!/usr/local/bin/python3.6

import sys
import os
import json
from multiprocessing import Pool

from bpm.bpm_extractor import get_song_bpm
from classification.extractor.low_level_data_extractor import make_low_level_data_file
from classification.classifier.profile_data_extractor import get_classifier_data
from video_emotion.extract_classifier import classify_video
from database.track_bpm import TrackBPM
from database.track_party import TrackParty
from database.track_relaxed import TrackRelaxed
from database.track_timbre import TrackTimbre
from rest_api.application import app, hostURL, hostPort


if __name__ == "__main__":
    app.run(host=hostURL, port=hostPort, debug=True)