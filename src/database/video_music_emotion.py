from database.storinator import Storinator
from database.video_music_emotion_database import VMEDatabase


class VideoMusicEmotion(Storinator):
    def __init__(self):
        self._col = 'video_music_emotion'
        self._db = VMEDatabase()

    def add(self, song_id, video_id,
            bpm, timbre, party, relaxed, emotions):
        return self._db.insert(self._col, song_id, video_id,
                               bpm, timbre, party,
                               relaxed, emotions)

    def get(self, song_id, video_id):
        return self._db.find(self._col, song_id, video_id)

    def get_all(self):
        return self._db.find_all(self._col)

    def close(self):
        self._db.close()
