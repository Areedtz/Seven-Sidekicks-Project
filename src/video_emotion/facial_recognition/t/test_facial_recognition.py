from video_emotion.facial_recognition.facial_recognition import analyze_video
from utilities.filehandler.handle_path import get_absolute_path


def test_facial_recognition_of_at_least_one_face():
    test_filename = (get_absolute_path
                     ("video_emotion/facial_recognition/t/test" +
                      "_facial_recognition/Fun_at_a_Fair.mp4"))

    # analyze from 3s to 5s for performance reasons
    output_frames = analyze_video(test_filename, (3000, 5000))

    assert len(output_frames) != 0
