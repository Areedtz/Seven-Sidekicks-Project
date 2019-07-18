from typing import Dict
import json

from records import Database

from utilities.config_loader import load_config


class AudioDB:
    def __init__(self):
        cfg = load_config()

        self._db = Database("{}://{}:{}@{}/{}".format(
            cfg['sql_type'], cfg['sql_user'], cfg['sql_pass'], cfg['sql_host'], cfg['sql_db']))

    def _get_data(self, query, audio_id: str):
        ids = audio_id.split("-")

        if len(ids) != 3:
            return None

        rows = self._db.query(query, rel=ids[0], side=ids[1], track=ids[2])

        result = json.loads(rows.export("json"))

        if len(result) == 0:
            return None

        return result[0]

    def setup(self):
        self._db.query("""
        CREATE TABLE Audio
        (
            audio_release INT NOT NULL,
            audio_side INT NOT NULL,
            audio_track INT NOT NULL,
            bpm INT,
            bpm_confidence FLOAT,
            timbre VARCHAR(20),
            timbre_confidence FLOAT,
            relaxed VARCHAR(20),
            relaxed_confidence FLOAT,
            party VARCHAR(20),
            party_confidence FLOAT,
            aggressive VARCHAR(20),
            aggressive_confidence FLOAT,
            happy VARCHAR(20),
            happy_confidence FLOAT,
            sad VARCHAR(20),
            sad_confidence FLOAT,
            peak FLOAT,
            loudness_integrated FLOAT,
            loudness_range FLOAT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(audio_release, audio_side, audio_track)
        )""")

        # CREATE INDEXES

    def exists(self, audio_id: str) -> bool:
        """Check if an entry with the given audio id exists in the database

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        bool
            True if an entry exists, False otherwise
        """

        query = """
                SELECT audio_release
                FROM Audio
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return None != self._get_data(query, audio_id)

    def post_all(self, data: Dict) -> str:
        if not 'audio_id' in data:
            pass

        ids = data['audio_id'].split("-")

        if len(ids) != 3:
            return None

        query = """
        INSERT INTO Audio (
            audio_release, audio_side, audio_track,
            bpm, bpm_confidence, timbre,
            timbre_confidence, relaxed,
            relaxed_confidence, party,
            party_confidence, aggressive,
            aggressive_confidence, happy,
            happy_confidence, sad,
            sad_confidence, peak,
            loudness_integrated, loudness_range
        )
        VALUES ("""

        query = "{}{}, {}, {}, ".format(query, ids[0], ids[1], ids[2])

        if 'BPM' in data:
            query = "{}{}, {}, ".format(
                query, data['BPM']['value'], data['BPM']['confidence'])
        else:
            query = query + "NULL, NULL, "

        if 'timbre' in data:
            query = "{}'{}', {}, ".format(
                query, data['timbre']['value'], data['timbre']['confidence'])
        else:
            query = query + "NULL, NULL, "

        if 'emotions' in data:
            query = "{}'{}', {}, ".format(
                query, data['emotions']['relaxed']['value'], data['emotions']['relaxed']['confidence'])
            query = "{}'{}', {}, ".format(
                query, data['emotions']['party']['value'], data['emotions']['party']['confidence'])
            query = "{}'{}', {}, ".format(
                query, data['emotions']['aggressive']['value'], data['emotions']['aggressive']['confidence'])
            query = "{}'{}', {}, ".format(
                query, data['emotions']['happy']['value'], data['emotions']['happy']['confidence'])
            query = "{}'{}', {}, ".format(
                query, data['emotions']['sad']['value'], data['emotions']['sad']['confidence'])
        else:
            query = query + "NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, "

        if 'loudness' in data:
            query = "{}{}, ".format(query, data['loudness']['peak'])
            query = "{}{}, ".format(
                query, data['loudness']['loudness_integrated'])
            query = "{}{})".format(query, data['loudness']['loudness_range'])
        else:
            query = query + "NULL, NULL, NULL)"

        self._db.query(query)

    def update_all(self, data: Dict) -> str:
        if not 'audio_id' in data:
            pass

        ids = data['audio_id'].split("-")

        if len(ids) != 3:
            return None

        query = "UPDATE Audio SET "

        if 'BPM' in data:
            query = "{}bpm={}, bpm_confidence={}, ".format(
                query, data['BPM']['value'], data['BPM']['confidence'])
        else:
            query = query + "bpm=NULL, bpm_confidence=NULL, "

        if 'timbre' in data:
            query = "{}timbre='{}', timbre_confidence={}, ".format(
                query, data['timbre']['value'], data['timbre']['confidence'])
        else:
            query = query + "timbre=NULL, timbre_confidence=NULL, "

        if 'emotions' in data:
            query = "{}relaxed='{}', relaxed_confidence={}, ".format(
                query, data['emotions']['relaxed']['value'], data['emotions']['relaxed']['confidence'])
            query = "{}party='{}', party_confidence={}, ".format(
                query, data['emotions']['party']['value'], data['emotions']['party']['confidence'])
            query = "{}aggressive='{}', aggressive_confidence={}, ".format(
                query, data['emotions']['aggressive']['value'], data['emotions']['aggressive']['confidence'])
            query = "{}happy='{}', happy_confidence={}, ".format(
                query, data['emotions']['happy']['value'], data['emotions']['happy']['confidence'])
            query = "{}sad='{}', sad_confidence={}, ".format(
                query, data['emotions']['sad']['value'], data['emotions']['sad']['confidence'])
        else:
            query = query + "relaxed=NULL, relaxed_confidence=NULL, party=NULL, party_confidence=NULL, aggressive=NULL, aggressive_confidence=NULL, happy=NULL, happy_confidence=NULL, sad=NULL, sad_confidence=NULL, "

        if 'loudness' in data:
            query = "{}peak={}, ".format(query, data['loudness']['peak'])
            query = "{}loudness_integrated={}, ".format(
                query, data['loudness']['loudness_integrated'])
            query = "{}loudness_range={}, ".format(
                query, data['loudness']['loudness_range'])
        else:
            query = query + "peak=NULL, loudness_integrated=NULL, loudness_range=NULL, "

        query = query + "last_updated=CURRENT_TIMESTAMP "

        query = "{}WHERE audio_release={} AND audio_side={} AND audio_track={}".format(
            query, ids[0], ids[1], ids[2])

        self._db.query(query)

    def get_all(self, audio_id: str) -> str:
        """Get all fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT * 
                FROM Audio 
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_rhythm(self, audio_id: str) -> str:
        """Get all rhythm fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT bpm, bpm_confidence, last_updated
                FROM Audio 
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_bpm(self, audio_id: str) -> str:
        """Get all bpm fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT bpm, bpm_confidence, last_updated
                FROM Audio 
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_timbre(self, audio_id: str) -> str:
        """Get all timbre fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT timbre, timbre_confidence, last_updated
                FROM Audio
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_emotions(self, audio_id: str) -> str:
        """Get all emotion fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT relaxed, relaxed_confidence, party, party_confidence, 
                       aggressive, aggressive_confidence, happy, happy_confidence, 
                       sad, sad_confidence, last_updated
                FROM Audio 
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_relaxed(self, audio_id: str) -> str:
        """Get all relaxed fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT relaxed, relaxed_confidence, last_updated
                FROM Audio
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_party(self, audio_id: str) -> str:
        """Get all party fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT party, party_confidence, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)

    def get_aggressive(self, audio_id: str) -> str:
        """Get all aggressive fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT aggressive, aggressive_confidence, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)

    def get_happy(self, audio_id: str) -> str:
        """Get all happy fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT happy, happy_confidence, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)

    def get_sad(self, audio_id: str) -> str:
        """Get all sad fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
                SELECT sad, sad_confidence, last_updated
                FROM Audio
                WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
                """

        return self._get_data(query, audio_id)

    def get_level(self, audio_id: str) -> str:
        """Get all level fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT peak, Loudness_integrated, loudness_range, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)

    def get_peak(self, audio_id: str) -> str:
        """Get all peak fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT peak, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)

    def get_loudness_integrated(self, audio_id: str) -> str:
        """Get all loudness integrated fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT Loudness_integrated, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)

    def get_loudness_range(self, audio_id: str) -> str:
        """Get all loudness range fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        query = """
            SELECT loudness_range, last_updated
            FROM Audio
            WHERE audio_release=:rel AND audio_side=:side AND audio_track=:track
            """

        return self._get_data(query, audio_id)
