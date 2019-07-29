import numpy as np
import cv2

from video_emotion.emotion_tagger.\
    face_emotion_extraction import classify_faces
from video_emotion.emotion_tagger.\
    face_emotion_extraction import get_labels
from video_emotion.emotion_tagger.\
    face_emotion_extraction import preprocess_input
from utilities.filehandler.handle_path import get_absolute_path

current_directory = "video_emotion/emotion_tagger/t/"


def test_angry_face():
    filename = get_absolute_path(current_directory +
                                 "test_face_emotion_extra" +
                                 "ction_data/angry1.png")
    img = cv2.imread(filename)
    face_data = classify_faces([img])
    assert len(face_data[0]) == 7
    assert face_data[0][0] > 0.5


def test_happy_1():
    filename = get_absolute_path(current_directory +
                                 "test_face_emotion_extra" +
                                 "ction_data/happy1.png")
    img = cv2.imread(filename)
    face_data = classify_faces([img])
    assert len(face_data[0]) == 7
    assert face_data[0][3] > 0.5


def test_happy_2():
    filename = get_absolute_path(current_directory +
                                 "test_face_emotion_extr" +
                                 "action_data/happy2.png")
    img = cv2.imread(filename)
    face_data = classify_faces([img])
    assert len(face_data[0]) == 7
    assert face_data[0][3] > 0.5


def test_happy_3():
    filename = get_absolute_path(current_directory +
                                 "test_face_emotion_extra" +
                                 "ction_data/happy3.png")
    img = cv2.imread(filename)
    face_data = classify_faces([img])
    assert len(face_data[0]) == 7
    assert face_data[0][3] > 0.3


def test_neutral_1():
    filename = get_absolute_path(current_directory +
                                 "test_face_emotion_extra" +
                                 "ction_data/neutral1.png")
    img = cv2.imread(filename)
    face_data = classify_faces([img])
    assert len(face_data[0]) == 7
    assert face_data[0][6] > 0.5


def test_get_labels_valid_input():
    dataset_expected = {0: 'angry', 1: 'disgust', 2: 'fear',
                        3: 'happy', 4: 'sad', 5: 'surprise',
                        6: 'neutral'}

    result = get_labels()

    assert dataset_expected == result


def test_preprocess_input():  # expermentially we have reached that it should
    # output the expected value
    expected = 0.9607843137254901

    tf = np.float32(250)  # testing float
    result = preprocess_input(tf)

    assert (expected == result)


def test_Many_Faces():
    face_list = []

    filename1 = get_absolute_path(current_directory +
                                  "test_face_emotion_extr" +
                                  "action_data/happy1.png")
    filename2 = get_absolute_path(current_directory +
                                  "test_face_emotion_extr" +
                                  "action_data/happy2.png")
    filename3 = get_absolute_path(current_directory +
                                  "test_face_emotion_extr" +
                                  "action_data/happy3.png")

    img1 = cv2.imread(filename1)
    img2 = cv2.imread(filename2)
    img3 = cv2.imread(filename3)
    face_list.append(img1)
    face_list.append(img2)
    face_list.append(img3)
    list_with_faces = classify_faces(face_list)
    assert list_with_faces[0][3] > 0.5
    assert list_with_faces[1][3] > 0.5
    assert list_with_faces[2][3] > 0.3
