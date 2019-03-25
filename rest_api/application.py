import sys
import os
import json

# Start of importing the utilities module
#sys.path.insert(0, os.path.abspath("../"))
#import bpm.bpm_extractor as bpm_extractor

# End of importing the utilities module

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, reqparse, fields
from pathlib import PurePath
from json import JSONDecoder

app = Flask(__name__)
api = Api(app)

# We need to find the right way to set a custom json decoder
# the proper way. That shit below is improper
app.json_decoder = json.loads

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
        a = request.get_json()
        return 'a'
        
@api.route('/shutdown')
class Shutdown(Resource):
    def get(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    
if __name__ == '__main__':
    app.run(host=hostURL, port=hostPort, debug=True)