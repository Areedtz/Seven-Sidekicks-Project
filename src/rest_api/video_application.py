import sys
import os
import json
import _thread
from bson.json_util import dumps

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

from database.video_emotion import VideoEmotion
from database.video_emotion_no_song import VideoEmotionNS
from utilities.config_loader import load_config
from video_emotion.api_helper import process_data_and_extract_emotions, process_data_and_extract_emotions_with_song


cfg = load_config()

app = Flask(__name__)
api = Api(app)

hostURL = cfg['rest_api_url']
hostPort = cfg['rest_api_port']
output_directory_for_commands = "./"

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
                "The given source path '{}' does not seem to exist"
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
                "The given source path '{}' does not seem to exist"
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
