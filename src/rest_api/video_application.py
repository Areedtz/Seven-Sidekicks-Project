import os
import json
import _thread

from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

from utilities.config_loader import load_config
from video_emotion.api_helper import process_data_and_extract_emotions, \
    process_data_and_extract_emotions_with_song


cfg = load_config()

app = Flask(__name__)
api = Api(app)

"""
    Models the time-range of a video input
"""
timerange_model = api.model('TimeRange_Model', {
    'from': fields.Integer(
        description='The beginning time of the ' +
        'content to analyze in milliseconds',
        required=True),
    'to': fields.Integer(
        description='The end time of the content to analyze milliseconds',
        required=True),
})

"""
    Models a request for analyzing a video and song in
    conjunction so that their data can be collated
"""
video_fields_with_song = api.model('VideoModelWithSong', {
    'id': fields.String(
        description='The ID of the video to analyze',
        required=True),
    'song_id': fields.String(
        description='The ID of the song in the video',
        required=True),
    'time_range': fields.Nested(
        timerange_model,
        description='The model for the time range analyzed by the program'),
    'source_path': fields.String(
        description='The path of the video to analyze',
        required=True),
    'user': fields.String(
        description='The requesting user',
        required=True),
})

"""
    Models a request for analyzing a video
"""
video_fields = api.model('VideoModel', {
    'id': fields.String(
        description='The ID of the video to analyze',
        required=True),
    'time_range': fields.Nested(
        timerange_model,
        description='The model for the time range analyzed by the program'),
    'source_path': fields.String(
        description='The path of the video to analyze',
        required=True),
    'user': fields.String(
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

        video_id = data['id']
        video_path = data['source_path']
        video_time_range = data['time_range']

        check_if_invalid_time_range(video_time_range)

        check_if_none(video_path)

        _thread.start_new_thread(
            process_data_and_extract_emotions,
            (
                video_id,
                video_path,
                video_time_range
            )
        )

        return {'Response': 'The request is being processed and will be' +
                'available in the database when done.'}


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

        video_id = data['id']
        song_id = data['song_id']
        video_path = data['source_path']
        video_time_range = data['time_range']

        check_if_invalid_time_range(video_time_range)

        check_if_none(video_path)

        _thread.start_new_thread(
            process_data_and_extract_emotions_with_song,
            (
                video_id,
                video_path,
                video_time_range,
                song_id
            )
        )

        return {'Response': 'The request is being processed and will be' +
                'available in the database when done.'}



def check_if_invalid_time_range(video_time_range):
    if video_time_range["from"] == video_time_range["to"]:
        api.abort(
            400,
            "From and to can not be equal"
        )
    return


def check_if_none(video_path):
    if not os.path.isfile(video_path):
        api.abort(
            400,
            "The given source path '{}' does not seem to exist"
            .format(video_path)
        )
    return
