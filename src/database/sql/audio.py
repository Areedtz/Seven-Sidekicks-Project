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

        self._db.query(
            "INSERT INTO Audio(sRelease, Side, Track, BPM) VALUES (10, 10, 10, 100)")

    def get_all(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT * 
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_bpm(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT BPM, BPM_Confidence, Last_Updated
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_timbre(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Timbre, Timbre_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_emotions(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Relaxed, Relaxed_Confidence, Party, Party_Confidence, 
                   Aggressive, Aggressive_Confidence, Happy, Happy_Confidence, 
                   Sad, Sad_Confidence, Last_Updated
            FROM Audio 
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2])

        return rows[0].export("json")

    def get_relaxed(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Relaxed, Relaxed_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_party(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Party, Party_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_aggressive(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Aggressive, Aggressive_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_happy(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Happy, Happy_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_sad(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Sad, Sad_Confidence, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_meter(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Peak, Loudness_Integrated, Loudness_Range, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_peak(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Peak, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_loudness_integrated(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Loudness_Integrated, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")

    def get_loudness_range(self, audio_id: str):
        ids = audio_id.split("-")

        rows = self._db.query("""
            SELECT Loudness_Range, Last_Updated
            FROM Audio
            WHERE sRelease=:rel AND Side=:side AND Track=:track
            """, rel=ids[0], side=ids[1], track=ids[2]
        )

        return rows[0].export("json")


if __name__ == "__main__":
    a = AudioDB()
    print(a.get_all("10-10-10"))
