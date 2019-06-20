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
            # Do something
            print("Got request for the " + song_path + " file")
        else:  # Is folder
            # Do something else
            print("Got request for the " + song_path + " folder")

        return {'Response': 'The request has been received and this API does nothing atm'}, 201
