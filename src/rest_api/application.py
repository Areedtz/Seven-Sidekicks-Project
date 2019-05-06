#!/usr/local/bin/python3.6

import sys
import os
import json
import _thread
from bson.json_util import dumps

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

import bpm.bpm_extractor as bpm_extract
import classification.api_helper as mood_extract
import classification.api_helper as music_emotion_classifier
from video_emotion.api_helper import process_data_and_extract_emotions, process_data_and_extract_emotions_with_song
from utilities.get_song_id import get_song_id
from utilities.config_loader import load_config
from database.track_emotion import TrackEmotion
from similarity.similarity import analyze_songs, query_similar
from database.video_emotion import VideoEmotion
from database.video_emotion_no_song import VideoEmotionNS


cfg = load_config()

app = Flask(__name__)
api = Api(app)

hostURL = cfg['rest_api_url']
hostPort = cfg['rest_api_port']
output_directory_for_commands = "./"


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
        description='The beginning time of the content to analyze',
        required=True),
    'To': fields.Integer(
        description='The end time of the content to analyze',
        required=True),
})

video_fields_with_song = api.model('VideoModelWithSong', {
    'ID': fields.String(
        description='The ID of the video to analyze',
        required=True),
    'SongID': fields.String(
        description='The ID of the song in the video',
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

song_model = api.model('SongModel', {
    'ID': fields.Nested(
        id_model,
        description='ID model of the song to analyze',
        required=True),
    'Filepath': fields.String(
        description='Filepath of the requested resource',
        required=True),
})

similarity_analysis_model = api.model('SimilarityAnalysisModel', {
                                      'songs': fields.List(fields.Nested(song_model))})

song_id_field = api.model('SongIdField', {
    'SongID': fields.String(
        description='The ID of the song in the video',
        required=True),
})


@api.route('/audio')
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
                song_path
            )
        )

        return {'Response': 'The request has been sent and'
                            ' should be updated in Splunk as soon as it is done.'}, 201


@api.route('/audio/<string:diskotek_nr>')
class AnalyzeSongGet(Resource):
    def get(self, diskotek_nr):
        db = TrackEmotion()

        r = db.get(diskotek_nr)

        if r is None:
            api.abort(
                400,
                "The given no. '{}' does not seem to exist"
                .format(diskotek_nr)
            )

        del r['_id']
        r['last_updated'] = r['last_updated'].isoformat()

        return r


@api.route('/video')
class AnalyzeVideo(Resource):
    @api.expect(video_fields)
    def post(self):
        data = request.get_json()

        video_id = data['ID']
        video_path = data['SourcePath']
        video_time_range = data['TimeRange']

        if video_time_range["From"] == video_time_range["To"]:
            api.abort(
                400,
                "From and to can not be equal"
            )

        if not os.path.isfile(video_path):
            api.abort(
                400,
                "The given filepath '{}' does not seem to exist"
                .format(video_path)
            )

        _thread.start_new_thread(
            process_data_and_extract_emotions,
            (
                video_id,
                video_path,
                video_time_range
            )
        )

        return {'Response': 'The request has been sent and should be'
                            ' updated in Splunk as soon as it is done.'}, 201


@api.route('/video/<string:video_id>')
class AnalyzeVideoGet(Resource):
    def get(self, video_id):
        db = VideoEmotionNS()
        result = db.get_by_video_id(video_id)

        if result is None:
            api.abort(
                400,
                "The given no. '{}' does not seem to exist"
                .format(video_id)
            )

        return result


@api.route('/video_with_audio')
class AnalyzeVideoWithSong(Resource):
    @api.expect(video_fields_with_song)
    def post(self):
        data = request.get_json()

        video_id = data['ID']
        song_id = data['SongID']
        video_path = data['SourcePath']
        video_time_range = data['TimeRange']

        if video_time_range["From"] == video_time_range["To"]:
            api.abort(
                400,
                "From and to can not be equal"
            )

        if not os.path.isfile(video_path):
            api.abort(
                400,
                "The given filepath '{}' does not seem to exist"
                .format(video_path)
            )

        _thread.start_new_thread(
            process_data_and_extract_emotions_with_song,
            (
                video_id,
                video_path,
                video_time_range,
                song_id
            )
        )

        return {'Response': 'The request has been sent and should be'
                            ' updated in Splunk as soon as it is done.'}


@api.route('/similarity')
class AnalyzeSimilarity(Resource):
    @api.expect(similarity_analysis_model)
    def post(self):

        data = request.get_json()

        transformed = list(map(lambda a: ('{}-{}-{}'.format(
            a["ID"]["Release"], a["ID"]["Side"],
            a["ID"]["Track"]
        ), a['Filepath']), data['songs']))

        _thread.start_new_thread(analyze_songs, (transformed, ))

        return {'message': 'Updating similarity with new songs'}


@api.route('/similar/<string:diskotek_nr>/<int:from_time>/<int:to_time>')
class Similar(Resource):
    @api.expect(timerange_model)
    def get(self, diskotek_nr, from_time, to_time):
        similar = query_similar(diskotek_nr, from_time, to_time)

        if similar == None:
            # Should be 404, but restplus inserts additional text
            api.abort(400, 'No similar songs found')

        return similar


@api.route('/video_with_audio/<string:song_id>')
class AnalyzeVideoWithSongGet(Resource):
    def get(self, song_id):
        db = VideoEmotion()
        result = db.get_by_song_id(song_id)

        if result is None:
            api.abort(
                400,
                "The given no. '{}' does not seem to exist"
                .format(song_id)
            )

        return result
