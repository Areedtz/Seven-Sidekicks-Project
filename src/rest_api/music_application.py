import os
import json

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

import classification.api_helper as music_emotion_classifier
# Some linting can show this as not being imported
from celery import chain

from tasks import check_done, add_bpm, add_emotions, add_metering, \
    add_similarity_features, save_to_db
from utilities.config_loader import load_config


cfg = load_config()

app = Flask(__name__)
api = Api(app)


"""
    Models an analysis request for a piece of music including its location
"""
song_fields = api.model('SongModel', {
    'SourcePath': fields.String(
        description='The path of the song to analyze',
        required=True)
})


@api.route('/audio')
class AnalyzeSong(Resource):
    @api.expect(song_fields)
    def post(self) -> str:
        """Analyzes a song and outputs the data to the database
        """

        data = request.get_json()
        song_path = data["SourcePath"]

        if os.path.isfile(song_path):
            # if song_path.endswith(("mp3", "wav")):
                # Send to pipeline
            print("Got request for the " + song_path + " file")
        else:  # Is folder
            for _ in os.listdir(song_path):
                add_to_pipeline(data, song_path)

        return {'Response': 'The song has been added to the pipeline' +
                'and will be available once analyzed'}, 201
