import os
import cv2

from video_emotion.facial_recognition.facial_recognition import analyze_video, analyze_frame

def test_facial_recognition_of_at_least_one_face():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_facial_recognition/Fun_at_a_Fair.mp4")

    output_frames = analyze_video(test_filename, (3000, 5000))

    assert len(output_frames) != 0

    frame_key = "79"
    faces = output_frames[frame_key]

    assert len(faces) == 2
'''
def test_facial_recognition_of_two_faces_in_single_frame():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_facial_recognition/Fun_at_a_Fair.mp4")

    cap = cv2.VideoCapture(test_filename)
    frame = cap.read()
    output_tuple = {}
    while(cap.isOpened()):
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
        if timestamp < 3079:
            continue
        elif timestamp > 3082:
            break
        output_tuple = analyze_frame(frame)

    assert len(output_tuple) != 0
    assert len(output_tuple) == 2
'''