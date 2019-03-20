import os

import numpy as np
import cv2

from video_emotion.emotionTagger.face_emotion_extraction import classify_face,classify_faces
from video_emotion.emotionTagger.face_emotion_extraction import get_labels
from video_emotion.emotionTagger.face_emotion_extraction import preprocess_input


def test_angry_face():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/angry1.png")
    img = cv2.imread(filename)
    faceData = classify_face(img)
    assert len(faceData) == 7
    assert faceData[0] > 0.5

def test_happy_1():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/happy1.png")
    img = cv2.imread(filename)
    faceData = classify_face(img)
    assert len(faceData) == 7
    assert faceData[3] > 0.5

def test_happy_2():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/happy2.png")
    img = cv2.imread(filename)
    faceData = classify_face(img)
    assert len(faceData) == 7
    assert faceData[3] > 0.5

def test_happy_3():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/happy3.png")
    img = cv2.imread(filename)
    faceData = classify_face(img)
    assert len(faceData) == 7
    assert faceData[3] > 0.3
    
def test_neutral_1():
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_face_emotion_extraction_data/neutral1.png")
    img = cv2.imread(filename)
    faceData = classify_face(img)
    assert len(faceData) == 7
    assert faceData[6] > 0.5

def test_get_labels_valid_input():
    dataset_expected = {0:'angry', 1:'disgust', 2:'fear',
                        3:'happy', 4:'sad', 5:'surprise',
                        6:'neutral'}

    result = get_labels()

    assert dataset_expected == result

def test_preprocess_input(): #test if the preprocessor behaves as it should
    expected = 0.9607843137254901

    tf = np.float32(250) # testing float
    result = preprocess_input(tf)

    assert (expected == result)

def test_Many_Faces():
    face_list = []
    dirname = os.path.abspath(os.path.dirname(__file__))
    fileName1 = os.path.join(
                            dirname,
                            "test_face_emotion_extraction_data/happy1.png")
    fileName2 = os.path.join(
                            dirname,
                            "test_face_emotion_extraction_data/happy2.png")
    fileName3 = os.path.join(
                            dirname,
                            "test_face_emotion_extraction_data/happy3.png")
    img1 = cv2.imread(fileName1)
    img2 = cv2.imread(fileName2)
    img3 = cv2.imread(fileName3)
    face_list.append(img1)
    face_list.append(img2)
    face_list.append(img3)
    list_with_faces = classify_faces(face_list)
    assert list_with_faces[0][3]  > 0.5
    assert list_with_faces[1][3]  > 0.5
    assert list_with_faces[2][3]  > 0.3
    