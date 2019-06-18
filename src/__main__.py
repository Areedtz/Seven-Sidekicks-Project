#!/usr/local/bin/python3.6
import os
from pymongo import MongoClient

from similarity.similarity import analyze_songs, _load_songs
from database.song_segment import SongSegment
from utilities.get_song_id import get_song_id
from utilities.config_loader import load_config

if __name__ == "__main__":
    ss = SongSegment()

    res = ss.get_all()

    cfg = load_config()

    _client = MongoClient(
        cfg['mongo_host'], cfg['mongo_port'],
        username=cfg['mongo_user'],
        password=cfg['mongo_pass'])
    _db = _client[cfg['mongo_db']]
    _db = _db['song_segmentation']

    res = _db.aggregate([{'$group': {'_id': '$song_id'}}])

    songs = []
    for r in res:
        songs.append((r['_id'], ''))

    _client.close()

    analyze_songs(songs)
