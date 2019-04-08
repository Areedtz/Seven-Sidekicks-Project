import sys
import os
import json

# Importing the BPM module
sys.path.insert(0, os.path.abspath("../bpm/"))
import bpm_extractor as bpm_extract

# Importing the classification module
sys.path.insert(0, os.path.abspath("../classification"))
import main as mood_extract


from flask import Flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields
from pathlib import PurePath
from flask.json import JSONEncoder, JSONDecoder

app = Flask(__name__)
api = Api(app)

# We need to find the right way to set a custom json decoder
# the proper way. That shit below is improper

hostURL = "0.0.0.0"
hostPort = 1337
apiRoute = '/hello'


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

    @api.doc(body=song_fields)
    def post(self):
        # ../utilities/ressources/music/77245-1-1_Charles-Aznavour_Yesterday-when-i-was-young.wav
        retdict = {}    
        a = request.get_json()
        #song_id, song_bpm, confidence = bpm_extract.get_song_bpm(a["SourcePath"])
        #retdict["song_id"] = song_id
        #retdict["song_bpm"] = song_bpm
        #retdict["confidence"] = confidence
        #ree = mood_extract.get_classifier_data(a["SourcePath"])s
        #print("------------------------------------------------------")
        #mood_extract.process_data_and_extract_profiles(
        #    "77245-1-1",
        #    "../utilities/ressources/music/77245-1-1_Charles-Aznavour_Yesterday-when-i-was-young.wav",
        #    "yikes.json")
        #ree = mood_extract.get_classifier_data("../utilities/ressources/music/77245-1-1_Charles-Aznavour_Yesterday-when-i-was-young.wav")
        
        return request.get_json() # {'Response': 'The request has been sent and should be updated in Splunk as soon as it is done.'}


@api.route('/shutdown')
class Shutdown(Resource):
    def get(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()


if __name__ == '__main__':
    app.run(host=hostURL, port=hostPort, debug=True)