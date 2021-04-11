import os
import json
import datetime

import requests
from flask import Flask
from flask import request
from flask_restplus import Resource, Api, fields

from database.sql.audio import AudioDB
from database.mongo.video.video_emotion import VideoEmotion
from database.mongo.video.video_emotion_no_song import VideoEmotionNS
from similarity.similarity import query_similar
from utilities.config_loader import load_config

cfg = load_config()

app = Flask(__name__)
api = Api(app)

"""
    Models an analysis request for a piece of music including its location
"""
song_fields = api.model('SongModel', {
    'mediesek_id': fields.String(
        description='',
        required=True),
    'source_path': fields.String(
        description='The path of the song to analyze',
        required=True),
    'force': fields.Boolean(
        description='Should every analysis run'),
    'config': fields.Raw(
        description='Config parameters for the analysis')
})

"""
    Models the time-range of a video input
"""
timerange_model = api.model('TimeRange_Model', {
    'from': fields.Integer(
        description=('The beginning time of the content' +
                     'to analyze in milliseconds'),
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


@api.route('/audio')
class AnalyzeSong(Resource):
    @api.expect(song_fields)
    def post(self) -> str:
        """Validates the request and forwards it to the audio API
        """

        req_data = request.get_json()
        song_path = req_data["source_path"]

        if not (os.path.isfile(song_path)):
            if os.path.isdir(song_path):
            api.abort(
                400,
                    "The given path {} is a folder and not a file"
                    .format(song_path)
                )
            else:
                api.abort(
                    400,
                    "The given file {} can not be found"
                .format(song_path)
            )

        resp = requests.post(
            cfg['rest_api_music_url'] + "/audio", json=req_data)

        return resp.json(), resp.status_code


@api.route('/audio/<string:diskotek_nr>')
class GetAnalyzedSong(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_all(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/rhythm/<string:diskotek_nr>')
class GetAnalyzedSongRhythm(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's rhythm data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the rhythm
            information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_rhythm(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/rhythm/bpm/<string:diskotek_nr>')
class GetAnalyzedSongBPM(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's BPM data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the BPM information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_bpm(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/timbre/<string:diskotek_nr>')
class GetAnalyzedSongTimbre(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's timbre data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the timbre
            information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_timbre(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/emotions/<string:diskotek_nr>')
class GetAnalyzedSongEmotions(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's emotion data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the emotion
            information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_emotions(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/emotions/relaxed/<string:diskotek_nr>')
class GetAnalyzedSongEmotionsRelaxed(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's relaxed data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the relaxed
            information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_relaxed(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/emotions/party/<string:diskotek_nr>')
class GetAnalyzedSongEmotionsParty(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's party data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the party information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_party(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/emotions/aggressive/<string:diskotek_nr>')
class GetAnalyzedSongEmotionsAggressive(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's aggressive data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the aggressive
            information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_aggressive(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/emotions/happy/<string:diskotek_nr>')
class GetAnalyzedSongEmotionsHappy(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's happy data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the happy information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_happy(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/emotions/sad/<string:diskotek_nr>')
class GetAnalyzedSongEmotionsSad(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's sad data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the sad information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_sad(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/levels/<string:diskotek_nr>')
class GetAnalyzedSongMeter(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's levels data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the levels
            information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_level(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/levels/peak/<string:diskotek_nr>')
class GetAnalyzedSongMeterPeak(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's peak data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the peak information of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_peak(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/levels/loudness_integrated/<string:diskotek_nr>')
class GetAnalyzedSongMeterLoudnessIntegrated(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's loudness
           integrated data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the loudness
            integrated of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_loudness_integrated(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/audio/levels/loudness_range/<string:diskotek_nr>')
class GetAnalyzedSongMeterLoudnessRange(Resource):
    def get(self, diskotek_nr: str) -> object:
        """Retrieves a previously analyzed song's
           loudness range data from the database

        Parameters
        ----------
        diskotek_nr : str
            The ID of the the song to retrieve

        Returns
        -------
        object
            A json object containing the peak
            loudness range of the analyzed song
        """

        db_connection = AudioDB()

        result = db_connection.get_loudness_range(diskotek_nr)

        check_if_none(result, diskotek_nr)

        return result


@api.route('/video')
class AnalyzeVideo(Resource):
    @api.expect(video_fields)
    def post(self) -> object:
        """Validates the request and forwards it to the video API

        Returns
        -------
        object
            A json response to confirm that the analysis has begun
        """

        data = request.get_json()

        video_path = data['source_path']
        video_time_range = data['time_range']

        if video_time_range["from"] == video_time_range["to"]:
            api.abort(
                400,
                "From and to can not be equal"
            )

        if not (os.path.isfile(video_path) or os.path.isdir(video_path)):
            api.abort(
                400,
                "The given source path '{}' does not seem to exist"
                .format(video_path)
            )

        resp = requests.post(
            cfg['rest_api_video_url'] + "/video", json=data)

        return resp.json(), resp.status_code


@api.route('/video/<string:video_id>')
class GetAnalyzedVideo(Resource):
    def get(self, video_id: str) -> object:
        """Retrieves a previously analyzed song's data from the database

        Parameters
        ----------
        video_id : str
            The ID of the the video to analyze

        Returns
        -------
        object
            A json object of the information of the the analyzed video
        """

        db_connection = VideoEmotionNS()
        result = db_connection.get_by_video_id(video_id)

        if result is None:
            api.abort(
                400,
                "The given id '{}' does not seem to exist"
                .format(video_id)
            )

        return result


@api.route('/video_with_audio')
class AnalyzeVideoWithSong(Resource):
    @api.expect(video_fields_with_song)
    def post(self) -> object:
        """Validates the request and forwards it to the video API

        Returns
        -------
        object
            A json response to confirm that the analysis has begun
        """

        data = request.get_json()

        video_path = data['source_path']
        video_time_range = data['time_range']

        if video_time_range["from"] == video_time_range["to"]:
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

        resp = requests.post(
            cfg['rest_api_video_url'] + "/video_with_audio", json=data)

        return resp.json(), resp.status_code


@api.route('/video_with_audio/<string:song_id>')
class GetAnalyzedVideoWithSong(Resource):
    def get(self, song_id: str) -> object:
        """Retrieves a previously analyzed song's + video's data from the database

        Parameters
        ----------
        song_id : str
            The ID of the song to get song + video data for

        Returns
        -------
        object
            A json object of the information of the analyzed song + video
        """

        db_connection = VideoEmotion()
        result = db_connection.get_by_song_id(song_id)

        if result is None:
            api.abort(
                400,
                "The given id '{}' does not seem to exist"
                .format(song_id)
            )

        return result


@api.route('/similarity/<string:diskotek_nr>/<int:from_time>/<int:to_time>')
class Similar(Resource):
    def get(self, diskotek_nr: str, from_time: int, to_time: int) -> object:
        """Retrieves a previously analyzed song's similarity data from the database

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

        if similar is None:
            # Should be 404, but restplus inserts additional text
            api.abort(400, 'No similar songs found')

        return similar


def check_if_none(result, diskotek_nr):
    if result is None:
        api.abort(
            400,
            "The given id '{}' does not seem to exist"
            .format(diskotek_nr)
        )
    return


def format_date(result):
    date = datetime.datetime.strptime(
            result['Last_Updated'], '%Y-%m-%dT%H:%M:%S')
    result['Last_Updated'] = date.isoformat()
    
    return result
