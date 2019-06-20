#!/usr/local/bin/python3.6
#from rest_api.application import app, hostURL, hostPort


# if __name__ == "__main__":
#    app.run(host=hostURL, port=hostPort, debug=False

from tasks import check_done, add_bpm, add_emotions, add_metering, add_similarity_features, save_to_db
from celery import chain, group

if __name__ == "__main__":
    song = dict({
        'song_id': '8376-1-2',
        'source_path': '/code/similarity/t/test_split_song/8376-1-1_Demolition_Man_proud_music_preview.wav',
        'FORCE': True,
    })

    print(song)

    s = chain(
        check_done.s(),
        group(
            add_bpm.s(),
            add_emotions.s(),
            add_metering.s(),
            add_similarity_features.s(),
        ),
        save_to_db.s()
    )

    s.delay(song)

    print("Pipeline started")
