import os

import cv2

from video_emotion.facial_recognition.facial_recognition import analyze_video, analyze_frame


def test_facial_recognition_of_at_least_one_face():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_facial_recognition/Fun_at_a_Fair.mp4")

    output_frames = analyze_video(test_filename, (3000, 5000))  # analyze from 3s to 5s for performance reasons

    assert len(output_frames) != 0

    frame_key = "79"
    faces = output_frames[frame_key]

    assert len(faces) == 2
