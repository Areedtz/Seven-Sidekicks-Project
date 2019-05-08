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

"""
    Models the time-range of a video input
"""
timerange_model = api.model('TimeRange_Model', {
    'From': fields.Integer(
        description='The beginning time of the content to analyze in milliseconds',
        required=True),
    'To': fields.Integer(
        description='The end time of the content to analyze milliseconds',
        required=True),
})

"""
    Models a request for analyzing a video and song in conjunction so that their data can be collated
"""
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

"""
    Models a request for analyzing a video
"""
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


@api.route('/get_analyzed_song/<string:diskotek_nr>')
class GetAnalyzeSong(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed songs data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the information of the analyzed song
        """

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
    def post(self) -> object:
        """Analyzes a video and outputs the data to the database

        Returns
        -------
        object
            A dummy json response to confirm that the analysis has begun
        """

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
    def get(self, video_id: str) -> object:
        """Retrieves a previously analyzed songs data from the database

        Parameters
        ----------
        video_id : str
            The ID of the the video to analyze

        Returns
        -------
        object
            A json object of the information of the the analyzed video
        """

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
    def post(self) -> object:
        """Analyzes a video together with a song and outputs the data to the database

        Returns
        -------
        object
            A dummy json response to confirm that the analysis has begun
        """

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
    def post(self) -> object:
        """Analyzes the similarity of a song

        Returns
        -------
        object
            A dummy json response to confirm that the analysis has begun
        """

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
    def get(self, diskotek_nr: str, from_time: int, to_time: int) -> object:
        """Retrieves a previously analyzed songs similarity data from the database

        Parameters
        ----------
        diskotek_nr : str
            The diskotek ID of the song to analyze
        from_time : int
            The start time of the similarity value to get, in milliseconds
        to_time: int
            The end time of the similarity value to get, in milliseconds

        Returns
        -------
        object
            A json object of the information of the similarity analyzed song
        """

        similar = query_similar(diskotek_nr, from_time, to_time)

        if similar == None:
            # Should be 404, but restplus inserts additional text
            api.abort(400, 'No similar songs found')

        return similar


@api.route('/video_with_audio/<string:song_id>')
class AnalyzeVideoWithSongGet(Resource):
    def get(self, song_id: str) -> object:
        """Retrieves a previously analyzed song+video from the database

        Parameters
        ----------
        song_id : str
            The ID of the song to get song+video data for

        Returns
        -------
        object
            A json object of the information of the analyzed song+video
        """

        db = VideoEmotion()
        result = db.get_by_song_id(song_id)

        if result is None:
            api.abort(
                400,
                "The given no. '{}' does not seem to exist"
                .format(song_id)
            )

        return result
