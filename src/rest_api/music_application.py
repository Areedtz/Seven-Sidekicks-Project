import sys
import os
import json
import _thread
from bson.json_util import dumps

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields
from celery import chain

from tasks import check_done, add_bpm, add_emotions, add_metering, add_similarity_features, save_to_db
import classification.api_helper as music_emotion_classifier
from utilities.config_loader import load_config
from utilities.get_song_id import get_song_id


cfg = load_config()

app = Flask(__name__)
api = Api(app)


"""
    Models an analysis request for a piece of music including its location
"""
song_fields = api.model('SongModel', {
    'SourcePath': fields.String(
        description='The path of the song to analyze',
        required=True),
    'Force': fields.String(
        description='Should every analysis run',
        required=False)
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
            if song_path.endswith(("mp3", "wav")):
                id = get_song_id(song_path)
                song = dict({
                    'audio_id': id,
                    'source_path': song_path,
                    'FORCE': data['Force'],
                })

                s = chain(
                    check_done.s(),
                    add_bpm.s(),
                    add_emotions.s(),
                    add_metering.s(),
                    add_similarity_features.s(),
                    save_to_db.s()
                )

                s.delay(song)
        else:  # Is folder
            for file in os.listdir(song_path):
                if file.endswith(("mp3", "wav")):
                    id = get_song_id(file)
                    song = dict({
                        'audio_id': id,
                        'source_path': file,
                        'FORCE': data['Force'],
                    })

                    s = chain(
                        check_done.s(),
                        add_bpm.s(),
                        add_emotions.s(),
                        add_metering.s(),
                        add_similarity_features.s(),
                        save_to_db.s()
                    )

                    s.delay(song)

        return {'Response': 'The request has been received and this API does nothing atm'}, 201
