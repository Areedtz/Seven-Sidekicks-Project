#!/usr/local/bin/python3.6

import sys
import os
import json
import _thread

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

import classification.api_helper as mood_extract
import bpm.bpm_extractor as bpm_extract
import classification.api_helper as music_emotion_classifier
import video_emotion.api_helper as video_emotion_classifier
from utilities.get_song_id import get_song_id
from utilities.config_loader import load_config

cfg = load_config()

app = Flask(__name__)
api = Api(app)

hostURL = cfg['rest_api_url']
hostPort = cfg['rest_api_port']
output_directory_for_commands = "./"


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# Model is nested inside the song_fields model
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


timerange_model = api.model('TimeRange_Model', {
    'From': fields.Integer(
        description='The beginning time of the video to analyze',
        required=True),
    'To': fields.Integer(
        description='The end time of the video to analyze',
        required=True),
})


video_fields = api.model('VideoModel', {
    'ID': fields.String(
        description='The ID of the video to analyze',
        required=True),
    'TimeRange': fields.Nested(
        timerange_model,
        description='The model for the time range analyzed by the program'),
    'SourcePath': fields.String(
        description='The path of the video to analyze',
        required=True),
    'User': fields.String(
        description='The requesting user',
        required=True),
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

        song_path = data["SourcePath"]
        if not os.path.isfile(song_path):
            api.abort(
                400,
                "The given filepath '{}' does not seem to exist"
                .format(song_path)
            )

        _thread.start_new_thread(
            music_emotion_classifier.process_data_and_extract_profiles,
            (
                song_id,
                song_path,
                output_directory_for_commands
            )
        )
        return {'Response': 'The request has been sent and should be updated in Splunk as soon as it is done.'}


@api.route('/analyze_video')
class AnalyzeSong(Resource):
    @api.expect(video_fields)
    def post(self):
        data = request.get_json()

        video_id = data['ID']
        video_path = data['SourcePath']
        video_time_range = data['TimeRange']
        
        if not os.path.isfile(video_path):
            api.abort(
                400,
                "The given filepath '{}' does not seem to exist"
                .format(video_path)
            )


        _thread.start_new_thread(
            video_emotion_classifier.process_data_and_extract_emotions,
            (
                video_id,
                video_path,
                video_time_range,
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

