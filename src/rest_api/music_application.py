import sys
import os
import json
import _thread
from bson.json_util import dumps

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

import classification.api_helper as music_emotion_classifier
from utilities.config_loader import load_config


cfg = load_config()

app = Flask(__name__)
api = Api(app)

hostURL = cfg['rest_api_url']
hostPort = cfg['rest_api_port']
output_directory_for_commands = "./"

"""
    Models the id of a piece of music
"""
id_model = api.model('IdModel', {
    'Release': fields.Integer(
        description='The release ID of the song',
        required=True),
    'Side': fields.Integer(
        description='The side of the media',
        required=True),
    'Track': fields.Integer(
        description='The tracknumber of the media',
        required=True),
})

"""
    Models an analysis request for a piece of music including its location and the user requesting the analysis
"""
song_fields = api.model('SongModel', {
    'ID': fields.Nested(
        id_model,
        description='ID model of the song to analyze',
        required=False),
    'SourcePath': fields.String(
        description='The path of the song to analyze',
        required=True),
    'User': fields.String(
        description='The requesting user',
        required=True),
})


@api.route('/audio')
class AnalyzeSong(Resource):
    @api.expect(song_fields)
    def post(self) -> str:
        """Analyzes a song and outputs the data to the database
        """

        data = request.get_json()
        song_id = '{}-{}-{}'.format(
            data["ID"]["Release"], data["ID"]["Side"],
            data["ID"]["Track"]
        )

        song_path = data["SourcePath"]
        if not os.path.isfile(song_path):
            api.abort(
                400,
                "The given source path '{}' does not seem to exist"
                .format(song_path)
            )

        _thread.start_new_thread(
            music_emotion_classifier.process_data_and_extract_profiles,
            (
                song_id,
                song_path
            )
        )

        return {'Response': 'The request has been sent and'
                            ' should be updated in Splunk as soon as it is done.'}, 201
