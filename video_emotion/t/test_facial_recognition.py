import os

from video_emotion.facial_recognition.facial_recognition import analyze_video

def test_facial_recognition_of_at_least_one_face():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_facial_recognition/Fun_at_a_Fair.mp4")

    output_files = analyze_video(test_filename, (3000, 5000))

    output_file_name1 = os.path.join(
        dirname, "output_files/80_0.png")

    output_file_name2 = os.path.join(
        dirname, "output_files/80_1.png")

    assert len(output_files) != 0
'''
def test_facial_recognition_of_two_faces_in_one_frame():
    dirname = os.path.dirname(__file__)
    test_filename = os.path.join(
        dirname, "test_facial_recognition/Fun_at_a_Fair.mp4")

    output_files = facial_recognition(test_filename, (3000, 5000))

    output_file_name1 = os.path.join(
        dirname, "output_files/80_0.png")

    output_file_name2 = os.path.join(
        dirname, "output_files/80_1.png")

    assert (os.path.exists(output_file_name1) and os.path.exists(output_file_name2))
'''