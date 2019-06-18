import json

from records import Database


class AudioDB:
    def __init__(self):
        self._db = Database('mysql://root:pass@sqldb/itumir')

        self._db.query("""DROP TABLE Audio;
        CREATE TABLE IF NOT EXISTS Audio
        (
            sRelease INT NOT NULL,
            Side INT NOT NULL,
            Track INT NOT NULL,
            BPM INT,
            BPM_Confidence FLOAT,
            Timbre VARCHAR(20),
            Timbre_Confidence FLOAT,
            Relaxed VARCHAR(20),
            Relaxed_Confidence FLOAT,
            Party VARCHAR(20),
            Party_Confidence FLOAT,
            Aggressive VARCHAR(20),
            Aggressive_Confidence FLOAT,
            Happy VARCHAR(20),
            Happy_Confidence FLOAT,
            Sad VARCHAR(20),
            Sad_Confidence FLOAT,
            Peak FLOAT,
            Loudness_Integrated FLOAT,
            Loudness_Range FLOAT,
            Last_Updated TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
            Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(sRelease, Side, Track)
        )""")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT * 
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT BPM, BPM_Confidence, Last_Updated
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

    def get_bpm(self, audio_id: str) -> str:
        """Get all BPM fields for the given audio_id

        Parameters
        ----------
        audio_id : str
            The id of the audio to search for

        Returns
        -------
        str
            A JSON string containing the result
        """

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT BPM, BPM_Confidence, Last_Updated
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Timbre, Timbre_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Relaxed, Relaxed_Confidence, Party, Party_Confidence, 
                   Aggressive, Aggressive_Confidence, Happy, Happy_Confidence, 
                   Sad, Sad_Confidence, Last_Updated
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2])

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Relaxed, Relaxed_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Party, Party_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Aggressive, Aggressive_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Happy, Happy_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Sad, Sad_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Peak, Loudness_Integrated, Loudness_Range, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

    def get_peak(self, audio_id: str) - str:
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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Peak, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Loudness_Integrated, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")

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

        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Loudness_Range, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows.export("json")
