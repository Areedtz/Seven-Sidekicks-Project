import sys
import os
import json
import _thread

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields

import bpm.bpm_extractor as bpm_extract
import classification.api_helper as mood_extract
from utilities.get_song_id import get_song_id

app = Flask(__name__)
api = Api(app)

hostURL = "0.0.0.0"
hostPort = 1337
apiRoute = '/hello'
output_directory_for_commands = "./"


@api.route(apiRoute)
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


# Model is nested inside the song_fields model
id_model = api.model('IdModel', {
    'Release': fields.Integer(description='The release ID of the song', required=True),
    'Side': fields.Integer(description='The side of the media', required=True),
    'Track': fields.Integer(description='The tracknumber of the media', required=True),
})

song_fields = api.model('SongModel', {
    'ID': fields.Nested(id_model, description='ID model of the song to analyze', required=False),
    'SourcePath': fields.String(description='The path of the song to analyze', required=True),
    'User': fields.String(description='The requesting user', required=True),
})


@api.route('/analyze_song')
class AnalyzeSong(Resource):
    @api.expect(song_fields)
    def post(self):
        data = request.get_json()
        song_id = '{}-{}-{}'.format(
            data["ID"]["Release"], data["ID"]["Side"],
            data["ID"]["Track"]
        )
        # ../utilities/ressources/music/77245-1-1_Charles-Aznavour_Yesterday-when-i-was-young.wav
        song_path = data["SourcePath"]
        if not os.path.isfile(song_path):
            api.abort(
                400,
                "The given filepath '{}' does not seem to exist"
                .format(song_path)
            )

        _thread.start_new_thread(
            mood_extract.process_data_and_extract_profiles,
            (
                song_id,
                song_path,
                output_directory_for_commands
            )
        )
        return {'Response': 'The request has been sent and should be updated in Splunk as soon as it is done.'}

@api.route('/shutdown')
class Shutdown(Resource):
    def get(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


if __name__ == '__main__':
    app.run(host=hostURL, port=hostPort, debug=True)